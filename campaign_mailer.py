#!/usr/bin/env python3
"""Automate a personalized email campaign from CSV contacts and templates."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import smtplib
import ssl
import sys
import time
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable

TOKEN_PATTERN = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")
SKIPPED_STATUSES = {"done", "sent", "skip", "skipped"}


@dataclass(frozen=True)
class Contact:
    row_number: int
    email: str
    data: dict[str, str]

    def render_context(self) -> dict[str, str]:
        context = dict(self.data)
        context.setdefault("email", self.email)
        context.setdefault("today", dt.date.today().isoformat())
        return context


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    username: str
    password: str
    security: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare and send personalized campaign emails."
    )
    parser.add_argument(
        "--contacts",
        default="data/contacts.csv",
        help="CSV file containing at least an email column.",
    )
    parser.add_argument(
        "--subject-template",
        default="templates/media_subject.txt",
        help="Path to the email subject template.",
    )
    parser.add_argument(
        "--body-template",
        default="templates/media_body.txt",
        help="Path to the email body template.",
    )
    parser.add_argument(
        "--log-file",
        default="outbox/sent-log.jsonl",
        help="JSONL log used to skip recipients already contacted.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of contacts to process.",
    )
    parser.add_argument(
        "--sender",
        default=os.getenv("MAIL_SENDER", ""),
        help="Sender email address. Defaults to MAIL_SENDER.",
    )
    parser.add_argument(
        "--reply-to",
        default=os.getenv("MAIL_REPLY_TO", ""),
        help="Optional reply-to address. Defaults to MAIL_REPLY_TO.",
    )
    parser.add_argument(
        "--context",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Static template variable available to every email. Repeat as needed.",
    )
    parser.add_argument(
        "--throttle-seconds",
        type=float,
        default=5.0,
        help="Delay between emails in send mode.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser(
        "preview", help="Render sample emails without sending."
    )
    preview_parser.add_argument(
        "--sample-count",
        type=int,
        default=3,
        help="How many rendered emails to display.",
    )

    send_parser = subparsers.add_parser(
        "send", help="Send emails through an SMTP server."
    )
    send_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and list messages without connecting to SMTP.",
    )
    send_parser.add_argument(
        "--smtp-host",
        default=os.getenv("SMTP_HOST", ""),
        help="SMTP host. Defaults to SMTP_HOST.",
    )
    send_parser.add_argument(
        "--smtp-port",
        type=int,
        default=int(os.getenv("SMTP_PORT", "587")),
        help="SMTP port. Defaults to SMTP_PORT or 587.",
    )
    send_parser.add_argument(
        "--smtp-user",
        default=os.getenv("SMTP_USER", ""),
        help="SMTP username. Defaults to SMTP_USER.",
    )
    send_parser.add_argument(
        "--smtp-password",
        default=os.getenv("SMTP_PASSWORD", ""),
        help="SMTP password. Defaults to SMTP_PASSWORD.",
    )
    send_parser.add_argument(
        "--smtp-security",
        choices=("starttls", "ssl", "none"),
        default=os.getenv("SMTP_SECURITY", "starttls"),
        help="SMTP transport security mode.",
    )

    return parser.parse_args()


def load_contacts(path: str | Path) -> list[Contact]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Contacts file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("The contacts CSV is empty.")
        if "email" not in [name.strip() for name in reader.fieldnames]:
            raise ValueError("The contacts CSV must contain an 'email' column.")

        contacts: list[Contact] = []
        for row_number, raw_row in enumerate(reader, start=2):
            cleaned_row = {
                (key or "").strip(): (value or "").strip()
                for key, value in raw_row.items()
            }

            if not any(cleaned_row.values()):
                continue

            email = cleaned_row.get("email", "")
            if not email:
                raise ValueError(f"Missing email in CSV row {row_number}.")

            contacts.append(Contact(row_number=row_number, email=email, data=cleaned_row))

    return contacts


def load_template(path: str | Path) -> str:
    template_path = Path(path)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def render_template(template: str, context: dict[str, str]) -> str:
    missing_keys: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = context.get(key, "")
        if not value:
            missing_keys.append(key)
            return match.group(0)
        return value

    rendered = TOKEN_PATTERN.sub(replace, template)
    if missing_keys:
        ordered_keys = ", ".join(sorted(set(missing_keys)))
        raise ValueError(f"Missing values for template fields: {ordered_keys}")
    return rendered


def load_sent_recipients(path: str | Path) -> set[str]:
    log_path = Path(path)
    if not log_path.exists():
        return set()

    sent: set[str] = set()
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            email = str(entry.get("email", "")).strip().lower()
            if email:
                sent.add(email)
    return sent


def select_contacts(
    contacts: Iterable[Contact],
    already_sent: set[str],
    limit: int | None = None,
) -> list[Contact]:
    selected: list[Contact] = []

    for contact in contacts:
        status = contact.data.get("status", "").strip().lower()
        if status in SKIPPED_STATUSES:
            continue
        if contact.email.strip().lower() in already_sent:
            continue

        selected.append(contact)
        if limit is not None and len(selected) >= limit:
            break

    return selected


def parse_context_args(items: Iterable[str]) -> dict[str, str]:
    context: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --context value '{item}'. Expected KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError("Context keys cannot be empty.")
        context[key] = value
    return context


def prepare_messages(
    contacts: Iterable[Contact],
    subject_template: str,
    body_template: str,
    shared_context: dict[str, str] | None = None,
) -> list[tuple[Contact, str, str]]:
    rendered_messages: list[tuple[Contact, str, str]] = []
    shared_context = shared_context or {}

    for contact in contacts:
        context = {**shared_context, **contact.render_context()}
        subject = render_template(subject_template, context)
        body = render_template(body_template, context)
        rendered_messages.append((contact, subject, body))

    return rendered_messages


def build_message(
    sender: str,
    reply_to: str,
    recipient: str,
    subject: str,
    body: str,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    if reply_to:
        message["Reply-To"] = reply_to
    message.set_content(body)
    return message


def append_log(path: str | Path, entry: dict[str, str | int]) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def smtp_client(config: SMTPConfig):
    if config.security == "ssl":
        return smtplib.SMTP_SSL(config.host, config.port, context=ssl.create_default_context())

    client = smtplib.SMTP(config.host, config.port)
    client.ehlo()
    if config.security == "starttls":
        client.starttls(context=ssl.create_default_context())
        client.ehlo()
    return client


def ensure_sender(sender: str) -> None:
    if not sender:
        raise ValueError(
            "Missing sender email. Pass --sender or set the MAIL_SENDER environment variable."
        )


def ensure_smtp_config(args: argparse.Namespace) -> SMTPConfig:
    if not args.smtp_host:
        raise ValueError("Missing SMTP host. Pass --smtp-host or set SMTP_HOST.")

    if args.smtp_security in {"starttls", "ssl"} and not args.smtp_user:
        raise ValueError("Missing SMTP user. Pass --smtp-user or set SMTP_USER.")
    if args.smtp_security in {"starttls", "ssl"} and not args.smtp_password:
        raise ValueError("Missing SMTP password. Pass --smtp-password or set SMTP_PASSWORD.")

    return SMTPConfig(
        host=args.smtp_host,
        port=args.smtp_port,
        username=args.smtp_user,
        password=args.smtp_password,
        security=args.smtp_security,
    )


def command_preview(args: argparse.Namespace) -> int:
    contacts = load_contacts(args.contacts)
    sent = load_sent_recipients(args.log_file)
    selected = select_contacts(contacts, sent, limit=args.limit or args.sample_count)
    subject_template = load_template(args.subject_template)
    body_template = load_template(args.body_template)
    shared_context = parse_context_args(args.context)
    prepared = prepare_messages(selected, subject_template, body_template, shared_context)

    if not prepared:
        print("No contacts available for preview.")
        return 0

    for index, (contact, subject, body) in enumerate(prepared[: args.sample_count], start=1):
        print(f"--- Preview #{index} | {contact.email} ---")
        print(f"Subject: {subject}")
        print()
        print(body)
        print()

    print(
        f"Previewed {min(len(prepared), args.sample_count)} email(s) "
        f"out of {len(prepared)} selected contact(s)."
    )
    return 0


def command_send(args: argparse.Namespace) -> int:
    ensure_sender(args.sender)

    contacts = load_contacts(args.contacts)
    sent = load_sent_recipients(args.log_file)
    selected = select_contacts(contacts, sent, limit=args.limit)
    subject_template = load_template(args.subject_template)
    body_template = load_template(args.body_template)
    shared_context = parse_context_args(args.context)
    shared_context.setdefault("sender_email", args.sender)
    prepared = prepare_messages(selected, subject_template, body_template, shared_context)

    if not prepared:
        print("No contacts left to send.")
        return 0

    if args.dry_run:
        print(f"Dry run: {len(prepared)} email(s) validated and ready to send.")
        for contact, subject, _ in prepared:
            print(f"- {contact.email} | {subject}")
        return 0

    config = ensure_smtp_config(args)

    with smtp_client(config) as client:
        if config.username:
            client.login(config.username, config.password)

        for index, (contact, subject, body) in enumerate(prepared, start=1):
            message = build_message(
                sender=args.sender,
                reply_to=args.reply_to,
                recipient=contact.email,
                subject=subject,
                body=body,
            )
            client.send_message(message)
            append_log(
                args.log_file,
                {
                    "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "email": contact.email,
                    "subject": subject,
                    "row_number": contact.row_number,
                },
            )
            print(f"[{index}/{len(prepared)}] Sent to {contact.email}")
            if index < len(prepared) and args.throttle_seconds > 0:
                time.sleep(args.throttle_seconds)

    print(f"Campaign complete: {len(prepared)} email(s) sent.")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "preview":
        return command_preview(args)
    if args.command == "send":
        return command_send(args)
    raise AssertionError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - CLI safety net
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
