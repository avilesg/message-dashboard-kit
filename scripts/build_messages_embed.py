#!/usr/bin/env python3
"""Build the compact threads+topics embed a Message tracker Page reads.
Threads = quote chains (hard) + same-sender/name-ping follow-ups (soft).
Example: python scripts/build_messages_embed.py --db ~/wacli/wacli.db --chat-jid YOUR_GROUP_JID@g.us --days 30 --out out/messages_embed.local.json
Output contains message text: keep it local (gitignored)."""
import argparse,collections,datetime,json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from _common import *
ap=add_common_args(argparse.ArgumentParser(description=__doc__))
here=os.path.dirname(os.path.abspath(__file__))
ap.add_argument("--topics",default=os.path.join(here,"..","ontology","topics.share.json"))
ap.add_argument("--days",type=int,default=30,help="Threads active in last N days")
ap.add_argument("--trunc",type=int,default=280,help="Max chars per message")
ap.add_argument("--cap",type=int,default=12,help="Max replies per thread")
ap.add_argument("--exclude-newer",type=int,default=0,help="Skip threads active in last N days (for split embeds)")
ap.add_argument("--out",default="messages_embed.local.json")
a=ap.parse_args(); resolve(a)
DAYS,TRUNC,CAP,NEWER,OUT=a.days,a.trunc,a.cap,a.exclude_newer,a.out
G=a.chat_jid; c=connect(a.db)
rows=c.execute("select msg_id,sender_name,sender_jid,ts,coalesce(nullif(text,''),nullif(media_caption,''),nullif(display_text,''),''),media_type,quoted_msg_id,reaction_to_id,reaction_emoji,revoked,from_me from messages where chat_jid=? order by ts",(G,)).fetchall()
M={};reacts=collections.Counter()
for r in rows:
  if r[7] or r[8]: reacts[r[7]]+=1; continue
  M[r[0]]=dict(id=r[0],name=(a.self_label if r[10] else clean_name(r[1]) or 'Unnamed sender'),jid=r[2],ts=r[3],text=('(deleted)' if r[9] else r[4] or ''),mt=r[5],q=r[6])
def root(i):
  seen=0
  while M[i]['q'] and M[i]['q'] in M and seen<50: i=M[i]['q']; seen+=1
  return i
for i,m in M.items(): m['root']=root(i); m['link']='root' if m['root']==i else 'hard'
# soft links: unquoted, same sender within 3 min after own msg in a thread, or name ping in 10 min
lst=sorted(M.values(),key=lambda m:m['ts'])
last_by_sender={}; recent=[]
first=lambda n:n.split()[0].lower() if n and n[0].isalpha() else ''
for m in lst:
  if not m['q'] and m['link']=='root':
    p=last_by_sender.get(m['jid'])
    if p and m['ts']-p['ts']<=180 and p['root']!=p['id'] or (p and m['ts']-p['ts']<=180 and len(m['text'])>0 and M[p['root']].get('nrep',0)>=0 and p['q']):
      m['root']=p['root']; m['link']='soft'
    else:
      t=m['text'].strip().lower()
      for o in reversed(recent):
        if m['ts']-o['ts']>600: break
        f=first(o['name'])
        if o['jid']!=m['jid'] and len(f)>=3 and (t.startswith(f) or t.startswith('@'+f)):
          m['root']=o['root']; m['link']='soft'; break
  last_by_sender[m['jid']]=m; recent.append(m); recent=recent[-60:]
pats,labels,_,_=load_topics(a.topics)
def tags(m): return tag_text(m['text'],m['mt'],pats,labels)
cut=max(m['ts'] for m in lst)-DAYS*86400
th=collections.defaultdict(list)
for m in lst: th[m['root']].append(m)
cut2=max(m['ts'] for m in lst)-NEWER*86400 if NEWER else 1e12
keep=[r for r,ms in th.items() if any(x['ts']>=cut for x in ms) and not any(x['ts']>=cut2 for x in ms) and not (len(ms)==1 and (ms[0]['text'] in ('','(message)','(deleted)') or (ms[0]['mt'] and ms[0]['text'].startswith('Sent ')) ))]
MED={'image':'Image','video':'Video','document':'Document','audio':'Voice/audio','ptt':'Voice/audio','sticker':'Sticker','gif':'GIF'}
authors=[];ai={}
def A(n):
  if n not in ai: ai[n]=len(authors); authors.append(n)
  return ai[n]
base=min(min(x['ts'] for x in th[r]) for r in keep)
out=[];nmsg=0;nsoft=0
for r in keep:
  ms=th[r]; rt=M[r]
  hard=[x for x in ms if x['link']!='soft']; soft=[x for x in ms if x['link']=='soft'][:3]
  body=[rt]+sorted([x for x in hard if x['id']!=r],key=lambda x:x['ts'])
  extra=max(0,len(body)-1-CAP); body=body[:CAP+1]
  allm=sorted(body+soft,key=lambda x:x['ts']); allm.remove(rt); allm=[rt]+allm
  enc=[]
  for x in allm:
    tx=re.sub(r'\s+',' ',x['text']).strip(); tx='' if tx=='(message)' else tx; full=len(tx)
    if full>TRUNC: tx=tx[:TRUNC].rstrip()+'…'
    tg=tags(x)
    qi=-1
    if x['q']:
      for k,y in enumerate(allm):
        if y['id']==x['q']: qi=k;break
    enc.append([(x['ts']-base)//60,A(x['name']),tx,MED.get(x['mt'] or '',x['mt'] or ''),{'root':0,'hard':1,'soft':2}[x['link']],''.join(chr(48+j) for j in tg),qi,reacts.get(x['id'],0)])
    nmsg+=1; nsoft+=x['link']=='soft'
  last=max(x['ts'] for x in ms)
  out.append([(last-base)//60,len(hard)-1,extra,enc])
out.sort(key=lambda t:-t[0])
emb=dict(base=base,days=DAYS,authors=authors,threads=out,subtopics=labels)
s=json.dumps(emb,separators=(',',':'),ensure_ascii=False)
open(OUT,'w').write(s)
iso=lambda t:datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
print(len(s),'threads',len(out),'msgs',nmsg,'soft',nsoft,'span',iso(base),iso(max(m['ts'] for m in lst)),'cut',iso(cut))
