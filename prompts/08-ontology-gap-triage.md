# 08 — Ontology gap triage (personal vs core)

Paste into your bot (any time, or let the gap watch run it):

> Review recent messages that didn't fit any topic, plus any terms I've asked about. Follow `docs/ONTOLOGY-LAYERS.md` in the git repo `avilesg/message-dashboard-kit`:
> 0. **Freshness first:** fetch `ontology/LAST_UPDATE` from git `main`. If it is newer than the copy I last used (or I have none), re-fetch the whole `ontology/` folder from `main` before assessing gaps. Note any topics/aliases that are new in core.
> 1. For each gap decide **personal** (specific to my group, people, slang, priorities) or **core candidate** (generic, no private details). Default to personal when unsure. If it duplicates a core topic, treat it as an alias.
> 2. If `ontology_review.notify_in_bot_chat` is on in my notification config, message me in bot chat with two labeled sections: **Core (from git)** — new shared topics from `main`; **Candidate (from messages)** — new topics spotted in messages, each with your personal vs core-candidate recommendation. Ask me to **agree** or **suggest a tweak** for each.
> 3. Do not apply anything until I agree (`require_owner_agree_before_apply`). After I agree (with tweaks): add personal items to my personal extension (`custom_topics` / `topic_aliases` / `topic_weights` / `keywords`) and re-run classification; for core candidates show a draft proposal (label, aliases, parent, relationships, anonymized examples) and only open a PR to the git repo if I explicitly say so.
> 4. Summarize what changed and remind me to refresh my prefs backup (prompt 07).
