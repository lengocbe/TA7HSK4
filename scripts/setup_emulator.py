"""Prepare a headless Android test device, kept outside the delivery artifacts."""
from pathlib import Path
import urllib.request, zipfile, concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
SDK=ROOT/'tools/android-sdk'
def fetch(url):
    name=url.rsplit('/',1)[-1]
    archive=ROOT/'tools'/name
    if not archive.exists():urllib.request.urlretrieve(url,archive)
    with zipfile.ZipFile(archive) as z:z.extractall(SDK)
    print('Emulator component ready:',name,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(fetch,['https://dl.google.com/android/repository/emulator-windows_x64-16489710.zip','https://dl.google.com/android/repository/sys-img/android/x86_64-28_r04.zip']))
