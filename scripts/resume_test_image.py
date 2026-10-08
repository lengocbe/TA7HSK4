from pathlib import Path
import concurrent.futures, urllib.request, time, zipfile, shutil, tempfile
ROOT=Path(__file__).resolve().parents[1]
url='https://dl.google.com/android/repository/sys-img/android/x86_64-28_r04.zip'
total=564792723
archive=ROOT/'tools/x86_64-28_r04.zip'
start=archive.stat().st_size
parts=ROOT/'tools/image-parts';parts.mkdir(exist_ok=True)
ranges=[(i,a,min(total-1,a+16*1024*1024-1)) for i,a in enumerate(range(start,total,16*1024*1024))]
def fetch(task):
    i,a,b=task;p=parts/str(i)
    for attempt in range(5):
        n=p.stat().st_size if p.exists() else 0
        if n==b-a+1:return p
        try:
            req=urllib.request.Request(url,headers={'Range':f'bytes={a+n}-{b}'})
            with urllib.request.urlopen(req,timeout=45) as r:
                if r.status!=206:raise ValueError('Range response required')
                with p.open('ab') as f:
                    while True:
                        chunk=r.read(65536)
                        if not chunk:break
                        f.write(chunk)
            if p.stat().st_size!=b-a+1:raise ValueError('Incomplete range')
            print('Image part',i+1,'/',len(ranges),'ready',flush=True)
            return p
        except Exception:
            if attempt==4:raise
            time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:paths=list(pool.map(fetch,ranges))
with archive.open('ab') as out:
    for p in paths:
        with p.open('rb') as f:shutil.copyfileobj(f,out)
assert archive.stat().st_size==total
sdk=Path(tempfile.gettempdir())/'lingo-emulator-sdk'
sdk.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:z.extractall(sdk/'system-images/android-28/default')
shutil.copytree(ROOT/'tools/android-sdk/emulator',sdk/'emulator',dirs_exist_ok=True)
shutil.copytree(ROOT/'tools/android-sdk/platform-tools',sdk/'platform-tools',dirs_exist_ok=True)
print('Android test image ready at',sdk,flush=True)
