"""FastAPI adapter sharing the same tested service layer."""
import hmac,json,os
from pathlib import Path
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse,FileResponse
from starlette.concurrency import run_in_threadpool
from ops.service import Service
ROOT=Path(__file__).parent
TOKEN=os.environ.get('OPS_TOKEN','')
if len(TOKEN)<32:raise RuntimeError('Set OPS_TOKEN to a random value of at least 32 characters.')
app=FastAPI(title='Sachibara Ops Studio',version='1.0.0');service=Service(ROOT/'data/ops.sqlite')
@app.get('/api/health')
def health():return {'status':'ok'}
@app.api_route('/api/{route:path}',methods=['GET','POST'])
async def api(route:str,request:Request):
    if not hmac.compare_digest(request.headers.get('authorization',''),'Bearer '+TOKEN):return JSONResponse({'error':'Unauthorized'},status_code=401)
    raw=bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw)>1500000:return JSONResponse({'error':'Request exceeds 1.5 MB.'},status_code=413)
    try:
        payload=json.loads(raw) if raw else {}
        if not isinstance(payload,dict):raise ValueError('JSON body must be an object.')
        return await run_in_threadpool(service.dispatch,request.method,'/api/'+route,payload)
    except KeyError:return JSONResponse({'error':'Unknown route or missing required field.'},status_code=404)
    except (ValueError,TypeError,AttributeError) as exc:return JSONResponse({'error':str(exc)},status_code=400)
@app.get('/')
def home():return FileResponse(ROOT/'web/index.html')
@app.get('/app.js')
def script():return FileResponse(ROOT/'web/app.js',media_type='text/javascript')
@app.get('/style.css')
def style():return FileResponse(ROOT/'web/style.css',media_type='text/css')
