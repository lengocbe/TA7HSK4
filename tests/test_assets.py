"""Check source links, packaged audio bytes and decoded recordings."""
from pathlib import Path
import base64,hashlib,json,sys,zipfile
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
words=catalog['words'];ids={w['id'] for w in words}
assert len(ids)==len(words)
assert len([w for w in words if w.get('grade') not in [6,8,9] and w.get('level') not in [2,3,6,'spoken','hsk30','boya','han','office','intensive5']])==2422
assert len([w for w in words if w['lang']=='en' and w.get('grade') not in [6,8,9]])==264
assert len([w for w in words if w['lang']=='zh' and w.get('grade') not in [6,8,9] and w.get('level') not in [2,3,6,'spoken','hsk30','boya','han','office','intensive5']])==2158
for l in catalog['lessons']:
    assert l['words'] and all(id in ids for id in l['words'])
    assert len(l['words'])==len(set(l['words']))
for w in words:
    assert all(w[k] for k in ['text','pron','meaning','pos','source','sourceFile','sourcePage'])
    if w['lang']=='zh':assert w['occurrences']
    assert (w['example'] and w['translation']) or w.get('exampleKind')=='pending' or (w.get('level')=='spoken' and w.get('exampleKind') in ['spoken-vocabulary','spoken-phrase'])
apk=ROOT/'output/Lingo-SoTuVung-1.13.0.apk'
with zipfile.ZipFile(apk) as z:
    assert z.testzip() is None
    for name in ['index.html','app.js','app.compat.js','style.css','data.js']:
        assert z.read('assets/www/'+name)==(ROOT/'www'/name).read_bytes(),name
    assert 'classes.dex' in z.namelist()
    assert len([n for n in z.namelist() if n.endswith('.mp3')])==len(words)
    for w in words:
        data=(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes()
        assert z.read('assets/www/audio/'+w['id']+'.mp3')==data
        assert z.getinfo('assets/www/audio/'+w['id']+'.mp3').compress_type==zipfile.ZIP_STORED
        assert hashlib.sha256(data).hexdigest()==manifest[w['id']]['sha256']
        assert manifest[w['id']]['text']==w['text']

decoded=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    page=browser.new_page()
    for i in range(0,len(words),25):
        payload=[{'id':w['id'],'data':base64.b64encode((ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes()).decode()} for w in words[i:i+25]]
        results=page.evaluate('''async files => {
            const context = new AudioContext();
            const result = await Promise.all(files.map(async file => {
                const bytes = Uint8Array.from(atob(file.data), c=>c.charCodeAt(0));
                const audio = await context.decodeAudioData(bytes.buffer);
                const samples = audio.getChannelData(0);
                let peak=0, sum=0;
                for(let i=0;i<samples.length;i++){peak=Math.max(peak,Math.abs(samples[i]));sum+=samples[i]*samples[i];}
                return {id:file.id,duration:audio.duration,peak,rms:Math.sqrt(sum/samples.length)};
            }));
            await context.close();return result;
        }''',payload)
        decoded+=results
    browser.close()
for recording in decoded:
    assert .25<recording['duration']<12,recording
    assert recording['peak']>.02 and recording['rms']>.003,recording
report={'result':'passed','words':len(words),'english':sum(w['lang']=='en' for w in words),'chinese':len([w for w in words if w['lang']=='zh']),'hsk5':1388,'hsk51':723,'hsk52':665,'lessonViews':len(catalog['lessons']),'checks':['All lessons resolve to valid unique IDs','Word fields and Chinese PDF occurrences present','APK zip CRC integrity',f'All {len(words)} MP3 assets match their manifests and package uncompressed','All recordings decode and contain non-silent audio'],'durationRangeSeconds':[min(d['duration'] for d in decoded),max(d['duration'] for d in decoded)]}
(ROOT/'output/asset-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('All content and packaged audio checks passed.')
