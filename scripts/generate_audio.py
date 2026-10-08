"""Generate word audio once at build time; the shipped app never uses a TTS service."""
import asyncio, hashlib, json, sys
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'content/catalog.json'
OUT=ROOT/'www/audio'
OUT.mkdir(parents=True,exist_ok=True)
VOICES={'en':'en-GB-SoniaNeural','zh':'zh-CN-XiaoxiaoNeural'}
words=json.loads(CATALOG.read_text(encoding='utf-8'))['words']
completed=0
manifest={}
existing=ROOT/'content/audio-manifest.json'
if existing.exists():manifest=json.loads(existing.read_text(encoding='utf-8'))
lock=asyncio.Semaphore(5)

async def generate(w):
    global completed
    id=w['id'];voice=VOICES[w['lang']]
    checksum=hashlib.sha256((voice+'|'+w['text']).encode()).hexdigest()
    path=OUT/(id+'.mp3')
    if path.exists() and path.stat().st_size>2000 and manifest.get(id,{}).get('textHash')==checksum:
        completed+=1;return
    async with lock:
        for attempt in range(5):
            try:
                tmp=path.with_suffix('.tmp')
                await asyncio.wait_for(edge_tts.Communicate(w['text'],voice,rate='-8%').save(str(tmp)),45)
                if tmp.stat().st_size<2000:raise ValueError('Audio too short')
                tmp.replace(path)
                manifest[id]={'text':w['text'],'voice':voice,'textHash':checksum,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
                existing.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
                completed+=1
                if completed%25==0:print(f'Audio: {completed}/{len(words)}',flush=True)
                return
            except Exception as error:
                if attempt==4:raise RuntimeError(f'Failed to generate {id} ({w["text"]}): {error}') from error
                await asyncio.sleep(2+attempt*3)

async def main():
    await asyncio.gather(*(generate(w) for w in words))
    print(f'All {len(words)} word recordings ready. {sum(p.stat().st_size for p in OUT.glob("*.mp3"))/1048576:.1f} MiB.',flush=True)

asyncio.run(main())
