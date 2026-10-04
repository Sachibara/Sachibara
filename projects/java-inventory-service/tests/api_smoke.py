import base64,json,os,uuid
from urllib.request import Request,urlopen
from urllib.error import HTTPError
base=os.environ.get('JAVA_API_URL','http://127.0.0.1:8084')
auth='Basic '+base64.b64encode(('admin:'+os.environ['INVENTORY_ADMIN_PASSWORD']).encode()).decode()
def call(path,body=None,authenticated=True):
    headers={'Content-Type':'application/json'}
    if authenticated:headers['Authorization']=auth
    req=Request(base+'/api'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
    try:
        with urlopen(req,timeout=10) as response:return response.status,json.loads(response.read())
    except HTTPError as error:return error.code,json.loads(error.read() or '{}')
assert call('/products',authenticated=False)[0]==401
body={'sku':'TEST-'+uuid.uuid4().hex[:12],'name':'Test cable'}
status,row=call('/products',body);assert status==201,(status,row)
assert call('/products',body)[0]==409
path='/products/'+str(row['id'])
status,received=call(path+'/adjust',{'delta':10,'reason':'Test receipt','version':row['version']});assert status==200 and received['quantity']==10
assert call(path+'/adjust',{'delta':-11,'reason':'Invalid overdraw','version':received['version']})[0]==400
assert call(path+'/adjust',{'delta':1,'reason':'Stale request','version':row['version']})[0]==409
status,history=call(path+'/movements');assert status==200 and len(history)==1
print('Java API auth, duplicate SKU, stock receipt, underflow, stale version and audit passed.')
