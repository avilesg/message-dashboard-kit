# Back up your personal config

**Why:** your bot's computer and memory can be reset. Shared files (ontology, scripts, prompts) come back from this kit; your *personal* settings do not unless you saved a copy.

| Shared (in the kit) | Personal (never in the public kit) |
| --- | --- |
| `ontology/`, `scripts/`, `prompts/`, `examples/` | `config/personal.json`, `config/*.local.json`: group JID/label, people, keywords, alert rules, store path |

**Recommended**
1. **Private clone:** keep `config/personal.json` (gitignored) in your own private clone or fork.
2. **Periodic bot export:** use `prompts/07-backup-personal-config.md` to have the bot rebuild `personal.json` from memory and give you a downloadable JSON. Do this after changing people/keywords/alerts.
3. **Optional off-box copy:** store that JSON in a private Drive folder or encrypted note.

**Never** commit `personal.json` (or any `*.local.json`) to the public kit. The WhatsApp store itself is not part of the backup; re-pair to rebuild it.

**Restore:** new bot → load the kit → upload your backup JSON → "Restore my personal config from this file and re-apply the send lock."
