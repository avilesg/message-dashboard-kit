"""Shared helpers for the kit scripts. Read-only access to a wacli SQLite store."""
import json, os, re, sqlite3

PH_JID = "YOUR_GROUP_JID@g.us"

def load_personal(path=None):
    """Optional local config (config/personal.json). Never committed."""
    here = os.path.dirname(os.path.abspath(__file__))
    for p in [path, os.path.join(here, "..", "config", "personal.json")]:
        if p and os.path.exists(p):
            return json.load(open(p))
    return {}

def add_common_args(ap):
    ap.add_argument("--config", help="Path to personal.json (default: config/personal.json if present)")
    ap.add_argument("--db", help="Path to wacli.db (or set store_path in personal.json)")
    ap.add_argument("--chat-jid", help="Group JID, e.g. %s" % PH_JID)
    ap.add_argument("--self-label", help='Label for your own messages (default "You")')
    return ap

def resolve(args):
    cfg = load_personal(getattr(args, "config", None))
    args.db = args.db or cfg.get("store_path") or os.environ.get("WACLI_DB")
    args.chat_jid = args.chat_jid or cfg.get("chat_jid") or os.environ.get("CHAT_JID")
    args.self_label = args.self_label or cfg.get("self_label") or "You"
    if not args.db or not args.chat_jid or args.chat_jid == PH_JID:
        raise SystemExit("Need --db and --chat-jid (or config/personal.json).")
    return cfg

def connect(db):
    return sqlite3.connect("file:%s?mode=ro" % db, uri=True)

def clean_name(n):
    return (n or "").strip("~ \u202f")

REA = re.compile(r"\b(real estate|listing|buyer'?s?|seller'?s?|title|insurance|leasing)\s+agents?\b", re.I)

def load_topics(path):
    """Returns (pats, labels, shape, domain_labels) in file order.
    Domain 'tech_ai' uses strict word boundaries; others allow prefix stems."""
    T = json.load(open(path))
    pats, labels, shape, dl = [], [], [], []
    for D in T["domains"]:
        dl.append(D["label"]); shape.append(len(D["topics"]))
        strict = D.get("strict") or D["id"] == "tech_ai"
        for t in D["topics"]:
            ps = [re.compile(r"\b" + re.escape(k.strip()) + (r"\b" if strict else ""), re.I)
                  for k in t.get("keywords", []) if k.strip()]
            pats.append((t["id"], ps)); labels.append(t["label"])
    return pats, labels, shape, dl

def tag_text(text, media_type, pats, labels):
    o = []
    for j, (tid, ps) in enumerate(pats):
        tt = REA.sub(" ", text) if tid == "agents_automation" else text
        if any(p.search(tt) for p in ps):
            o.append(j)
    if media_type and (len(text.strip()) < 8 or re.fullmatch(r"Sent \w+", text.strip())):
        if "Media-only / low text" in labels:
            o.append(labels.index("Media-only / low text"))
    return o
