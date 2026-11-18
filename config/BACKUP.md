# Back up your custom config (preferences only, not messages)

**Why:** your bot's computer and memory can be reset. Shared files (ontology, scripts, prompts) come back from this git repo; your *personal* settings do not unless you saved a copy.

## What this backup includes
Your **preferences and configuration settings**:
- Group label and JID (placeholders in `custom.json`), timezone, store path
- Priority people, keywords, custom topics
- Relationship / topic weights, if you set any
- Alert details: critical-watch rules, digest schedules (weekday / weekly), notification config pointers
- The custom ontology layer (topics, aliases, weights, keywords)

## What it does NOT include
- **WhatsApp messages, the message store, or media.** None of these go in the export.
- After a reset, re-pair wacli to rebuild the store from WhatsApp.

| Shared (in this repo) | Custom config (never in the public repo) |
| --- | --- |
| `ontology/`, `scripts/`, `prompts/`, `examples/` | `config/custom.json`, `config/*.local.json` |

**Recommended**
1. **Private clone:** keep `config/custom.json` (gitignored) in your own private clone or fork.
2. **Periodic bot export:** use `prompts/07-backup-custom-config.md` to have the bot rebuild `custom.json` from memory and give you a downloadable JSON. Do this after changing people, keywords, weights, or alerts.
3. **Optional off-box copy:** store that JSON in a private Drive folder or encrypted note.

**Never** commit `custom.json` (or any `*.local.json`) to the public repo.

## Optional: separate message-store backup
If the messages themselves are critical to keep, set up a **different, optional job** that backs up the message store (for example, a private encrypted archive). It is separate from this prefs export, holds private data, and must never go in this repo or any public repo.

**Restore prefs:** new bot → load this repo → upload your backup JSON → "Restore my custom config from this file and re-apply the send lock."

## Ontology review
Agreeing to a custom topic, alias, weight, or keyword during ontology review changes your prefs. Refresh this backup afterward (prompt 07). Shared ontology on git `main` is not part of this prefs backup; bots refresh `ontology/` using `ontology/LAST_UPDATE`. See `docs/ONTOLOGY-LAYERS.md`.

## Migration
The custom layer and this config used to be called personal. `config/personal.json` still works when `config/custom.json` is missing, and `.gitignore` lists both. When both exist, the scripts use `custom.json`. Older exports may be named `personal-config-backup-YYYY-MM-DD.json`. Prompt 07 used to live at `prompts/07-backup-personal-config.md`.
