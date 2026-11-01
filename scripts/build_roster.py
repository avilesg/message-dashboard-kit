#!/usr/bin/env python3
"""Phone roster for one group: everyone who posted or is a current participant.
first_seen approximates join date; 'Not in current list' approximates left/removed.
Example: python scripts/build_roster.py --db ~/wacli/wacli.db --chat-jid YOUR_GROUP_JID@g.us --out out/roster.local.json
"""
import argparse, collections, datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import *

ap = add_common_args(argparse.ArgumentParser(description=__doc__))
ap.add_argument("--out", default="roster.local.json")
a = ap.parse_args(); resolve(a)
G = a.chat_jid; c = connect(a.db)
part = {u: r for u, r in c.execute("select user_jid,role from group_participants where group_jid=?", (G,))}
con = {j: (fn or sn or bn or pn or "") for j, pn, fn, bn, sn in
       c.execute("select jid,push_name,full_name,business_name,system_name from contacts")}
try: alias = {j: x for j, x in c.execute("select jid,alias from contact_aliases")}
except Exception: alias = {}
new = lambda: dict(n=0, first=None, last=None, names=collections.Counter())
st = collections.defaultdict(new)
for sj, sn, ts, fm, rx in c.execute("select sender_jid,sender_name,ts,from_me,reaction_to_id from messages "
                                    "where chat_jid=? and sender_jid!=? and from_me=0", (G, G)):
    s = st[sj]; s["n"] += 0 if rx else 1
    s["first"] = ts if s["first"] is None else min(s["first"], ts)
    s["last"] = ts if s["last"] is None else max(s["last"], ts)
    if clean_name(sn): s["names"][clean_name(sn)] += 1
def phone(j):
    d = j.split("@")[0]
    if not d.isdigit(): return j.split("@")[0]
    if d.startswith("1") and len(d) == 11: return f"+1 ({d[1:4]}) {d[4:7]}-{d[7:]}"
    return "+" + d
D = lambda t: datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d") if t else ""
rows = []
for j in set(st) | set(part):
    s = st.get(j) or new()
    name = s["names"].most_common(1)[0][0] if s["names"] else ""; src = "message" if name else ""
    if not name and (alias.get(j) or con.get(j)): name = alias.get(j) or con.get(j); src = "contact"
    rows.append([name or "Unnamed", src, phone(j), s["n"], D(s["first"]), D(s["last"]),
                 "Member" if j in part else "Not in current list", part.get(j) or ""])
me = c.execute("select count(*),min(ts),max(ts) from messages where chat_jid=? and from_me=1 and reaction_to_id is null", (G,)).fetchone()
rows.append([a.self_label, "self", "(your number)", me[0], D(me[1]), D(me[2]), "Member", ""])
rows.sort(key=lambda r: -r[3])
un = [r for r in rows if r[0] == "Unnamed" and r[3] > 0]
summ = dict(people=len(rows), members_now=len(part), posted=sum(r[3] > 0 for r in rows),
            left_or_removed=sum(r[6] != "Member" for r in rows), unnamed_posting=len(un),
            unnamed_msgs=sum(r[3] for r in un), silent_members=sum(r[3] == 0 for r in rows))
json.dump(dict(summary=summ, cols=["name", "name_source", "phone", "msgs", "first_seen", "last_seen", "status", "role"], rows=rows),
          open(a.out, "w"), ensure_ascii=False)
print(summ, "->", a.out)
