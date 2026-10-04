import json,tempfile,threading,unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from ops.network import plan,audit
from ops.security import analyze,endpoints
from ops.service import Service
from server import make_server
class CoreTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.service=Service(Path(self.tmp.name)/'test.sqlite')
    def tearDown(self):self.tmp.cleanup()
    def test_vlsm_no_overlap_and_gateway_capacity(self):
        result=plan({'network':'10.0.0.0/24','vlans':[{'id':10,'name':'Staff','hosts':50},{'id':20,'name':'Guest','hosts':25}]})
        self.assertEqual(result['vlans'][0]['network'],'10.0.0.0/26');self.assertEqual(result['vlans'][1]['network'],'10.0.0.64/27');self.assertEqual(result['vlans'][0]['client_capacity'],61)
    def test_vlsm_rejects_overflow_duplicate_and_injection(self):
        for rows in [[{'id':1,'name':'Staff','hosts':100}],[{'id':1,'name':'Bad\ncommand','hosts':1}],[{'id':1,'name':'A','hosts':1},{'id':1,'name':'B','hosts':1}]]:
            with self.assertRaises(ValueError):plan({'network':'10.0.0.0/28','vlans':rows})
    def test_config_redacts_secrets_and_detects_telnet(self):
        result=audit({'baseline':'','candidate':'username bob secret sensitive\ntransport input telnet'})
        self.assertNotIn('sensitive',result['diff']);self.assertFalse(result['checks'][-1]['passed'])
    def test_log_window_and_success(self):
        logs=[{'timestamp':f'2026-10-01T12:0{i}:00Z','event':'login_failed' if i<5 else 'login_success','ip':'192.0.2.1','user':'demo'} for i in range(6)]
        result=analyze({'logs':'\n'.join(json.dumps(x) for x in logs)})
        self.assertEqual(len(result['alerts']),2);self.assertEqual(result['alerts'][-1]['severity'],'high')
        logs[-1]['timestamp']='2026-10-01T12:20:00Z';self.assertEqual(len(analyze({'logs':'\n'.join(json.dumps(x) for x in logs)})['alerts']),1)
    def test_malformed_log_rejected(self):self.assertEqual(len(analyze({'logs':'not json'})['rejected']),1)
    def test_endpoint_rules_and_staleness(self):
        row={'name':'PC','os':'Windows','disk_free_percent':5,'firewall_enabled':False,'observed_at':(datetime.now(timezone.utc)-timedelta(days=8)).isoformat()}
        self.assertEqual(len(endpoints({'devices':[row]})['devices'][0]['issues']),3)
    def test_data_upsert_and_reject(self):
        text='id,priority,opened_at,resolved_at\na,P1,2026-10-01T00:00:00Z,2026-10-01T02:00:00Z\nb,P2,invalid,\n'
        for _ in range(2):result=self.service.dispatch('POST','/api/data/import',{'csv':text})
        self.assertEqual(result['accepted'],1);self.assertEqual(len(result['rejected']),1);self.assertEqual(result['summary']['total'],1);self.assertEqual(result['summary']['groups'][0]['sla_percent'],100)
    def test_open_tickets_not_counted_as_resolved(self):
        result=self.service.dispatch('POST','/api/data/import',{'csv':'id,priority,opened_at,resolved_at\na,P1,2026-10-01T00:00:00Z,'})
        self.assertIsNone(result['summary']['groups'][0]['sla_percent'])
    def test_knowledge_sources_persist_and_no_match(self):
        self.service.dispatch('POST','/api/documents/add',{'title':'DNS guide','body':'Check DNS resolver settings before clearing the client cache.'})
        restarted=Service(self.service.path);result=restarted.dispatch('POST','/api/knowledge/ask',{'question':'DNS resolver'})
        self.assertEqual(result['sources'][0]['title'],'DNS guide');self.assertEqual(result['mode'],'retrieval')
        self.assertEqual(restarted.dispatch('POST','/api/knowledge/ask',{'question':'unrelated zebra'})['sources'],[])
class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.server,cls.token=make_server(port=0,db=Path(cls.tmp.name)/'http.sqlite',token='test-token');cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.base='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.tmp.cleanup()
    def request(self,path,body=None,token=None):
        req=Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers={'Authorization':'Bearer '+(token or ''),'Content-Type':'application/json'})
        try:
            with urlopen(req) as response:return response.status,response.read()
        except HTTPError as error:return error.code,error.read()
    def test_health_and_auth(self):
        self.assertEqual(self.request('/api/health')[0],200);self.assertEqual(self.request('/api/history')[0],401);self.assertEqual(self.request('/api/history',token=self.token)[0],200)
    def test_actual_network_api_and_bad_request(self):
        code,body=self.request('/api/network/plan',{'network':'10.1.0.0/24','vlans':[{'id':1,'name':'Clients','hosts':20}]},self.token)
        self.assertEqual(code,200);self.assertEqual(json.loads(body)['vlans'][0]['gateway'],'10.1.0.1')
        self.assertEqual(self.request('/api/network/plan',{'network':'bad'},self.token)[0],400)
    def test_static_allowlist(self):self.assertEqual(self.request('/')[0],200);self.assertEqual(self.request('/../server.py')[0],404)
if __name__=='__main__':unittest.main()
