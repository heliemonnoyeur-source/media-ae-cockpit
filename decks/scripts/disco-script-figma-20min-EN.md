# Cursor × Figma — 20-min Discovery Script (Value Selling)

**Cast in the room**

- **You** — Cursor AE
- **Marcel** — Marcel Weekes, VP of Engineering, Figma (~650 engineers)
- **SEL** — Security Engineering Leader
- **SEC** — Security team member

**Known facts walking in**

- ~85% on VS Code · GitHub Copilot deployed team-wide
- Currently evaluating Claude Code
- 31 Cursor Pro shadow users · mixed Privacy Mode

**Methodology — Value Selling reminders**

- Discovery is about *their* P&L, not our product
- Open questions only until minute 9
- Ask about **impact and consequence**, not symptoms
- Get them to **quantify in their own words**
- Surface the **cost of inaction**
- Equip Marcel with the story he'll repeat upward (champion enablement)

---

## 00:00 – 02:00 · Frame & permission

> "Marcel, thanks for the 20 minutes. [SEL], [SEC] — thanks for joining. Having you both in the room is exactly what's useful here, so I want to make sure we cover what matters for each of you.
>
> Before we get into anything: I noticed **31 of your engineers are already on Cursor Pro**, in mixed Privacy Mode. I'd rather start there than pitch. So I'm going to spend most of the time asking questions, then I'll share where I think Cursor fits — or doesn't — for what you're trying to do.
>
> The goal on my side isn't to close anything in 20 minutes; it's to find out whether a specific follow-up is worth your team's time.
>
> Sound right? Anything you want to add or take off the agenda?"

*Pause. Let them respond.*

---

## 02:00 – 09:00 · Pain Discovery (open questions only)

### Q1 — Copilot baseline *(impact, not features)*

> "Marcel, walk me through how the Copilot rollout went. Where did it land vs where you'd hoped it would, a year in?"

**Listen for:** quality plateau · adoption plateau · senior IC opt-out · whether the ROI was ever measured.

### Q2 — The metric that matters *(value-selling anchor)*

> "When your exec team looks at engineering throughput today — cycle time, PR throughput, whatever your north-star metric is — what's the line that's not moving as fast as it needs to?"

**Why this question:** It pins the rest of the call to *their* business outcome, not your product. Everything downstream gets tied back to this metric.

### Q3 — The 31 Pro users *(vulnerability-inviting, signals their champion landscape)*

> "The 31 Pro users — how did that emerge, and what does it signal to you? I'm curious whether you think of it as a positive signal, a risk signal, or both."

**Why this question:** Three possible outputs. (a) If Marcel didn't know → visibility gap = wedge. (b) If he did know → you find out who's tracking and what they're doing about it. (c) Either way, the shadow usage becomes a Cursor-friendly conversation, not a security incident waiting to happen.

### Q4 — Claude Code *(pressure-test urgency)*

> "Help me understand the Claude Code evaluation. What pulled you toward looking at it, and what would have to be true for you to actually switch?"

**Listen for:** real driver behind the eval · the switching bar you have to clear · is this curiosity, board pressure, or a specific feature gap.

### Q5 — Senior tier *(org-pattern probe)*

> "When you look at how your senior ICs use AI tools versus your juniors — is there a difference? And if there is, what do you think it tells you?"

**Why this question:** Senior opt-out is the most expensive symptom in eng productivity. If they confirm it, you've found the gap Cursor is best placed to close.

### Q6 — Hand-off to security *(value-led)*

> "[SEL] — I'd love your view on this. From where you sit, what does AI tooling actually **cost** Figma today in terms of risk exposure or governance overhead? Not in theory — in the real day-to-day."

**Why this question:** The word "cost" — not "concern" — primes business framing for security. Gives [SEL] their seat without making them the blocker.

### Q7 — Cost of inaction *(value selling crown jewel)*

> "Last open question before I share where I think we fit — if you held everything constant for 6 more months, no new AI tool decisions, what's the version of Figma that worries you most? What's the cost of standing still?"

**Why this question:** Surfaces the cost of inaction in their own words. This is what justifies any deal in a procurement cycle — and it's what Marcel will need to say upward when he champions the deal.

*Total listening time: 6–9 minutes. Count to 3 after each answer before asking the next.*

---

## 09:00 – 13:00 · Vision & Why Cursor

> "Okay — really helpful, thank you. Let me share where I think this lands, then I'd love to test it with you.

### Three things on Cursor — honest about where we win and where we don't.

**One — what we are.**

> Cursor is the editor at the center of an AI-native engineering org. ~70% of the Fortune 1000 are already on it, and the reason is pretty specific: we're not 'AI added to an editor,' we're the editor designed for an org where most non-trivial work involves an AI agent at some point in the loop.
>
> That distinction matters for Figma specifically because, with 85% of your team already in VS Code and a complex C++/WASM + Rust + TS codebase, switching tools is normally an adoption tax. **Cursor is a VS Code fork** — your engineers' muscle memory, extensions, keymaps, settings all carry over. The adoption cost is close to zero. That's the practical part.

**Two — the strategic part. Where our CEO's vision matters.**

