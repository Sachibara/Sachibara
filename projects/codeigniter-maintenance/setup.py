from pathlib import Path
import shutil,subprocess
root=Path(__file__).resolve().parent; target=root/'runtime'
if target.exists(): raise SystemExit('runtime already exists; refusing to overwrite it.')
subprocess.run(['composer','create-project','codeigniter4/appstarter',str(target),'^4.7','--no-interaction'],check=True)
for f in (root/'overlay').rglob('*'):
    if f.is_file():
        out=target/f.relative_to(root/'overlay');out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out)
(target/'.env').write_text("CI_ENVIRONMENT = development\napp.baseURL = 'http://localhost:8082/'\ndatabase.default.DBDriver = SQLite3\ndatabase.default.database = '"+str(target/'writable/maintenance.sqlite').replace('\\','/')+"'\n")
subprocess.run(['php','spark','migrate'],cwd=target,check=True)
print('Ready: cd runtime and run php spark serve --host 127.0.0.1 --port 8082')
