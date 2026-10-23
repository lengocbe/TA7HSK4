"""HSK 6 content, legacy preservation and course-specific study/backup flows."""
from pathlib import Path
import json,zipfile,sys,hashlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.5.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode('utf-8').removeprefix('const DATA = ').strip().removesuffix(';'))
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes(),w['id']
 for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l
new=[w for w in data['words'] if w.get('level')==6]
assert len(new)==1963 and len([w for w in data['words'] if w.get('level') not in ['spoken','hsk30','boya']])==4868
assert len([l for l in data['lessons'] if l.get('level') not in ['spoken','hsk30','boya']])==170
audit={r['id']:r for r in json.loads((ROOT/'content/hsk6/source-audit.json').read_text(encoding='utf-8'))}
counts={c:sum(w['course']==c for w in new) for c in ['6.1','6.2']}
for c,start in [('6.1',1),('6.2',21)]:
 lessons=[l for l in data['lessons'] if l.get('course')==c];assert len(lessons)==20
 assert [l['number'] for l in lessons]==list(range(start,start+20))
 for l in lessons:
  ws=[byid[id] for id in l['words']];assert [w['bookNumber'] for w in ws]==list(range(1,len(ws)+1))
  for w in ws:
   assert w['course']==c and w['level']==6 and w['sourceFile']==f'Giáo trình chuẩn HSK{c}.pdf'
   assert all(w[k] for k in ['meaning','pron','example','examplePron','translation','sourcePage','examplePages'])
   assert w['exampleKind'] in ['excerpt','title']
   assert any(v in w['example'] for v in [w['text']]+w.get('exampleForms',[]))
   assert audit[w['id']]['source']['num']==w['bookNumber']
   assert audit[w['id']]['source']['page']==w['sourcePage']
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
for w in new:
 voice='zh-CN-XiaoxiaoNeural';spoken=w.get('speechText',w['text'])
 assert manifest[w['id']]['textHash']==hashlib.sha256((voice+'|'+w['text']+('|'+spoken if spoken!=w['text'] else '')).encode()).hexdigest()
