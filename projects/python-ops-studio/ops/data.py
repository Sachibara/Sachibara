import csv,io,sqlite3
from .security import timestamp
SLA={'P1':4,'P2':24,'P3':72}
def ingest(db,text):
    if not isinstance(text,str) or len(text)>1000000:raise ValueError('CSV must be under 1 MB.')
    reader=csv.DictReader(io.StringIO(text))
    if set(reader.fieldnames or [])!=set(['id','priority','opened_at','resolved_at']):raise ValueError('Required CSV columns: id,priority,opened_at,resolved_at')
    accepted=[];rejected=[];seen=set()
    for line,row in enumerate(reader,2):
        if line>10001:raise ValueError('Limit: 10000 rows per import.')
        try:
            ident=row['id'].strip();priority=row['priority'].strip().upper();opened=timestamp(row['opened_at']);resolved=timestamp(row['resolved_at']) if row['resolved_at'] else None
            if not ident or len(ident)>100 or ident in seen:raise ValueError('Missing, oversized or duplicate ID in file.')
            if priority not in SLA:raise ValueError('Priority must be P1, P2 or P3.')
            if resolved and resolved<opened:raise ValueError('Resolution precedes opening.')
            seen.add(ident);accepted.append((ident,priority,opened.isoformat(),resolved.isoformat() if resolved else None))
        except (ValueError,TypeError,AttributeError) as exc:rejected.append({'line':line,'error':str(exc)})
    with db:
        db.executemany('INSERT INTO tickets VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET priority=excluded.priority,opened_at=excluded.opened_at,resolved_at=excluded.resolved_at',accepted)
    return {'accepted':len(accepted),'rejected':rejected,'summary':summary(db),'note':'Valid rows were upserted by ID; rejected rows were skipped.'}
def summary(db):
    rows=db.execute('SELECT id,priority,opened_at,resolved_at FROM tickets').fetchall();groups=[]
    for priority,target in SLA.items():
        selected=[r for r in rows if r[1]==priority];hours=[(timestamp(r[3])-timestamp(r[2])).total_seconds()/3600 for r in selected if r[3]]
        groups.append({'priority':priority,'total':len(selected),'resolved':len(hours),'open':len(selected)-len(hours),'average_resolution_hours':round(sum(hours)/len(hours),2) if hours else None,'sla_met':sum(h<=target for h in hours),'sla_target_hours':target,'sla_percent':round(100*sum(h<=target for h in hours)/len(hours),1) if hours else None})
    return {'total':len(rows),'groups':groups,'definition':'SLA percentage uses resolved tickets only; P1=4h, P2=24h, P3=72h. Open-ticket breaches are not included.'}
def csv_report(db):
    output=io.StringIO();fields=['priority','total','resolved','open','average_resolution_hours','sla_met','sla_target_hours','sla_percent'];writer=csv.DictWriter(output,fieldnames=fields);writer.writeheader();writer.writerows(summary(db)['groups']);return output.getvalue()
