import unittest

from campaign_mailer import (
    Contact,
    parse_args,
    prepare_messages,
    render_template,
    select_contacts,
)


class CampaignMailerTests(unittest.TestCase):
    def test_render_template_replaces_known_fields(self):
        rendered = render_template(
            "Bonjour {{ name }}, voici {{ company }}.",
            {"name": "Lea", "company": "Studio Nova"},
        )

        self.assertEqual(rendered, "Bonjour Lea, voici Studio Nova.")

    def test_render_template_rejects_missing_fields(self):
        with self.assertRaises(ValueError) as context:
            render_template("Bonjour {{ name }} depuis {{ outlet }}", {"name": "Lea"})

        self.assertIn("outlet", str(context.exception))

    def test_select_contacts_skips_sent_or_opted_out_rows(self):
        contacts = [
            Contact(2, "fresh@example.com", {"email": "fresh@example.com", "status": ""}),
            Contact(3, "sent@example.com", {"email": "sent@example.com", "status": ""}),
            Contact(4, "skip@example.com", {"email": "skip@example.com", "status": "skip"}),
        ]

        selected = select_contacts(contacts, {"sent@example.com"})

        self.assertEqual([contact.email for contact in selected], ["fresh@example.com"])

    def test_prepare_messages_uses_contact_context(self):
        contact = Contact(
            2,
            "hello@example.com",
            {"email": "hello@example.com", "name": "Lea", "company": "Studio Nova"},
        )

        prepared = prepare_messages(
            [contact],
            "Sujet pour {{ name }}",
            "Bonjour {{ name }},\nVotre projet chez {{ company }} m'interesse.",
        )

        _, subject, body = prepared[0]
        self.assertEqual(subject, "Sujet pour Lea")
        self.assertIn("Studio Nova", body)

    def test_prepare_messages_strips_subject_whitespace(self):
        contact = Contact(2, "hello@example.com", {"email": "hello@example.com", "name": "Lea"})

        prepared = prepare_messages([contact], "Sujet pour {{ name }}\n", "Bonjour {{ name }}")

        _, subject, _ = prepared[0]
        self.assertEqual(subject, "Sujet pour Lea")

    def test_parse_args_accepts_common_options_after_subcommand(self):
        args = parse_args(
            [
                "preview",
                "--contacts",
                "data/contacts.csv",
                "--context",
                "sender_name=Alex",
            ]
        )

        self.assertEqual(args.command, "preview")
        self.assertEqual(args.contacts, "data/contacts.csv")
        self.assertEqual(args.context, ["sender_name=Alex"])


if __name__ == "__main__":
    unittest.main()
