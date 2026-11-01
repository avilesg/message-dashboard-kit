# 08 — Ontology gap triage (personal vs core)

Paste into your bot (any time, or let it run weekly):

> Review recent messages that didn't fit any topic, plus any terms I've asked about. For each gap, follow `docs/ONTOLOGY-LAYERS.md` in the message-dashboard kit:
> 1. Decide **personal** (specific to my group, people, slang, or priorities) or **core candidate** (generic and useful to most groups, no private details). Default to personal when unsure. If it duplicates an existing core topic, treat it as an alias.
> 2. Personal: add it to my personal extension (`custom_topics` / `topic_aliases` / `topic_weights` / `keywords`) and re-run classification.
> 3. Core candidate: show me a draft proposal (preferred label, aliases, parent area, relationships, anonymized examples). Keep it personal for now. Only open a PR to the kit if I explicitly say so.
> 4. Summarize what you changed, then remind me to refresh my prefs backup (prompt 07).
