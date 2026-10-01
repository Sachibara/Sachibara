"""Contract test against a running .NET API. Creates and deletes its own record."""
import json,sys,uuid
from urllib.request import Request,urlopen
from urllib.error import HTTPError
def call(base,path,method='GET',body=None):
    request=Request(base+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers={'Content-Type':'application/json'})
    try:
        with urlopen(request,timeout=10) as response: return response.status,json.loads(response.read() or 'null')
    except HTTPError as error: return error.code,json.loads(error.read() or 'null')
def test_assets(base):
    data={'tag':'TEST-'+uuid.uuid4().hex[:12],'name':'Smoke-test laptop','owner':'Test operator','status':'Available'}
    assert call(base,'/api/health')[0]==200
    assert call(base,'/api/assets','POST',{**data,'tag':''})[0]==400
    status,row=call(base,'/api/assets','POST',data);assert status==201,(status,row)
    path='/api/assets/'+str(row['id'])
    try:
        assert call(base,path)[0]==200
        assert call(base,'/api/assets','POST',data)[0]==409
        status,rows=call(base,'/api/assets');assert status==200 and any(x['id']==row['id'] for x in rows)
        assert call(base,path,'PUT',{**data,'status':'Unknown'})[0]==400
        status,updated=call(base,path,'PUT',{**data,'status':'Repair'});assert status==200 and updated['status']=='Repair'
    finally:
        assert call(base,path,'DELETE')[0]==204
    assert call(base,path,'DELETE')[0]==404
if __name__=='__main__':
    if len(sys.argv)!=3 or sys.argv[1]!='assets':raise SystemExit('Usage: python tests/api_smoke.py assets http://127.0.0.1:5080')
    test_assets(sys.argv[2].rstrip('/'));print('Asset CRUD/validation/duplicate contract passed.')
