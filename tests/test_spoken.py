"""Spoken courses, real UI study/backup flows, and exact legacy preservation."""
from pathlib import Path
import json,zipfile,sys,hashlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in data['words']}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.6.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode().removeprefix('const DATA = ').strip().removesuffix(';'))
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes()
 for l in old['lessons']:assert next(x for x in data['lessons'] if x['id']==l['id'])==l
new=[w for w in data['words'] if w.get('course') in ['spoken-upper','spoken-lower']]
assert len(old['words'])==4868 and len(new)==1014
assert sum(w['itemKind']=='phrase' for w in new)==138
assert sum(w['itemKind']=='vocabulary' for w in new)==876
counts=json.loads((ROOT/'content/spoken/counts.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'content/audio-manifest.json').read_text(encoding='utf-8'))
for w in new:
 spoken=w.get('speechText',w['text'])
 assert manifest[w['id']]['textHash']==hashlib.sha256(('zh-CN-XiaoxiaoNeural|'+w['text']+('|'+spoken if spoken!=w['text'] else '')).encode()).hexdigest()
 assert manifest[w['id']]['sha256']==hashlib.sha256((ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes()).hexdigest()
assert next(w['pron'] for w in new if w['text']=='你游泳游得怎么样？')=='nǐ yóu yǒng yóu de zěn me yàng？'
assert next(w['pron'] for w in new if w['text']=='请数一下儿。')=='qǐng shǔ yí xiàr。'
for n in range(1,31):
 l=next(l for l in data['lessons'] if l['id']==f'zhk-u{n}')
 assert l['course']==('spoken-upper' if n<=15 else 'spoken-lower')
 ws=[byid[id] for id in l['words']]
 assert len(ws)==sum(counts[str(n)].values()) and counts[str(n)]['phrases']>=3
 for w in ws:
  assert all(w[k] for k in ['text','pron','meaning','source','sourcePage','sourceFile'])
  assert w['course']==l['course'] and w['sourcePage']<= (179 if n<=15 else 219)
  assert not any(s in w['text'] for s in ['j心','米米',')便宜','(体温计)'])
errors=[]
backup={'schema':1,'progress':{'zh6-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-08'}},'mistakes':{'zh6-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['zh6-01-01'],'last':{'en':'en-u1','zh':'zh6-u21'},'lastCourses':{'6.2':'zh6-u21'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
 context.add_init_script("window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}}")
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto((ROOT/'www/index.html').as_uri());assert page.evaluate('Object.keys(state.progress).length')==0
 print('Fresh state loaded',flush=True)
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup)
 assert page.evaluate('state.progress')==backup['progress'] and page.evaluate('state.mistakes')==backup['mistakes']
 page.locator('[data-action="open-language"][data-lang="zh"]').click()
 page.locator('[data-action="hsk-level"][data-level="spoken"]').click()
 for c,n in [('spoken-upper',1),('spoken-lower',16)]:
  print('Testing',c,flush=True)
  page.locator(f'[data-action="hsk-book"][data-book="{c}"]').click()
  assert page.locator('[data-action="lesson"]').count()==15
  assert page.locator('[data-action="hsk-book"]').count()==6
  assert page.evaluate('(c)=>WORDS.filter(inCourse).every(w=>w.course===c)',c)
  page.screenshot(path=str(ROOT/f'output/screenshots/{c}.png'),full_page=True)
  page.locator(f'[data-action="lesson"][data-id="zhk-u{n}"]').click()
  for tab,kind in [('vocabulary','vocabulary'),('phrases','phrase')]:
   page.locator(f'[data-action="spoken-section"][data-section="{tab}"]').click()
   assert page.evaluate('(k)=>studyLessonWords(lessonId).every(w=>w.itemKind===k)',kind)
   assert page.evaluate('studyLessonWords(lessonId).length')==counts[str(n)]['phrases' if kind=='phrase' else 'vocabulary']
   page.locator('[data-action="learn"][data-mode="new"]').click()
   assert page.evaluate('(k)=>study.queue.every(w=>w.itemKind===k)',kind)
   page.evaluate("study=null;page='lesson';render()")
  page.locator('[data-action="quiz-menu"]').click()
  page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
  assert page.evaluate('(c)=>study.queue.every(w=>w.course===c&&w.itemKind==="phrase")&&study.options.every(w=>w.course===c&&w.itemKind==="phrase")',c)
  first=page.evaluate('study.queue[0].id');page.evaluate("answerQuestion('wrong');answerQuestion('wrong')")
  assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index<study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[first]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="open-mistakes"]').click();page.locator('[data-action="mistake-scope"][data-scope="zh"]').click()
  assert page.locator('.mistake-item').count()==1
  page.locator('[data-action="audio"]').first.click();assert page.evaluate('audioCalls.at(-1).id')==first
  page.locator('[data-action="review-mistake"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[first]
  page.evaluate("study=null;page='mistakes';render()")
  page.locator('[data-action="master-mistake"]').click();assert page.locator('.mistake-item').count()==0
  assert page.evaluate('(id)=>state.mistakes[id].mastered&&state.mistakes[id].count===1',first)
  page.evaluate("(id)=>{startStudy([BYID[id]],'meaning','Test','lesson');answerQuestion('wrong')}",first)
  assert page.evaluate('(id)=>state.mistakes[id].count===2&&!state.mistakes[id].mastered',first)
  page.evaluate("study=null;page='library';render()")
 saved=page.evaluate('state');raw=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(s)=>receiveBackup(s)',raw)
 print('Study flows passed',flush=True)
 assert page.evaluate('state')==saved
 page.reload();assert page.evaluate("state.lastCourses['spoken-upper']==='zhk-u1'&&state.lastCourses['spoken-lower']==='zhk-u16'")
 assert page.evaluate("state.progress['zh6-01-01'].reps===3&&state.lastCourses['6.2']==='zh6-u21'")
 for c,n in [('spoken-upper',1),('spoken-lower',16)]:
  id=f'zhk-{n:02}-p01'
  page.evaluate("(id)=>startStudy([BYID[id]],'typing','Test','lesson')",id)
  page.locator('#typed-answer').fill(byid[id]['text'].replace('，',',').replace('？','?').replace('。','').replace('！','!'))
  page.locator('[data-action="check-typing"]').click();assert page.evaluate('study.correct')==1
  page.evaluate("(id)=>startStudy([BYID[id]],'listening','Test','lesson')",id)
  assert page.evaluate('(c)=>study.options.every(w=>w.course===c&&w.itemKind==="phrase")',c)
  page.evaluate("(id)=>state.progress[id]={due:1,interval:0,reps:1,lapses:0,last:''}",id)
  assert page.evaluate('(c)=>dueWords("zh","spoken",c).length>0&&dueWords("zh","spoken",c).every(w=>w.course===c)',c)
 longest=max((w for w in new if w['itemKind']=='phrase'),key=lambda w:len(w['text']))
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for dark in [False,True]:
   for view in ['library','lesson','detail','mistakes','words','study']:
    page.evaluate('(a)=>{lang="zh";hskLevel="spoken";spokenBook=a.course;lessonId=a.lesson;spokenSection="phrases";currentWord=a.id;mistakeScope="zh";state.settings.dark=a.dark;if(a.view==="study")startStudy([BYID[a.id]],"meaning","Test","lesson");page=a.view;render()}',dict(course=longest['course'],lesson=longest['lesson'],id=longest['id'],dark=dark,view=view))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,dark,view)
    assert page.evaluate("[...document.querySelectorAll('.course-pills .pill')].every(b=>b.scrollWidth<=b.clientWidth+1)"),(width,dark,view)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("page='detail';state.settings.dark=false;render()")
 page.screenshot(path=str(ROOT/'output/screenshots/spoken-phrase.png'),full_page=True)
 assert not errors,errors
 browser.close()
report=dict(result='passed',vocabulary=876,phrases=138,lessons=30,legacyWordsUnchanged=4868,checks=['Fresh install state','Old backup restore','Both books and section tabs','Kind-specific cards and quiz options','Wrong answer deduplication and retry','Mastery retains history and reactivates','Audio bridge','Backup round trip and restart','Typing punctuation','Due isolation','320/360/390/700 light/dark layouts'],physicalPhoneTested=False)
(ROOT/'output/spoken-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Spoken tests passed:',report)
