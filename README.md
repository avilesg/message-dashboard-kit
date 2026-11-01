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
| `.gitignore` | Keeps your archive, media, and private settings out of git |

## Quick start
1. Read `docs/TUTORIAL.md`.
2. Pair **wacli** (https://wacli.sh) as a linked device on your phone — recommended.
3. Ask your Grok Bot to load the ontology from this repo and build your dashboard from your own store.

## Rules of the road
- Your archive stays on your machine / bot computer.
- The dashboard is **read-only** to WhatsApp: the bot never sends, types, or reacts in the group.
- Don't republish group content.
