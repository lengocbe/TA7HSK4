"""Full HSK 5.2 course, old APK migration and isolated textbook learning."""
from pathlib import Path
import json,zipfile,sys,hashlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.2.0.apk') as previous:
 old=json.loads(previous.read('assets/www/data.js').decode('utf-8').removeprefix('const DATA = ').strip().removesuffix(';'))
byid={w['id']:w for w in data['words']}
for w in old['words']:assert byid[w['id']]==w,w['id']
for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l,l['id']
new=[w for w in data['words'] if w.get('course')=='5.2']
assert len(new)==665 and len([w for w in data['words'] if w.get('level') not in [2,3,6,'spoken','hsk30','boya']])==2422
counts=[44,36,41,34,40,37,40,35,34,40,36,36,29,39,38,34,35,37]
for n,count in enumerate(counts,19):
 ws=[w for w in new if w['lesson']==f'zh5-u{n}'];assert len(ws)==count
 assert [w['bookNumber'] for w in ws]==list(range(1,count+1))
 for w in ws:
  assert w['sourceFile']=='Giáo trình chuẩn HSK5.2.pdf' and w['sourcePage']>0
  assert w['examplePages'] and w['translation'] and w['exampleKind'] in ['excerpt','title']
  assert any(v in w['example'] for v in [w['text']]+w.get('alternatives',[])+w.get('exampleForms',[])),w['id']
  assert all('\ufffd' not in v for v in w.values() if isinstance(v,str))
for id,pron in {'zh5-19-17':'yóu zhá','zh5-19-24':'báo','zh5-23-22':'xì','zh5-25-08':'cháo','zh5-26-06':'fǎn xǐng','zh5-30-12':'nián yú','zh5-34-25':'zhī gēng niǎo','zh5-35-25':'zhī gàn'}.items():assert byid[id]['pron']==pron
backup={'schema':1,'progress':{'zh5-01-01':{'due':1,'interval':4,'reps':3,'lapses':0},'zh4-01-01':{'due':1,'interval':2,'reps':1,'lapses':0}},'favorites':['zh5-01-01'],'last':{'zh':'zh5-u1'},'lastCourses':{'4':'zh-t1','5':'zh5-u1','4.1':'zh4-u1'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
 context.add_init_script('''window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}};''')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto((ROOT/'www/index.html').as_uri())
 # New install starts empty and both books can be selected.
 assert page.evaluate('Object.keys(state.progress).length')==0
 page.locator('[data-action="open-language"][data-lang="zh"]').click()
 page.locator('[data-action="hsk-level"][data-level="5"]').click()
 assert page.locator('.lesson').count()==18
 assert page.evaluate('WORDS.filter(inCourse).length')==723
 page.locator('[data-action="hsk-book"][data-book="5.2"]').click()
 assert page.locator('.lesson').count()==18
 assert page.evaluate('WORDS.filter(inCourse).length')==665
 page.screenshot(path=str(ROOT/'output/screenshots/12-hsk52-lessons.png'),full_page=True)
 page.locator('[data-action="lesson"][data-id="zh5-u19"]').click()
 assert page.locator('.word-row').count()==44
 page.evaluate("page='detail';currentWord='zh5-19-24';render()")
 assert 'báo' in page.locator('.pronunciation').inner_text()
 assert page.get_by_text('Cách đọc trong cụm 薄如白纸 (mỏng như giấy)').count()==1
 page.locator('[data-action="audio"]').click();assert page.evaluate('audioCalls.at(-1).id')=='zh5-19-24'
 page.screenshot(path=str(ROOT/'output/screenshots/13-hsk52-word.png'),full_page=True)
 page.evaluate("startStudy([BYID['zh5-19-01']], 'cards', 'Test')")
 page.locator('[data-action="reveal"]').click();page.locator('[data-action="rate"][data-rating="good"]').click()
 assert page.evaluate("state.progress['zh5-19-01'].reps")==1
 page.evaluate("startStudy([BYID['zh5-21-25']], 'typing', 'Test')")
 page.locator('#typed-answer').fill('繁体');page.locator('[data-action="check-typing"]').click()
 assert 'Chính xác' in page.locator('.feedback').inner_text()
 page.evaluate("startStudy([BYID['zh5-19-01']], 'listening', 'Test')")
 assert page.evaluate("study.options.every(w=>w.course==='5.2')")
 page.locator('[data-action="audio"]').click()
 page.locator('[data-action="answer"][data-id="zh5-19-01"]').click()
 assert 'Chính xác' in page.locator('.feedback').inner_text()
 # Restore version 1.2 backup and preserve the remembered books.
 page.evaluate('(s)=>localStorage.setItem("test-state",JSON.stringify(s))',backup);page.reload()
 assert page.evaluate("state.progress['zh5-01-01'].reps")==3
 assert page.evaluate("state.lastCourses[5]")=='zh5-u1'
 assert page.evaluate("state.lastCourses['4.1']")=='zh4-u1'
 page.evaluate("state.progress['zh5-19-01']={due:1,reps:1,interval:2,lapses:0};openLesson('zh5-u19')")
 assert page.evaluate("state.lastCourses['5.2']")=='zh5-u19'
 assert page.evaluate("dueWords('zh',5,'5.1').map(w=>w.id)")==['zh5-01-01']
 assert page.evaluate("dueWords('zh',5,'5.2').map(w=>w.id)")==['zh5-19-01']
 page.evaluate("page='stats';render()")
 page.locator('[data-action="review"][data-lang="zh"]').click()
 assert page.evaluate("study.queue.every(w=>w.course==='5.2')")
 page.locator('[data-action="exit-study"]').click()
 exported=page.evaluate('backup()');page.evaluate('state=defaults()')
 page.evaluate('(text)=>receiveBackup(text)',exported)
 assert page.evaluate("state.progress['zh5-19-01'].reps")==1
 assert page.evaluate("state.progress['zh5-01-01'].reps")==3
 page.reload();assert page.evaluate("state.lastCourses['5.2']")=='zh5-u19'
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for action in ["page='library';lang='zh';hskLevel=5;hsk5Book='5.2';render()","page='words';render()","page='stats';render()","page='detail';currentWord='zh5-21-22';render()"]:
   page.evaluate(action);assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(width,action)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("page='library';state.settings.dark=true;render()")
 page.screenshot(path=str(ROOT/'output/screenshots/14-hsk52-dark.png'),full_page=True)
 # Switching levels preserves each level's selected book.
 page.locator('[data-action="hsk-level"][data-level="4"]').click()
 page.locator('[data-action="hsk-book"][data-book="4.2"]').click()
 page.locator('[data-action="hsk-level"][data-level="5"]').click()
 assert page.evaluate('WORDS.filter(inCourse).length')==665
 page.locator('[data-action="hsk-book"][data-book="5.1"]').click()
 assert page.evaluate('WORDS.filter(inCourse).length')==723
 page.locator('[data-action="hsk-level"][data-level="4"]').click()
 assert page.evaluate('WORDS.filter(inCourse).length')==311
 assert not errors,errors
 browser.close()
report=dict(result='passed',addedWords=665,newLessons=18,oldWordsPreserved=1757,checks=['Exact lesson word numbering and source pages','Word fields and source excerpt coverage','New empty installation','Old APK records and backup migration','Separate textbook filters, choices, due queues and last lessons','Native audio bridge calls','Cards, listening quiz, typing and abbreviated forms','Backup round trip across books','Narrow and dark layouts'],limitation='Browser with simulated native bridge; physical Android device not tested.')
(ROOT/'output/hsk52-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('HSK 5.2 content, learning and upgrade migration checks passed.')
