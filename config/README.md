# Personal config (local only)

**Using Grok Bot only?** Skip this folder. Your bot keeps your group ID, name, and watchlist in its own memory / your Page.

**Comfortable with git and want everything on your own machine?**
1. Clone the repo.
2. `cp config/personal.example.json config/personal.json` and fill in your group JID, wacli store path, label for yourself, and any priority people.
3. Optional: `cp examples/notification_config.example.json config/notification_config.local.json` and edit.
4. Run scripts — they read `config/personal.json` automatically:
   ```
   python scripts/classify_store.py --out out/classification_summary.local.json
   python scripts/build_roster.py --out out/roster.local.json
   python scripts/build_messages_embed.py --days 30 --out out/messages_embed.local.json
   ```

`personal.json`, `*.local.json`, `out/`, and stores are all gitignored. Check `git status` before any commit.
