# 07 — Back up custom config (preferences only)

```
Write or update config/custom.json from what you remember about my setup: preferences and configuration settings only (group label and JID, timezone, store path, priority people, keywords, custom topics, relationship/topic weights if any, alert and digest settings, notification config pointers), using config/custom.example.json as the shape. If config/custom.json does not exist yet and config/personal.json does, read personal.json and write the updated settings to config/custom.json. Scripts still read personal.json when custom.json is missing. Do NOT include any WhatsApp messages, message store data, or media. Keep it gitignored and never commit it to the public repo. Then give me a downloadable copy named custom-config-backup-YYYY-MM-DD.json and tell me what changed since the last backup. Do not change the send lock: wacli stays read-only.
```

Repeat after any change to people, keywords, weights, or alerts. This does not back up messages; if those are critical, set up a separate, optional message-store backup. Older exports may be named `personal-config-backup-YYYY-MM-DD.json`; they are the same prefs file. See `config/BACKUP.md`.
