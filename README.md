# Sync your group chat to your own dashboard

A starter kit for turning **your own** WhatsApp group-chat history into a **personal** dashboard (counts by topic and author, thread drill-down, optional alerts to your bot chat).

**This is not a shared message database.** Everyone runs their own copy. Nothing in this repo contains anyone's messages, phone numbers, or private watchlists.

## What's here
| Path | What it is |
|---|---|
| `docs/TUTORIAL.md` | Step-by-step setup for non-technical users |
| `ontology/topics.share.json` | Shared topic vocabulary (areas → topics → keywords) |
| `ontology/entities.share.json` | Upper ontology: message types, facets, relationships |
| `examples/notification_config.example.json` | Placeholder alert settings — copy and edit privately |
| `scripts/` | Generic CLIs: `classify_store.py`, `build_roster.py`, `build_messages_embed.py` (read-only on a wacli store) |
| `prompts/` | Copy-paste prompts for your Grok Bot, in order |
| `config/` | `personal.example.json` sample for local-clone users (your filled copy is gitignored) |
| `.gitignore` | Keeps your archive, media, and private settings out of git |

## Quick start (default — no git needed)
1. Create a **new bot** in Grok Bot (e.g. "Message tracker").
2. Paste `prompts/01-load-kit.md` — it points the bot at this repo as its starting point. No clone, no repo of your own.
3. Follow the rest of `prompts/` in order (install wacli, pair QR, read-only lock, build tracker, optional alerts).

## Optional (advanced): run it on your own machine
Clone, `cp config/personal.example.json config/personal.json`, fill it in, and run the `scripts/` — see `config/README.md`. Your personal files stay gitignored.

## Want a change?
Ask for a capability; it's tested on a branch first and only merged if it stays generic (no group-specific or personal details). Or fork the kit yourself.

## Rules of the road
- Your archive stays on your machine / bot computer.
- The dashboard is **read-only** to WhatsApp: the bot never sends, types, or reacts in the group.
- Don't republish group content.

## Back up your customizations
Your personal settings (`config/personal.json`, `*.local.json`) are gitignored and live only on your bot computer. If it is reset they are gone. See [config/BACKUP.md](config/BACKUP.md) and prompt `prompts/07-backup-personal-config.md`.
