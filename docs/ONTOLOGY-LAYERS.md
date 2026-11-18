# Ontology layers: core vs custom

Your bot sorts messages into topics using **two layers**. Topics in either layer tag messages right away.

| Layer | Where it lives | Who owns it |
|---|---|---|
| **Core** | `ontology/*.share.json` in this public repo | The shared list everyone who builds from the recipe starts with. Changes only via reviewed PR. |
| **Custom** | `custom_topics`, `topic_aliases`, `topic_weights`, `relationship_weights`, `keywords` in your `config/custom.json` (and optionally `config/ontology.custom.json`) | Your own add-on layer. Only you get it; never committed. |

**The classifier uses core ∪ custom.** Custom entries can add topics, add aliases/keywords to core topics, or re-weight topics and relationships. They never edit the core files. A topic in custom tags matching messages as soon as you save it, the same way a core topic tags messages for everyone whose copy of core includes it.

## When the bot finds a gap
A gap = messages that match no topic, or a term you keep using that isn't in the vocabulary. The bot triages it:

- **Custom (default)** — specific to your group, people, local slang, or your priorities. Saved to your custom layer right away, so it tags messages right away.
- **Core candidate** — generic, useful to most groups, not tied to names or private context, and not a duplicate of an existing core topic (else it becomes an alias). The bot **drafts a proposal** (term, preferred label, aliases, parent area, relationships, 2–3 anonymized examples) and asks you. Only with your explicit OK does it open a PR to the repo. Until merged, it stays in your custom layer and tags messages from there.

Nothing goes into core automatically.

## Backup
Your prefs backup (`config/BACKUP.md`, prompt 07) **includes the custom ontology overlay** (topics, aliases, weights, keywords, alert details). It does **not** include messages — a message-store backup is a separate, optional private job.

Prompt: `prompts/08-ontology-gap-triage.md`.

## Ontology review (git freshness + owner agree/tweak)
- Shared ontology lives in the git repo `avilesg/message-dashboard-kit` on `main`, folder `ontology/`. `ontology/LAST_UPDATE` is the freshness flag; any change under `ontology/` must bump it.
- On gap detection or classify refresh: fetch `ontology/LAST_UPDATE` from git `main`, compare with the last-seen value; if newer (or missing locally), refresh the whole `ontology/` folder; then assess custom vs core-candidate.
- Config: `ontology_review` in the notification config (`core_from_git`, `candidates_from_messages`, `git`). If `notify_in_bot_chat` is true, message the owner in bot chat with labeled sections **Core (from git)** and **Candidate (from messages)**, and wait for agree/tweak before applying the custom overlay or proposing a git PR (`require_owner_agree_before_apply`).

## Migration from the personal layer
This layer used to be called **personal**. The filenames moved with it:

| Then | Now |
|---|---|
| `config/personal.example.json` | `config/custom.example.json` |
| `config/personal.json` | `config/custom.json` |
| `config/ontology.personal.json` | `config/ontology.custom.json` |
| `prompts/07-backup-personal-config.md` | `prompts/07-backup-custom-config.md` |

Existing installs keep working. If `config/custom.json` is missing, the scripts still read `config/personal.json`. When both exist, the scripts use `custom.json`. The optional overlay follows the same rule: `config/ontology.custom.json`, then `config/ontology.personal.json` when the new file is absent. Bots that read the overlay should use that order. `.gitignore` covers both names. Do not commit either file.

An older notification config may set `default_layer` to `personal`. That value means `custom`. Older prompt 07 exports named `personal-config-backup-YYYY-MM-DD.json` are the same prefs export as `custom-config-backup-YYYY-MM-DD.json`.
