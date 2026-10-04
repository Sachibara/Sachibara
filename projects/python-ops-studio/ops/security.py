"""Analyze supplied authentication logs; no network scanning."""
import ipaddress,json
from collections import defaultdict,deque
from datetime import datetime,timezone
def timestamp(value):
    if not isinstance(value,str):raise ValueError('Timestamp must be text.')
    dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    if dt.tzinfo is None:raise ValueError('Timestamp must include a UTC offset.')
    return dt.astimezone(timezone.utc)
def analyze(data):
    raw=data.get('logs','');threshold=data.get('threshold',5);window=data.get('window_seconds',300)
    if not isinstance(raw,str) or len(raw)>1000000:raise ValueError('Logs must be JSON Lines under 1 MB.')
    if type(threshold)!=int or not 2<=threshold<=100 or type(window)!=int or not 10<=window<=3600:raise ValueError('Invalid threshold or time window.')
    events=[];rejected=[]
    for n,line in enumerate(raw.splitlines(),1):
        if not line.strip():continue
        if n>5000:raise ValueError('Limit: 5000 log lines.')
        try:
            row=json.loads(line);dt=timestamp(row['timestamp']);ip=str(ipaddress.ip_address(row['ip']))
            if row.get('event') not in ['login_failed','login_success']:raise ValueError('Unsupported event.')
            if not isinstance(row.get('user'),str) or not 1<=len(row['user'])<=100:raise ValueError('Invalid user.')
            events.append((dt,ip,row['user'],row['event']))
        except (ValueError,KeyError,TypeError) as exc:rejected.append({'line':n,'error':str(exc)})
    buckets=defaultdict(deque);alerts=[];above=set()
    for dt,ip,user,event in sorted(events):
        bucket=buckets[ip]
        while bucket and (dt-bucket[0][0]).total_seconds()>window:bucket.popleft()
        if len(bucket)<threshold:above.discard(ip)
        if event=='login_failed':
            bucket.append((dt,user))
            if len(bucket)>=threshold and ip not in above:
                alerts.append({'rule':'Repeated authentication failures','severity':'medium','ip':ip,'timestamp':dt.isoformat(),'failures':len(bucket),'users':sorted({x[1] for x in bucket})});above.add(ip)
        elif len(bucket)>=threshold:
            alerts.append({'rule':'Success after repeated failures','severity':'high','ip':ip,'user':user,'timestamp':dt.isoformat(),'failures':len(bucket)})
            bucket.clear();above.discard(ip)
    return {'events':len(events),'rejected':rejected,'alerts':alerts,'note':'Threshold-based triage findings need investigation; they do not prove compromise.'}
def endpoints(data):
    devices=data.get('devices')
    if not isinstance(devices,list) or not 1<=len(devices)<=1000:raise ValueError('Supply 1–1000 device objects.')
    now=datetime.now(timezone.utc);results=[];names=set()
    for row in devices:
        name=row.get('name','');disk=row.get('disk_free_percent');firewall=row.get('firewall_enabled');observed=timestamp(row.get('observed_at'))
        if not isinstance(name,str) or not 1<=len(name)<=100 or name in names:raise ValueError('Device names must be unique nonempty text.')
        if type(disk) not in [float,int] or not 0<=disk<=100 or type(firewall)!=bool:raise ValueError('Disk must be 0–100 and firewall_enabled must be boolean.')
        age=(now-observed).total_seconds()/86400
        if age< -0.01:raise ValueError('Observation date is in the future.')
        names.add(name);issues=[]
        if not firewall:issues.append('One or more firewall profiles disabled')
        if disk<15:issues.append('Free system disk below 15%')
        if age>7:issues.append('Inventory older than 7 days')
        results.append({'name':name,'os':str(row.get('os','Unknown'))[:200],'disk_free_percent':disk,'firewall_enabled':firewall,'observed_at':observed.isoformat(),'issues':issues,'status':'Review' if issues else 'Baseline passed'})
    return {'devices':results,'review':sum(bool(x['issues']) for x in results),'total':len(results),'note':'This baseline checks reported firewall state, disk and inventory age. It does not assess patch completeness or antivirus health.'}
