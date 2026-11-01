# Back up your personal config (preferences only, not messages)

**Why:** your bot's computer and memory can be reset. Shared files (ontology, scripts, prompts) come back from this kit; your *personal* settings do not unless you saved a copy.

## What this backup includes
Your **preferences and configuration settings**:
- Group label and JID (placeholders in `personal.json`), timezone, store path
- Priority people, keywords, custom topics
- Relationship / topic weights, if you set any
- Alert details: critical-watch rules, digest schedules (weekday / weekly), notification config pointers

## What it does NOT include
- **WhatsApp messages, the message store, or media.** None of these go in the export.
- After a reset, re-pair wacli to rebuild the store from WhatsApp.

| Shared (in the kit) | Personal prefs (never in the public kit) |
| --- | --- |
| `ontology/`, `scripts/`, `prompts/`, `examples/` | `config/personal.json`, `config/*.local.json` |

**Recommended**
1. **Private clone:** keep `config/personal.json` (gitignored) in your own private clone or fork.
2. **Periodic bot export:** use `prompts/07-backup-personal-config.md` to have the bot rebuild `personal.json` from memory and give you a downloadable JSON. Do this after changing people, keywords, weights, or alerts.
3. **Optional off-box copy:** store that JSON in a private Drive folder or encrypted note.

**Never** commit `personal.json` (or any `*.local.json`) to the public kit.

## Optional: separate message-store backup
If the messages themselves are critical to keep, set up a **different, optional job** that backs up the message store (for example, a private encrypted archive). It is separate from this prefs export, holds private data, and must never go in the kit or a public repo.

**Restore prefs:** new bot → load the kit → upload your backup JSON → "Restore my personal config from this file and re-apply the send lock."
