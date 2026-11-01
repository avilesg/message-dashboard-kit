# Tutorial: sync your group chat to your own dashboard

Audience: non-technical users with a Grok Bot (or similar bot with a computer).
Time: about 20–40 minutes the first time.

## 1. Why
- See patterns: who talks about what, and when.
- Don't miss the people and topics you care about.
- Keep your own copy, so when your interests change you just re-ask the dashboard — no re-exporting forever.

## 2. What you get
- A **personal message store** (your own copy of the chat, with media).
- A **dashboard**: counts by topic and author, date/time sliders, click through to the actual threads.
- **Optional alerts** to your private bot chat.
- Your data stays on your machine or your bot's computer.

## 3. What you need
- A Grok Bot (or Cursor bot) with its own computer ("the box").
- Your phone with WhatsApp, able to add a **linked device** (Settings → Linked devices).
- 20–40 minutes, and willingness to scan a QR code once.
- This repo's link.

## 3b. Default setup: a new Grok Bot pointed at this repo
1. In Grok Bot, create a **new bot** and name it something like **Message tracker**.
2. Paste the prompt in `prompts/01-load-kit.md`. It tells the bot to use `https://github.com/avilesg/message-dashboard-kit` as its starting point.
3. You do **not** need to clone, fork, or create a GitHub repo. The bot reads this repo and keeps your settings in its own memory.
4. Continue with the prompts in `prompts/` (02 → 06), which match Path A below.

**Advanced (optional):** if you know git and want everything on your own machine, clone the repo, copy `config/personal.example.json` to `config/personal.json`, and run `scripts/` locally (see `config/README.md`). Your personal files are gitignored.

## 4. Path A (recommended): wacli
**wacli** is a small command-line tool that connects to WhatsApp as a linked device (like WhatsApp Web) and saves messages to a local folder. Docs: https://wacli.sh

1. **Get wacli** — ask your bot: "Install wacli on your box from https://wacli.sh."
2. **Create an empty store folder** — e.g. "Create a folder called `my-chat-store` for wacli."
3. **Pair once** — the bot shows a QR. On your phone: WhatsApp → Settings → Linked devices → Link a device → scan. QRs expire fast; ask for a new one if needed.
4. **Pick the group** — "List my groups and use the one called …".
5. **Full history + media** — "Backfill all history for that group and download its media." This can take a while.
6. **Keep a quiet sync running** — "Leave wacli following that group so new messages arrive." Reactions are only captured live, from pairing onward.
7. **Point the dashboard at the store** — "Load the ontology from <repo URL> and build me a Message tracker Page from my store."
8. **Set the read-only habit (send lock)** — tell your bot once: "Never send, type, or react in WhatsApp. Read only." Save it to its memory.

## 5. Path B: WhatsApp export (fallback)
Use when you can't add a linked device, have an older phone, or want a one-shot snapshot.
1. In the group: ⋮ / group name → More → **Export chat** → with or without media.
2. Send the `.zip` or `_chat.txt` to your bot (upload in chat).
3. Ask it to build the dashboard from that file.

Limits: one-shot (re-export for updates), no reactions, media in big exports may be missing or expired, quote/reply links are weaker.

## 6. Topics (ontology)
- Copy `ontology/topics.share.json` and `ontology/entities.share.json` from this repo. Check `ontology/LAST_UPDATE` on git `main` so the core copy is current.
- Rename labels or add keywords any time — just ask your bot.
- Keep private priorities (people, your keywords) out of shared files.
- Two layers: this repo's **core** topics plus your **personal extension** (in your prefs). New terms default to personal; the bot only proposes core additions with your OK. See `ONTOLOGY-LAYERS.md` and prompt 08.

## 6b. Ontology review
Before a gap assessment, the bot compares `ontology/LAST_UPDATE` on git `main` and refreshes `ontology/` when that date is newer. It then messages you in bot chat with **Core (from git)** and **Candidate (from messages)**. Nothing is applied until you agree or suggest a tweak. A git pull request for a core candidate happens only if you ask. See `docs/ONTOLOGY-LAYERS.md`.

## 7. Alerts (optional)
- **Critical** — ping me now (priority person posts, someone names me, an ask matches my interests).
- **Digest** — a daily or weekly roundup for everything else.
- Start from `examples/notification_config.example.json`; your real copy is private.

## 8. Safety & etiquette
- Your archive is personal. Don't share or republish others' messages or media.
- The bot never posts in the group.
- Don't commit your store, export, or private config to git (the `.gitignore` helps).

## 9. Troubleshooting
| Problem | Fix |
|---|---|
| QR timed out | Ask for a fresh QR and scan within ~20 seconds |
| "store locked" | Another sync is running. Stop the follow, do the write (backfill/media), then restart follow |
| `doctor` says locked | Normal while follow is running |
| Media "unavailable" | WhatsApp no longer has it; it stays marked unavailable, not an error |
| Empty dashboard | Check the date slider covers your messages |

## First-run status (ask your bot to update)
- [ ] wacli installed
- [ ] Store folder created
- [ ] Phone paired as linked device
- [ ] Group selected
- [ ] History backfilled
- [ ] Media downloaded
- [ ] Follow sync running
- [ ] Topics loaded
- [ ] Dashboard Page built
- [ ] Read-only rule saved
- [ ] Alerts configured (optional)
