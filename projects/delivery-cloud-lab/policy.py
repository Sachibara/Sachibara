"""Small policy checker for Terraform plan JSON. Does not run Terraform or contact AWS."""
import argparse,json
from pathlib import Path
def review(plan):
    changes=plan.get('resource_changes')
    if not isinstance(changes,list):raise ValueError('Expected terraform show -json output with resource_changes.')
    findings=[];evaluated=0
    for resource in changes:
        after=resource.get('change',{}).get('after')
        if not isinstance(after,dict):continue
        evaluated+=1;kind=resource.get('type');address=resource.get('address','unknown')
        def add(rule):findings.append({'resource':address,'severity':'high','rule':rule})
        if kind=='aws_s3_bucket_public_access_block' and any(after.get(key) is not True for key in ['block_public_acls','block_public_policy','ignore_public_acls','restrict_public_buckets']):add('S3 public access blocking must have all four controls explicitly enabled.')
        if kind=='aws_instance' and after.get('associate_public_ip_address') is True:add('Instance explicitly receives a public IP.')
        if kind=='aws_security_group':
            for rule in after.get('ingress') or []:
                public=any(x in ['0.0.0.0/0','::/0'] for x in (rule.get('cidr_blocks') or [])+(rule.get('ipv6_cidr_blocks') or []))
                if public and (str(rule.get('protocol'))=='-1' or any((rule.get('from_port') or 0)<=port<=(rule.get('to_port') or 0) for port in [22,3389])):add('Internet-wide access to all protocols, SSH or RDP.')
    return {'evaluated':evaluated,'findings':findings,'scope':'Three focused AWS checks, not a complete infrastructure security assessment.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('plan');args=parser.parse_args()
    result=review(json.loads(Path(args.plan).read_text()));print(json.dumps(result,indent=2));raise SystemExit(1 if result['findings'] else 0)
