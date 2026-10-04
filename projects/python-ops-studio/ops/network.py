"""Deterministic VLSM planning and read-only configuration auditing."""
import difflib,ipaddress,math,re
def plan(data):
    base=ipaddress.ip_network(data.get('network',''),strict=True)
    if base.version!=4 or not 8<=base.prefixlen<=30 or not any(base.subnet_of(ipaddress.ip_network(cidr)) for cidr in ['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']):raise ValueError('Use an RFC1918 IPv4 network between /8 and /30.')
    vlans=data.get('vlans',[])
    if not isinstance(vlans,list) or not 1<=len(vlans)<=64:raise ValueError('Provide 1–64 VLANs.')
    seen=set();requests=[]
    for row in vlans:
        vid=row.get('id');hosts=row.get('hosts');name=row.get('name','')
        if type(vid)!=int or not 1<=vid<=4094 or vid in seen:raise ValueError('VLAN IDs must be unique integers 1–4094.')
        if type(hosts)!=int or not 1<=hosts<=65533:raise ValueError('Host counts must be integers 1–65533.')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,31}',name):raise ValueError('VLAN names must use letters, digits, underscore or hyphen.')
        seen.add(vid)
        # One gateway, requested client addresses, network and broadcast.
        size=2**math.ceil(math.log2(hosts+3));requests.append((size,vid,name,hosts))
    cursor=int(base.network_address);allocated=[];commands=['! Review interface names and routing before applying.']
    for size,vid,name,hosts in sorted(requests,reverse=True):
        cursor=((cursor+size-1)//size)*size
        subnet=ipaddress.ip_network((cursor,32-int(math.log2(size))))
        if not subnet.subnet_of(base):raise ValueError('Requested VLANs do not fit inside the parent network.')
        gateway=str(subnet.network_address+1)
        allocated.append(dict(vlan=vid,name=name,network=str(subnet),gateway=gateway,client_start=str(subnet.network_address+2),client_end=str(subnet.broadcast_address-1),client_capacity=size-3,requested=hosts))
        commands.extend([f'vlan {vid}',f' name {name}',f'interface GigabitEthernet0/0.{vid}',f' encapsulation dot1Q {vid}',f' ip address {gateway} {subnet.netmask}'])
        cursor+=size
    return {'parent':str(base),'vlans':allocated,'allocated_addresses':sum(x[0] for x in requests),'total_addresses':base.num_addresses,'configuration':'\n'.join(commands),'configuration_note':'VLAN commands are for a switch; subinterfaces are for the router. Split by device and review before use.'}
def redact(config):
    return '\n'.join('[REDACTED credential line]' if re.search(r'(?i)\b(secret|password|community|private-key|pre-shared-key)\b',line) else line for line in config.splitlines())
def audit(data):
    before=data.get('baseline','');after=data.get('candidate','')
    if not all(isinstance(x,str) and len(x)<=200000 for x in [before,after]):raise ValueError('Configuration text must be under 200 KB.')
    rules=[('SSH enabled',r'(?im)^\s*ip ssh version 2\s*$'),('Timestamped logs',r'(?im)^\s*service timestamps log datetime'),('AAA configured',r'(?im)^\s*aaa new-model\s*$'),('Remote logging',r'(?im)^\s*logging (host )?\d')]
    checks=[{'rule':name,'passed':bool(re.search(pattern,after))} for name,pattern in rules]
    checks.append({'rule':'No explicit Telnet input','passed':not bool(re.search(r'(?im)^\s*transport input.*\b(telnet|all)\b',after))})
    changes=list(difflib.unified_diff(redact(before).splitlines(),redact(after).splitlines(),fromfile='baseline',tofile='candidate',lineterm=''))
    return {'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'diff':'\n'.join(changes),'note':'Checks cover a small Cisco IOS baseline, not complete device security. Credentials are redacted before diffing.'}