> Michael Truell, our CEO and co-founder, has been pretty explicit about where we think this is going. His framing — and the reason we built Cursor the way we did — is that **software development is shifting from typing characters one at a time to expressing intent.** The editor becomes the place where the conversation between an engineer and an AI happens.
>
> The thesis is that we're moving toward what he calls a **'human-AI programmer'** — one entity, combining engineer judgment with AI execution, where senior judgment gets *more* valuable, not less.
>
> For an org like Figma — 650 engineers, real performance constraints, a product that ships AI features itself — that's not abstract. It means the place your engineers spend their day stops being a code editor and starts becoming the system where engineering judgment scales.
>
> **The business outcome we're betting on isn't '20% faster typing.'** It's that the leverage of a single senior engineer becomes 3–5× what it is today, and the orgs that get there first compound that advantage every quarter. That's the bet — and we want Figma to be running on that curve, not behind it.

**Three — the honest comparison.**

> - **Versus Copilot:** the gap we see widening is on large-codebase tasks — refactors that span services, navigating unfamiliar code, reproducing bugs, writing the test that should exist but doesn't.
> - **Versus Claude Code,** which I know you're evaluating: two real differences. **Model neutrality** — you're not betting the next 12 months on Anthropic's roadmap exclusively. And **full IDE integration** rather than CLI-first, which matters when 85% of your team is already in VS Code.
> - **Where we don't obviously win:** if your bar is purely 'best frontier model for one specific task,' Claude Code is a perfectly good answer for that specific task. Our argument is the editor + agent + context combo is what wins over 12 months, not the model alone.

> "Does any of that match what you're seeing internally?"

*Re-open the conversation. Don't monologue past 4 minutes.*

---

## 13:00 – 17:00 · Security (preempt the objection)

> "Before next steps, I want to take security head-on because if I were in [SEL]'s seat it would be my first question. Three things:
>
> — **Code is not stored or retained.** Contractual, not a setting.
> — **Code is not used to train models.** Ours or any third-party provider's.
> — **Requests are isolated and ephemeral.** No persistent prompt logs in Privacy Mode.
>
> Plus SOC 2, admin controls, SSO, audit log export. The practical version of this conversation, [SEL]: we can have our security team on a call with yours within 7 days, with SIG, pentest summary, and a draft DPA in your hands before that call.
>
> The reason I bring this up now is the 31 Pro users you have today are running in mixed Privacy Mode — **the risk is already on your floor, just uncontrolled.** Switching them to mandated Privacy Mode is a < 1 day change.
>
> [SEL] — what's the question I haven't answered?"

*Hand the mic to security explicitly. Don't fill the silence.*

---

## 17:00 – 20:00 · Close (value-anchored, champion-enabling)

> "Marcel — based on what you've told me, here's what I'd propose, and tell me if it's the right next step or the wrong one.
>
> **A single 60-minute follow-up, within 10 days. Two purposes in one block:**
>
> — **First half:** technical scoping of a 20–30 engineer POC on a repo you choose. We pre-define the metrics — cycle time, PR throughput, senior IC adoption, NPS at day 15 and day 30. So when the POC ends, the conversation with your CFO or board has actual numbers, not vibes.
>
> — **Second half:** security review track in parallel. SIG, pentest, architecture, DPA all sent 7 days ahead. Your team isn't starting from zero when the technical POC finishes.
>
> The reason I'm proposing both in one meeting is so neither of you becomes the bottleneck for the other.
>
> Two open questions for you before we book it:
>
> — **Who on your side should be in the room** — DevEx, AppSec, anyone else?
> — And — this is the more important one — **what would need to be true at the end of that 60 minutes for you to say 'yes, worth running the POC'?**"

*Stop. The second question is the value-selling close: you're getting them to define success criteria for the next step in their own words — which is exactly what a champion needs to take upward.*

---

## After the call — within 2 hours

Send two emails. **Not one.** One to Marcel, one to [SEL]. Each recaps **what they said**, not what you said. Each ends with the one specific action they own next.

This is the champion-enablement gesture. Marcel needs to be able to forward your email upward as the summary that justifies the next step.

---

## Value Selling — cheat sheet for the call

| Principle | In practice during this call |
|---|---|
| **Their P&L > your features** | Q2 anchors the call on Figma's metric. Reference it in every answer. |
| **Cost of inaction** | Q7 is the crown jewel. Don't skip it even if time is tight. |
| **Quantify in their words** | Don't say "20% productivity gain." Get *them* to say "we're missing 8% of senior IC capacity." |
| **Champion enablement** | The close question — "what would need to be true" — gives Marcel the success criteria he'll quote upward. |
| **Honest tradeoffs** | The "where we don't win" line on Claude Code earns you trust for the next 60 minutes. |
| **Vision over feature** | CEO vision section is what makes this Cursor and not "another AI dev tool." |

---

## Anti-blank — when the room goes quiet

| Trigger | Verbatim |
|---|---|
| Silence drags | *"I'd rather give you the time — this is your conversation."* |
| Cursor gets hit | *"Fair feedback — here's what we do well, here's where we're not the best."* |
| Number you don't know | *"I don't want to make one up — I'll get back to you with the real answer today."* |
| Pressure-test | *"What would need to be true for this to be a no?"* |
| Pivot to security | *"Before we go further, I want to open security — that's where this gets real."* |
| Close | *"One question before we book the follow-up: what should I have asked?"* |
