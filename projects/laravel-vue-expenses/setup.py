from pathlib import Path
import shutil, subprocess
root=Path(__file__).resolve().parent
target=root/'runtime'
if target.exists(): raise SystemExit('runtime already exists; refusing to overwrite it.')
subprocess.run(['composer','create-project','laravel/laravel',str(target),'^12.0','--no-interaction'],check=True)
for f in (root/'overlay').rglob('*'):
    if f.is_file():
        out=target/f.relative_to(root/'overlay');out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out)
(target/'database/database.sqlite').touch(exist_ok=True)
env=target/'.env'
settings={'DB_CONNECTION':'sqlite','DB_DATABASE':str(target/'database/database.sqlite'),'SESSION_DRIVER':'file','CACHE_STORE':'file','QUEUE_CONNECTION':'sync'}
lines=env.read_text().splitlines()
for key,value in settings.items():
    lines=[line for line in lines if not line.startswith(key+'=')]
    lines.append(key+'="'+value.replace('\\','/')+'"')
env.write_text('\n'.join(lines)+'\n')
subprocess.run(['php','artisan','migrate','--force'],cwd=target,check=True)
print('Ready: cd runtime and run php artisan serve --host=127.0.0.1 --port=8000')
