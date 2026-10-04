"""Download-free local HTTP server. Use asgi.py for FastAPI deployment."""
import argparse,hmac,json,os,secrets
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from ops.service import Service
ROOT=Path(__file__).parent
def make_server(host='127.0.0.1',port=8090,db=None,token=None):
    service=Service(db or os.environ.get('OPS_DB') or ROOT/'data/ops.sqlite');secret=token or os.environ.get('OPS_TOKEN') or secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def send(self,status,value,ctype='application/json'):
            raw=value.encode() if isinstance(value,str) else json.dumps(value).encode()
            self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'self'");self.end_headers();self.wfile.write(raw)
        def handle_request(self):
            path=urlsplit(self.path).path
            if self.command=='GET' and path=='/api/health':return self.send(200,{'status':'ok'})
            assets={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
            if self.command=='GET' and path in assets:
                file,ctype=assets[path];return self.send(200,(ROOT/'web'/file).read_text(),ctype)
            if not path.startswith('/api/'):return self.send(404,{'error':'Not found'})
            if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+secret):return self.send(401,{'error':'Enter the operator token printed by the server.'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if size<0 or size>1500000:return self.send(413,{'error':'Request exceeds 1.5 MB.'})
                if self.command=='POST' and self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'Use application/json.'})
                payload=json.loads(self.rfile.read(size)) if size else {}
                if not isinstance(payload,dict):raise ValueError('JSON body must be an object.')
                result=service.dispatch(self.command,path,payload);return self.send(200,result)
            except KeyError:return self.send(404,{'error':'Unknown route or missing required field.'})
            except (ValueError,TypeError,AttributeError) as exc:return self.send(400,{'error':str(exc)})
            except Exception:return self.send(500,{'error':'Internal error; review server configuration.'})
        do_GET=handle_request;do_POST=handle_request
        def log_message(self,*args):pass
    return ThreadingHTTPServer((host,port),Handler),secret
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8090);args=parser.parse_args()
    server,token=make_server(port=args.port);print(f'Ops Studio: http://127.0.0.1:{server.server_port}\nOperator token: {token}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
