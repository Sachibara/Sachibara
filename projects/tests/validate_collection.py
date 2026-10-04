"""Source structure checks; runtime/build tests are separate."""
from pathlib import Path
import ast,json,re,xml.etree.ElementTree as ET,os
root=Path(__file__).resolve().parents[1]
names=['react-incident-board','dotnet-angular-assets','laravel-vue-expenses','php-service-booking','ruby-change-api','codeigniter-maintenance','wordpress-support-library','shopify-tech-collection','servicenow-change-governance','python-ops-studio','node-operations-platform','java-inventory-service','mobile-service-desk','delivery-cloud-lab','endpoint-network-toolkit','qa-automation-lab','data-bi-starter','nextjs-operations-portal']
for name in names:assert (root/name/'README.md').is_file(),name
files=[]
for directory,dirs,filenames in os.walk(root):
    dirs[:]=[d for d in dirs if d not in ['node_modules','data','runtime','target','__pycache__','.next','test-results','playwright-report','.git']]
    files.extend(Path(directory)/name for name in filenames)
for f in files:
    if f.suffix=='.json':json.loads(f.read_text())
    if f.suffix=='.py':ast.parse(f.read_text(),filename=str(f))
    if f.name.endswith('.csproj') or f.name=='pom.xml':ET.parse(f)
liquid=(root/'shopify-tech-collection/sections/tech-collection.liquid').read_text();schema=json.loads(re.search(r'{% schema %}(.*?){% endschema %}',liquid,re.S).group(1));ids=[s['id'] for s in schema['settings']];assert len(ids)==len(set(ids))
print(f'{len(names)} project guides; JSON, Python, XML and Shopify schema checks passed.')
