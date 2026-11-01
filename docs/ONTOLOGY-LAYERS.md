# Ontology layers: core vs personal extension

Your bot sorts messages into topics using **two layers**:

| Layer | Where it lives | Who owns it |
|---|---|---|
| **Core** | `ontology/*.share.json` in this public repo | Shared by everyone; changes only via reviewed PR |
| **Personal extension** | `custom_topics`, `topic_aliases`, `topic_weights`, `relationship_weights`, `keywords` in your `config/personal.json` (and optionally `config/ontology.personal.json`) | You only; never committed |

**The classifier uses core ∪ personal.** Personal entries can add topics, add aliases/keywords to core topics, or re-weight topics and relationships. They never edit the core files.

## When the bot finds a gap
A gap = messages that match no topic, or a term you keep using that isn't in the vocabulary. The bot triages it:

- **Personal (default)** — specific to your group, people, local slang, or your priorities. Saved to your personal extension right away.
- **Core candidate** — generic, useful to most groups, not tied to names or private context, and not a duplicate of an existing core topic (else it becomes an alias). The bot **drafts a proposal** (term, preferred label, aliases, parent area, relationships, 2–3 anonymized examples) and asks you. Only with your explicit OK does it open a PR to the repo. Until merged, it stays in your personal layer.

Nothing goes into core automatically.

## Backup
Your prefs backup (`config/BACKUP.md`, prompt 07) **includes the personal ontology overlay** (topics, aliases, weights, keywords, alert details). It does **not** include messages — a message-store backup is a separate, optional private job.

Prompt: `prompts/08-ontology-gap-triage.md`.

## Ontology review (git freshness + owner agree/tweak)
- Shared ontology lives in the git repo `avilesg/message-dashboard-kit` on `main`, folder `ontology/`. `ontology/LAST_UPDATE` is the freshness flag; any change under `ontology/` must bump it.
- On gap detection or classify refresh: fetch `ontology/LAST_UPDATE` from git `main`, compare with the last-seen value; if newer (or missing locally), refresh the whole `ontology/` folder; then assess personal vs core-candidate.
- Config: `ontology_review` in the notification config (`core_from_git`, `candidates_from_messages`, `git`). If `notify_in_bot_chat` is true, message the owner in bot chat with labeled sections **Core (from git)** and **Candidate (from messages)**, and wait for agree/tweak before applying the personal overlay or proposing a git PR (`require_owner_agree_before_apply`).
