import json,os,sqlite3
from pathlib import Path
from . import network,security,data,knowledge,monitor
class Service:
    def __init__(self,path):
        self.path=str(path);Path(path).parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS tickets(id TEXT PRIMARY KEY,priority TEXT NOT NULL,opened_at TEXT NOT NULL,resolved_at TEXT);
            CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(title,body);
            CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,kind TEXT NOT NULL,result TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
    def db(self):
        db=sqlite3.connect(self.path,timeout=10);db.execute('PRAGMA journal_mode=WAL');return db
    def dispatch(self,method,path,payload):
        db=self.db()
        try:
            if method=='GET' and path=='/api/data/summary':return data.summary(db)
            if method=='GET' and path=='/api/data/export':return {'csv':data.csv_report(db)}
            if method=='GET' and path=='/api/documents':return {'documents':[{'id':r[0],'title':r[1]} for r in db.execute('SELECT rowid,title FROM documents ORDER BY rowid DESC LIMIT 100')]}
            if method=='GET' and path=='/api/history':return {'runs':[{'id':r[0],'kind':r[1],'created_at':r[2]} for r in db.execute('SELECT id,kind,created_at FROM runs ORDER BY id DESC LIMIT 30')]}
            if method!='POST':raise KeyError('Unknown route')
            routes={'/api/network/plan':network.plan,'/api/config/audit':network.audit,'/api/security/analyze':security.analyze,'/api/endpoints/check':security.endpoints,'/api/monitor/check':lambda _:monitor.probe(),'/api/data/import':lambda value:data.ingest(db,value.get('csv','')),'/api/documents/add':lambda value:knowledge.add_document(db,value),'/api/knowledge/ask':lambda value:knowledge.ask(db,value)}
            if path not in routes:raise KeyError('Unknown route')
            result=routes[path](payload)
            # Keep audit metadata only; logs, configurations and source excerpts are not copied into run history.
            with db:db.execute('INSERT INTO runs(kind,result) VALUES (?,?)',(path,json.dumps({'ok':True})))
            return result
        finally:db.close()
