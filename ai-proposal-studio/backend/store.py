import json, sqlite3, uuid
from contextlib import closing
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/"data"/"studio.sqlite3"
def connection():
 DB.parent.mkdir(exist_ok=True)
 c=sqlite3.connect(DB)
 c.execute("CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
 c.execute("CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
 return c
def put(kind, payload, ident=None):
 if kind not in {"documents","proposals"}: raise ValueError("Invalid collection")
 ident=ident or str(uuid.uuid4())
 with closing(connection()) as c:
  c.execute(f"INSERT OR REPLACE INTO {kind} VALUES (?,?)",(ident,json.dumps(payload,ensure_ascii=False)))
  c.commit()
 return ident
def get(kind, ident):
 if kind not in {"documents","proposals"}: raise ValueError("Invalid collection")
 with closing(connection()) as c: row=c.execute(f"SELECT payload FROM {kind} WHERE id=?",(ident,)).fetchone()
 return json.loads(row[0]) if row else None
