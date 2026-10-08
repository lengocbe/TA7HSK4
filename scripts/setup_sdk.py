from pathlib import Path
import urllib.request, zipfile, concurrent.futures

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / 'tools' / 'android-sdk'
SDK.mkdir(parents=True, exist_ok=True)

def fetch(name):
    archive = ROOT / 'tools' / name
    if not archive.exists():
        urllib.request.urlretrieve('https://dl.google.com/android/repository/' + name, archive)
    with zipfile.ZipFile(archive) as z:
        z.extractall(SDK)
    print('Ready:', name, flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(fetch, ['platform-35_r02.zip', 'build-tools_r35_windows.zip', 'platform-tools_r37.0.1-win.zip']))
