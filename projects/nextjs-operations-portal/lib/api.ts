import 'server-only';
export async function backend(path:string,token?:string,method='GET',body?:string){return fetch((process.env.NODE_API_URL||'http://127.0.0.1:5081').replace(/\/$/,'')+'/api'+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},body,cache:'no-store',signal:AbortSignal.timeout(10000)});}
