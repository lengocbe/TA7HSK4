"""HSK 2/3 source coverage, course isolation, mistakes and upgrade backup compatibility."""
from pathlib import Path
import json,zipfile,sys,re
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.4.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode('utf-8').removeprefix('const DATA = ').strip().removesuffix(';'))
for w in old['words']:assert byid[w['id']]==w,w['id']
for lesson in old['lessons']:assert next(l for l in data['lessons'] if l['id']==lesson['id'])==lesson
new=[w for w in data['words'] if w.get('level') in [2,3]]
assert len([w for w in data['words'] if w.get('level') not in [6,'spoken','hsk30','boya']])==len(old['words'])+len(new)
audit={r['id']:r for r in json.loads((ROOT/'content/hsk23/source-audit.json').read_text(encoding='utf-8'))}
counts={level:sum(w['level']==level for w in new) for level in [2,3]}
assert counts=={2:169,3:314}
for id,pron in {'zh2-12-02':'qī zi','zh2-13-06':'zhǎng','zh3-11-04':'huán','zh3-16-06':'zhǎng','zh3-18-03':'zhī','zh3-18-17':'de'}.items():assert byid[id]['pron']==pron,(id,byid[id]['pron'])
assert sum(w['exampleKind']=='pending' for w in new)==2
assert sum(w['exampleKind']=='exercise-completed' for w in new)==3
assert all(w.get('sourceKind')=='contents-index' and w['sourcePage']==14 for w in new if w['lesson']=='zh3-u18')
for level,total in [(2,15),(3,20)]:
 lessons=[l for l in data['lessons'] if l.get('level')==level];assert len(lessons)==total
 assert [l['number'] for l in lessons]==list(range(1,total+1))
 for l in lessons:
  ws=[byid[id] for id in l['words']];assert ws
  assert [w['bookNumber'] for w in ws]==list(range(1,len(ws)+1))
  for w in ws:
   assert w['course']==str(level) and w['sourceFile']==f'Giáo trình chuẩn HSK{level}.pdf'
   assert w['sourcePage']>0 and w['exampleKind'] in ['excerpt','title','exercise-completed','pending']
   assert all(w[k] for k in ['pron','meaning','pos'])
   if w['exampleKind']=='pending':
    assert w['id'] in ['zh3-18-02','zh3-18-04'] and not w['example'] and w['exampleNote']
    continue
   assert w['examplePages'] and w['translation']
   variants=[w['text']]+w.get('alternatives',[])+w.get('exampleForms',[])
   if '……' in w['text']:assert all(v in w['example'] for v in w['text'].split('……') if v)
   else:assert any(v in w['example'] for v in variants),(w['id'],w['example'])
   assert audit[w['id']]['source']['num']==w['bookNumber']
