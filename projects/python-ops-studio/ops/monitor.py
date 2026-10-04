import json,os,time,urllib.request
from datetime import datetime,timezone
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None
def probe(targets=None):
    targets=targets if targets is not None else json.loads(os.environ.get('OPS_MONITOR_TARGETS','{"Ops Studio":"http://127.0.0.1:8090/api/health"}'))
    if not isinstance(targets,dict) or len(targets)>10:raise ValueError('Configure at most 10 monitoring targets.')
    results=[]
    for name,url in targets.items():
        if not isinstance(url,str) or not url.startswith(('http://','https://')):raise ValueError('Monitor targets must use HTTP or HTTPS.')
        started=time.monotonic();status=None;error=None
        try:
            with urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url,method='GET'),timeout=3) as response:status=response.status;response.read(1024)
        except Exception as exc:error=type(exc).__name__
        results.append({'name':name,'up':status is not None and 200<=status<400,'status':status,'latency_ms':round((time.monotonic()-started)*1000,1),'error':error,'checked_at':datetime.now(timezone.utc).isoformat()})
    return {'targets':results,'note':'An on-demand snapshot, not an uptime SLA. URLs are configured by the operator in OPS_MONITOR_TARGETS.'}
