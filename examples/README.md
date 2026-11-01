# Example alert config

Copy `notification_config.example.json` to `notification_config.json` (git-ignored) and edit it privately, or just tell your bot what you want and let it edit the file.

- `priority_people` — fake names here; put real people only in your private copy.
- `my_keywords` — empty on purpose. Your interests (markets, deal types, tools) are personal.
- `rules` — `critical` = message your bot chat right away; `digest_*` = a roundup on a schedule.
- `ontology_review` — bot-chat agree/tweak before applying shared topics from git `main` (**Core (from git)**) or topic candidates from messages (**Candidate (from messages)**). Detail is here; `config/personal.example.json` only points at it.
- `levels.ontology_gap` — meaning and delivery for that review (compare `ontology/LAST_UPDATE`, then wait for agree/tweak).
- Never commit your real copy.