backup={'schema':1,'progress':{'en-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-08'}},'mistakes':{'en-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['en-01-01'],'last':{'en':'en-u1','zh':'zh5-u19'},'lastCourses':{'5.2':'zh5-u19','4.1':'zh4-u1'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
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
 for level,total in [(2,15),(3,20)]:
  page.locator(f'[data-action="hsk-level"][data-level="{level}"]').click()
  assert page.locator('[data-action="lesson"]').count()==total
  assert page.locator('[data-action="hsk-book"]').count()==0
  assert page.locator('[data-section="tests"]').count()==0
  assert page.evaluate('WORDS.filter(inCourse).length')==counts[level]
  page.screenshot(path=str(ROOT/f'output/screenshots/18-hsk{level}-lessons.png'),full_page=True)
  page.locator(f'[data-action="lesson"][data-id="zh{level}-u1"]').click()
  page.evaluate("startStudy(lessonWords(lessonId),'meaning','Test','lesson')")
  assert page.evaluate('study.options.every(w=>w.level===hskLevel)')
  first=page.evaluate('study.queue[0].id');page.evaluate("answerQuestion('wrong')")
  # Complete round correctly except the first word, then retry exactly that word.
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index < study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[first]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click()
  assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
  page.locator('[data-action="open-mistakes"]').click();page.locator('[data-action="mistake-scope"][data-scope="zh"]').click()
  assert page.locator('.mistake-item').count()==1
  assert page.evaluate('visibleMistakes().every(w=>w.level===hskLevel)')
  page.locator('[data-action="audio"]').first.click();assert page.evaluate('audioCalls.at(-1).id')==first
  page.locator('[data-action="master-mistake"]').click();assert page.locator('.mistake-item').count()==0
  page.evaluate("page='library';render()")
 # Last lessons for each lower course survive backup validation and reload.
 exported=page.evaluate('backup()');saved=page.evaluate('state');page.evaluate('state=defaults()');page.evaluate('(raw)=>receiveBackup(raw)',exported)
 assert page.evaluate('state')==saved
 page.reload();assert page.evaluate('state.lastCourses[2]')=='zh2-u1' and page.evaluate('state.lastCourses[3]')=='zh3-u1'
 assert page.evaluate("state.progress['en-01-01'].reps")==3 and page.evaluate("state.mistakes['en-01-01'].mastered")
 # Both courses reuse listening, typing alternatives, cards and isolated due queues.
 page.evaluate("startStudy([BYID['zh3-01-10']],'typing','Test','lesson')")
 page.locator('#typed-answer').fill('南');page.locator('[data-action="check-typing"]').click();assert page.evaluate('study.correct')==1
 page.evaluate("startStudy([BYID['zh2-01-01']],'listening','Test','lesson')")
 assert page.evaluate('study.options.every(w=>w.level===2)')
 page.evaluate("startStudy([BYID['zh3-01-01']],'cards','Test','lesson');study.reveal=true;render()")
 assert page.locator('.meaning').count()==1
 page.evaluate("for(const id of ['zh2-01-01','zh3-01-01'])state.progress[id]={due:1,interval:0,reps:1,lapses:0,last:''}")
 assert page.evaluate("dueWords('zh',2,'2').every(w=>w.level===2)") and page.evaluate("dueWords('zh',3,'3').every(w=>w.level===3)")
 page.evaluate("currentWord='zh3-18-02';page='detail';render()")
 assert '168–169' in page.locator('.notice').inner_text()
 page.evaluate("currentWord='zh3-18-01';page='detail';render()")
 assert 'Câu bài tập đã điền đáp án' in page.locator('.example .eyebrow').text_content()
 for level,total in [(2,15),(3,20)]:
  page.evaluate('(level)=>{lang="zh";hskLevel=level;page="library";render()}',level)
  assert page.locator('[data-action="lesson"]').count()==total+1  # resume button
  for view in ['words','stats','mistakes']:
   page.evaluate('(view)=>{page=view;mistakeScope="zh";render()}',view)
   assert page.evaluate('WORDS.filter(inCourse).every(w=>w.level===hskLevel)')
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for level in [2,3,4,5]:
   for dark in [False,True]:
    page.evaluate('(a)=>{lang="zh";hskLevel=a.level;state.settings.dark=a.dark;page="library";render()}',dict(level=level,dark=dark))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,level,dark)
 assert not errors,errors;browser.close()
report=dict(result='passed',newWords=counts,newLessons=35,oldWordsPreserved=len(old['words']),checks=['Original records unchanged','Numbered source rows and contents/index recovery for lesson 18','Verified excerpts, completed exercise labels and two explicit source gaps','Fresh install and 1.4 backups','Separate levels, last lessons, due queues and quiz options','Incorrect answer, retry, mastery, typing alternatives, listening, cards and audio bridge','Backup round trip and reload','Light/dark layout at 320/360/390/700 px'],sourceLimitations=['Supplied HSK 3 PDF omits printed pages 168-169; lesson 18 vocabulary and order use contents/index','Two words (wan and zui) have no verified example','Three examples complete printed fill-in-the-blank exercises and are labelled'],limitation='Chromium with mocked Android bridge; actual phone not tested.')
(ROOT/'output/hsk23-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('HSK 2/3 integration and migration checks passed.')
