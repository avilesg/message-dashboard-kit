#!/usr/bin/env python3
"""Tag every message in one group chat with topics from the ontology; write summary JSON.
Example: python scripts/classify_store.py --db ~/wacli/wacli.db --chat-jid YOUR_GROUP_JID@g.us --out out/classification_summary.local.json
"""
import argparse, collections, datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

ap = add_common_args(argparse.ArgumentParser(description=__doc__))
here = os.path.dirname(os.path.abspath(__file__))
ap.add_argument("--topics", default=os.path.join(here, "..", "ontology", "topics.share.json"))
ap.add_argument("--out", default="classification_summary.local.json")
ap.add_argument("--top", type=int, default=15, help="Top N authors per topic")
a = ap.parse_args(); cfg = resolve(a)
G = a.chat_jid; c = connect(a.db)
rows = c.execute("select msg_id,sender_name,sender_jid,ts,coalesce(nullif(text,''),nullif(media_caption,''),nullif(display_text,''),''),"
                 "media_type,reaction_to_id,reaction_emoji,revoked,from_me from messages where chat_jid=? order by ts", (G,)).fetchall()
pats, labels, shape, dl = load_topics(a.topics)
cnt = collections.Counter(); who = collections.defaultdict(collections.Counter)
reacts = sysm = considered = tagged = assigns = 0
for r in rows:
    if r[6] or r[7]: reacts += 1; continue
    if r[2] == G and not r[9]: sysm += 1; continue
    considered += 1
    t = "" if r[8] else (r[4] or ""); t = "" if t == "(message)" else t
    name = a.self_label if r[9] else (clean_name(r[1]) or "Unnamed sender")
    o = tag_text(t, r[5], pats, labels)
    tagged += bool(o); assigns += len(o)
    for j in o: cnt[j] += 1; who[j][name] += 1
TN, k = [], 0
for n in shape: TN.append([cnt[k + i] for i in range(n)]); k += n
# Optional: per-topic counts for people you choose (personal.json priority_people; never commit names)
pp = cfg.get("priority_people", [])
CM, k = [], 0
for n in shape: CM.append([[who[k + i][p] for p in pp] for i in range(n)]); k += n
out = dict(version="kit-1", as_of=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
           total_rows=len(rows), reactions=reacts, system_rows=sysm, classified_msgs=considered,
           tagged_msgs=tagged, untagged=considered - tagged, tag_assignments=assigns,
           domains=dl, labels=labels, TOPIC_N=TN, priority_people=pp, CM=CM,
           top_authors={labels[j]: who[j].most_common(a.top) for j in cnt})
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
print({k: v for k, v in out.items() if k in ("total_rows", "classified_msgs", "tagged_msgs", "tag_assignments")}, "->", a.out)
