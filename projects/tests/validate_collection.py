"""Dependency-free structural checks. These do not replace framework builds."""
from pathlib import Path
import ast,json,re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
names=['react-incident-board','dotnet-angular-assets','laravel-vue-expenses','php-service-booking','ruby-change-api','codeigniter-maintenance','wordpress-support-library','shopify-tech-collection','servicenow-change-governance']
for name in names:
    p=root/name
    assert (p/'README.md').is_file(),name
    assert len(list(p.rglob('*')))>=2,name
for f in root.rglob('*.json'):json.loads(f.read_text())
for f in root.rglob('*.py'):ast.parse(f.read_text(),filename=str(f))
for f in root.rglob('*.csproj'):ET.parse(f)
liquid=(root/'shopify-tech-collection/sections/tech-collection.liquid').read_text()
schema=json.loads(re.search(r'{% schema %}(.*?){% endschema %}',liquid,re.S).group(1))
ids=[s['id'] for s in schema['settings']];assert len(ids)==len(set(ids))
assert "{% form 'product', product, id: form_id %}" in liquid
for f in root.rglob('*'):
    if f.is_file() and '.git' not in f.parts:
        assert f.name not in ['.env','credentials.json'],f
print('9 project guides; JSON/Python/XML; Shopify schema/IDs; source hygiene: passed.')
