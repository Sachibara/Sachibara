"""Batch ETL companion for Ops Studio, producing CSV suitable for BI import."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'python-ops-studio'))
from ops.service import Service
def main():
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--database',default='data/tickets.sqlite');parser.add_argument('--output',default='data/summary.csv');args=parser.parse_args()
    service=Service(args.database);result=service.dispatch('POST','/api/data/import',{'csv':Path(args.input).read_text(encoding='utf-8-sig')})
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(service.dispatch('GET','/api/data/export',{})['csv']);print(json.dumps(result,indent=2));return 2 if result['rejected'] else 0
if __name__=='__main__':raise SystemExit(main())
