"""Download a stable emulator using bounded, resumable HTTP ranges."""
from pathlib import Path
import concurrent.futures,urllib.request,zipfile,tempfile,shutil,time
ROOT=Path(__file__).resolve().parents[1]
url='https://dl.google.com/android/repository/emulator-windows_x64-11610631.zip'
with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':'bytes=0-0'}),timeout=30) as r:
    total=int(r.headers['Content-Range'].split('/')[-1])
folder=ROOT/'tools/stable-parts';folder.mkdir(exist_ok=True)
tasks=[(i,a,min(total-1,a+16*1024*1024-1)) for i,a in enumerate(range(0,total,16*1024*1024))]
def fetch(task):
    i,a,b=task;p=folder/str(i)
    for attempt in range(5):
        n=p.stat().st_size if p.exists() else 0
        if n==b-a+1:return p
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={a+n}-{b}'}),timeout=40) as r:
                if r.status!=206:raise ValueError('Range response required')
                with p.open('ab') as f:
                    while chunk:=r.read(65536):f.write(chunk)
            if p.stat().st_size!=b-a+1:raise ValueError('Incomplete range')
            print('Stable emulator part',i+1,'/',len(tasks),flush=True)
            return p
        except Exception:
            if attempt==4:raise
            time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:parts=list(pool.map(fetch,tasks))
archive=ROOT/'tools/emulator-windows_x64-11610631.zip'
with archive.open('wb') as out:
    for part in parts:
        with part.open('rb') as inp:shutil.copyfileobj(inp,out)
assert archive.stat().st_size==total
sdk=Path(tempfile.gettempdir())/'lingo-stable-emulator-sdk'
sdk.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:z.extractall(sdk)
previous=Path(tempfile.gettempdir())/'lingo-emulator-sdk'
shutil.copytree(previous/'system-images',sdk/'system-images',dirs_exist_ok=True)
shutil.copytree(previous/'platform-tools',sdk/'platform-tools',dirs_exist_ok=True)
shutil.copytree(ROOT/'tools/android-sdk/android-35',sdk/'platforms/android-35',dirs_exist_ok=True)
print('Stable emulator ready:',sdk,flush=True)