backup={'schema':1,'progress':{'en-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-08'}},'mistakes':{'en-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['en-01-01'],'last':{'en':'en-u1','zh':'zh3-u20'},'lastCourses':{'3':'zh3-u20','5.2':'zh5-u19','4.1':'zh4-u1'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
 context.add_init_script("window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}}")
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto((ROOT/'www/index.html').as_uri());assert page.evaluate('Object.keys(state.progress).length')==0
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup)
 assert page.evaluate('state.mistakes')==backup['mistakes']
 page.locator('[data-action="open-language"][data-lang="zh"]').click()
 page.locator('[data-action="hsk-level"][data-level="6"]').click()
 for c,n in [('6.1',1),('6.2',21)]:
  page.locator(f'[data-action="hsk-book"][data-book="{c}"]').click()
  assert page.locator('[data-action="lesson"]').count()==20
  assert page.locator('[data-action="hsk-book"]').count()==2
  assert page.locator('[data-section="tests"]').count()==0
  assert page.evaluate('WORDS.filter(inCourse).length')==counts[c]
  page.screenshot(path=str(ROOT/f'output/screenshots/hsk{c}-lessons.png'),full_page=True)
  page.locator(f'[data-action="lesson"][data-id="zh6-u{n}"]').click()
  page.evaluate("startStudy(lessonWords(lessonId).slice(0,3),'meaning','Test','lesson')")
  assert page.evaluate('(c)=>study.options.every(w=>w.course===c)',c)
  first=page.evaluate('study.queue[0].id');page.evaluate("answerQuestion('wrong');answerQuestion('wrong')")
  assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index < study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[first]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click()
  assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
  page.locator('[data-action="open-mistakes"]').click();page.locator('[data-action="mistake-scope"][data-scope="zh"]').click()
  assert page.locator('.mistake-item').count()==1
  assert page.evaluate('(c)=>visibleMistakes().every(w=>w.course===c)',c)
  page.locator('[data-action="audio"]').first.click();assert page.evaluate('audioCalls.at(-1).id')==first
  page.locator('[data-action="master-mistake"]').click();assert page.locator('.mistake-item').count()==0
  assert page.evaluate('(id)=>state.mistakes[id].count===1&&state.mistakes[id].mastered',first)
  page.evaluate("(id)=>{startStudy([BYID[id]],'meaning','Test','lesson');answerQuestion('wrong')}",first)
  assert page.evaluate('(id)=>state.mistakes[id].count===2&&!state.mistakes[id].mastered',first)
  page.evaluate("page='library';render()")
 exported=page.evaluate('backup()');saved=page.evaluate('state');page.evaluate('state=defaults()');page.evaluate('(raw)=>receiveBackup(raw)',exported)
 assert page.evaluate('state')==saved
 page.reload();assert page.evaluate("state.lastCourses['6.1']")=='zh6-u1' and page.evaluate("state.lastCourses['6.2']")=='zh6-u21'
 assert page.evaluate("state.progress['en-01-01'].reps")==3 and page.evaluate("state.mistakes['en-01-01'].mastered")
 for c,n in [('6.1',1),('6.2',21)]:
  id=f'zh6-{n:02}-01'
  page.evaluate("(id)=>startStudy([BYID[id]],'typing','Test','lesson')",id)
  page.locator('#typed-answer').fill(byid[id]['text']);page.locator('[data-action="check-typing"]').click();assert page.evaluate('study.correct')==1
  page.evaluate("(id)=>startStudy([BYID[id]],'listening','Test','lesson')",id)
  assert page.evaluate('(c)=>study.options.every(w=>w.course===c)',c)
  page.evaluate("(id)=>{startStudy([BYID[id]],'cards','Test','lesson');study.reveal=true;render()}",id)
  assert page.locator('.meaning').count()==1
  page.evaluate("(id)=>state.progress[id]={due:1,interval:0,reps:1,lapses:0,last:''}",id)
 assert page.evaluate("dueWords('zh',6,'6.1').length>0&&dueWords('zh',6,'6.1').every(w=>w.course==='6.1')")
 assert page.evaluate("dueWords('zh',6,'6.2').length>0&&dueWords('zh',6,'6.2').every(w=>w.course==='6.2')")
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for c,n in [('6.1',1),('6.2',21)]:
   for dark in [False,True]:
    for view in ['library','detail','mistakes','words']:
     page.evaluate('(a)=>{lang="zh";hskLevel=6;hsk6Book=a.c;currentWord=a.id;mistakeScope="zh";state.settings.dark=a.dark;page=a.view;render()}',dict(c=c,id=f'zh6-{n:02}-01',dark=dark,view=view))
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,c,dark,view)
     assert page.evaluate("[...document.querySelectorAll('.course-pills .pill')].every(b=>{const r=b.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&b.scrollWidth<=b.clientWidth+1})"),(width,c,dark,view,'clipped course button')
 page.set_viewport_size({'width':390,'height':844})
 page.evaluate("currentWord='zh6-01-05';page='detail';state.settings.dark=false;render()")
 page.screenshot(path=str(ROOT/'output/screenshots/hsk6-word.png'),full_page=True)
 assert not errors,errors;browser.close()
report=dict(result='passed',newWords=counts,newLessons=40,oldWordsAndAudioPreserved=len(old['words']),checks=['Numbered vocabulary and source/excerpt metadata','Fresh install and old backup import','Independent HSK 6 books and last lessons','Quiz options and due queue isolation','Wrong-answer deduplication, retry and mastery history','Typing, listening, flashcards and audio bridge','Backup round trip and reload','Light/dark layouts at 320/360/390/700 px'],limitation='Chromium with mocked Android bridge; actual phone not tested.')
(ROOT/'output/hsk6-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('HSK 6 integration and migration checks passed:',counts)
