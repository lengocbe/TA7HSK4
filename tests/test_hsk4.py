"""Textbook coverage, stable old IDs, separate courses and backup migration."""
from pathlib import Path
import json,sys,zipfile
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.1.0.apk') as previous:
 old=json.loads(previous.read('assets/www/data.js').decode('utf-8').removeprefix('const DATA = ').strip().removesuffix(';'))
byid={w['id']:w for w in data['words']}
for w in old['words']:assert byid[w['id']]==w,w['id']
new=[w for w in data['words'] if w.get('course') in ['4.1','4.2']]
assert len(new)==620
counts=[32,30,31,31,31,31,33,29,31,30,30,32,32,32,31,31,29,32,32,30]
for n,count in enumerate(counts,1):
 ws=[w for w in new if w['lesson']==f'zh4-u{n}']
 assert len(ws)==count
 assert [w['bookNumber'] for w in ws]==list(range(1,count+1))
 assert all(w['sourcePage'] and w['examplePages'] and w['exampleKind']=='excerpt' for w in ws)
 for w in ws:
  variants=[w['text']]+w.get('alternatives',[])
  assert any(v in w['example'] for v in variants),(w['id'],w['text'],w['example'])
assert byid['zh4-17-09']['pron']=='gàn'
assert byid['zh4-17-15']['text']=='入口'
assert byid['zh4-20-08']['text']=='怪'
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(viewport={'width':390,'height':844})
 context.add_init_script('''window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}};''')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'www/index.html').as_uri())
 page.locator('[data-action="open-language"][data-lang="zh"]').click()
 assert page.locator('.lesson').count()==10
 for book,count in [('4.1',309),('4.2',311),('legacy',150)]:
  page.locator(f'[data-action="hsk-book"][data-book="{book}"]').click()
  assert page.evaluate('WORDS.filter(inCourse).length')==count
  assert page.locator('.lesson').count()==10
  assert page.locator('[data-section="tests"]').count()==(1 if book=='legacy' else 0)
 page.locator('[data-action="hsk-book"][data-book="4.2"]').click()
 page.screenshot(path=str(ROOT/'output/screenshots/10-hsk4-textbooks.png'),full_page=True)
 page.locator('[data-action="lesson"][data-id="zh4-u17"]').click()
 assert page.locator('.word-row').count()==29
 page.evaluate("page='detail';currentWord='zh4-17-09';render()")
 page.evaluate("page='detail';currentWord='zh4-09-03';render()")
 assert page.get_by_text('Cách đọc trong cụm 得少吃 (phải ăn ít hơn)').count()==1
 page.locator('[data-action="audio"]').click()
 assert page.evaluate('audioCalls.at(-1).id')=='zh4-09-03'
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  page.evaluate("page='library';lang='zh';hskLevel=4;hskBook='4.2';render()")
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),width
  page.evaluate('state.settings.dark=true;render()')
 # Restore a v1.1 backup with old progress and a previous HSK5 lesson.
 backup={'schema':1,'progress':{'zh5-01-01':{'due':1,'interval':4,'reps':3,'lapses':0},'zh-01-01':{'due':1,'interval':2,'reps':1,'lapses':0}},'favorites':['zh5-01-01'],'last':{'zh':'zh5-u1'},'lastCourses':{'4':'zh-t1','5':'zh5-u1'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
 page.evaluate('(s)=>localStorage.setItem("test-state",JSON.stringify(s))',backup);page.reload()
 assert page.evaluate("state.progress['zh5-01-01'].reps")==3
 assert page.evaluate("state.lastCourses[5]")=='zh5-u1'
 page.evaluate("state.progress['zh4-01-01']={due:1,reps:1,interval:2,lapses:0};state.progress['zh4-11-01']={due:1,reps:1,interval:2,lapses:0}")
 assert page.evaluate("dueWords('zh',4,'4.1').map(w=>w.id)")==['zh4-01-01']
 assert page.evaluate("dueWords('zh',4,'4.2').map(w=>w.id)")==['zh4-11-01']
 assert page.evaluate("dueWords('zh',4,'legacy').map(w=>w.id)")==['zh-01-01']
 assert page.evaluate("makeOptions(WORDS.find(w=>w.id==='zh4-01-01')).every(w=>w.course==='4.1')")
 page.evaluate("openLesson('zh4-u11')")
 assert page.evaluate("state.lastCourses['4.2']")=='zh4-u11'
 page.reload()
 assert page.evaluate("state.lastCourses['4.2']")=='zh4-u11'
 browser.close()
assert not errors,errors
(ROOT/'output/hsk4-test-report.json').write_text(json.dumps({'result':'passed','addedWords':620,'book4.1':309,'book4.2':311,'lessons':20,'previousWordsPreserved':1137,'checks':['textbook numbering and excerpts','course separation','old backup migration','independent due queues','course choices','narrow and dark layouts'],'limitation':'Browser with simulated Android bridge; actual device not tested.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('HSK4 textbook and migration checks passed.')
