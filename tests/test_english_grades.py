"""English grade isolation, old backup compatibility and unchanged 1.12 content."""
from pathlib import Path
import json,zipfile,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.stdout.reconfigure(encoding='utf-8')
cat=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'));byid={w['id']:w for w in cat['words']};new=[w for w in cat['words'] if w.get('grade') in [6,8,9]]
assert len(new)==752 and len(cat['words'])==19411 and len(cat['lessons'])==660
assert {g:sum(w['grade']==g for w in new) for g in [6,8,9]}=={6:208,8:279,9:265}
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.12.0.apk') as z:
 old=json.loads(z.read('assets/www/data.js').decode().removeprefix('const DATA = ').strip().removesuffix(';'))
 for w in old['words']:
  assert byid[w['id']]==w,w['id']
  if '--ui-only' not in sys.argv:assert z.read('assets/www/audio/'+w['id']+'.mp3')==(ROOT/'www/audio'/(w['id']+'.mp3')).read_bytes(),w['id']
 for l in old['lessons']:assert next(n for n in cat['lessons'] if n['id']==l['id'])==l
for g in [6,8,9]:
 lessons=[l for l in cat['lessons'] if l.get('grade')==g]
 assert [l['number'] for l in lessons if l['kind']=='unit']==list(range(1,13))
 for n in range(1,5):
  review=next(l for l in lessons if l['id']==f'en{g}-r{n}')
  assert review['words']==[id for l in lessons if l['kind']=='unit' and (n-1)*3<l['number']<=n*3 for id in l['words']]
 for w in new:
  assert all(w[k] for k in ['text','pron','meaning','pos','sourceFile','sourcePage'])
backup={'schema':1,'progress':{'en-01-01':{'due':1,'interval':4,'reps':3,'lapses':1,'last':'2026-10-17'}},'mistakes':{'en-01-01':{'count':2,'lastWrong':1234,'mastered':True,'mode':'meaning'}},'favorites':['en-01-01'],'last':{'en':'en-u1'},'lastCourses':{'hsk30-1':'zh30-1-u1'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');ctx.add_init_script("window.Android={load(){return localStorage.getItem('grade-state')||''},save(s){localStorage.setItem('grade-state',s);return true},theme(){},stop(){},play(){}}")
 page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto((ROOT/'www/index.html').as_uri())
 assert page.evaluate('Object.keys(state.progress).length')==0
 page.evaluate('(s)=>receiveBackup(JSON.stringify(s))',backup)
 assert page.evaluate("state.lastCourses['en-7']==='en-u1'&&state.progress['en-01-01'].reps===3")
 for g in [6,7,8,9]:
  page.evaluate('lang="en";page="library";render()')
  page.locator(f'[data-action="en-grade"][data-grade="{g}"]').click()
  assert page.locator('[data-action="en-grade"]').count()==4
  assert page.locator('.lesson[data-action="lesson"]').count()==12
  assert page.evaluate('(g)=>WORDS.filter(inCourse).every(w=>englishGrade(w)===g)',g)
  page.locator('[data-action="lesson"]').first.click()
  page.locator('[data-action="quiz-menu"]').click();page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
  assert page.evaluate('(g)=>study.options.every(w=>englishGrade(w)===g)',g)
  id=page.evaluate('study.queue[0].id');prior=page.evaluate('(id)=>state.mistakes[id]?.count||0',id)
  page.evaluate("answerQuestion('wrong');answerQuestion('wrong')")
  assert page.evaluate('(id)=>state.mistakes[id].count',id)==prior+1
  page.locator('[data-action="next-question"]').click()
  while page.evaluate('study.index<study.queue.length'):
   page.evaluate('answerQuestion(study.queue[study.index].id)');page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click();assert page.evaluate('study.queue.map(w=>w.id)')==[id]
  page.evaluate('answerQuestion(study.queue[0].id)');page.locator('[data-action="next-question"]').click()
  page.evaluate('(g)=>{lang="en";enGrade=g;mistakeScope="en";page="mistakes";render()}',g)
  assert page.evaluate('(g)=>visibleMistakes().every(w=>englishGrade(w)===g)',g)
  page.evaluate('(id)=>setMastered(id,true)',id);assert page.evaluate('(id)=>state.mistakes[id].mastered',id)
  for mode in ['reverse','listening','typing']:
   page.evaluate('(a)=>{startStudy(WORDS.filter(w=>w.lang==="en"&&englishGrade(w)===a.g).slice(0,3),a.mode,"Test","library")}',dict(g=g,mode=mode))
   if mode=='typing':
    page.locator('#typed-answer').fill(page.evaluate('study.queue[0].text'));page.locator('[data-action="check-typing"]').click()
   else:page.evaluate('answerQuestion(study.queue[0].id)')
   assert page.evaluate('study.correct')==1
  page.evaluate('(g)=>{study=null;lang="en";enGrade=g;page="stats";render()}',g)
  assert page.evaluate('(g)=>dueWords("en",null,"en-"+g).every(w=>englishGrade(w)===g)',g)
  page.evaluate('(g)=>{lang="en";enGrade=g;page="library";section="review";render()}',g)
  assert page.locator('.lesson[data-action="lesson"]').count()==4
 saved=page.evaluate('state');raw=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(s)=>receiveBackup(s)',raw);assert page.evaluate('state')==saved;page.reload();assert page.evaluate('state')==saved
 for width in [320,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for g in [6,7,8,9]:
   for dark in [False,True]:
    for view in ['library','words','stats','mistakes']:
     page.evaluate('(a)=>{lang="en";enGrade=a.g;page=a.view;mistakeScope="en";state.settings.dark=a.dark;render()}',dict(g=g,view=view,dark=dark))
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,g,dark,view)
 page.set_viewport_size({'width':390,'height':844});page.evaluate('lang="en";enGrade=6;page="library";section="units";state.settings.dark=false;render()');page.screenshot(path=str(ROOT/'output/screenshots/english-grade6.png'))
 page.evaluate('lang="en";enGrade=9;page="library";render()');page.screenshot(path=str(ROOT/'output/screenshots/english-grade9.png'))
 assert not errors,errors;b.close()
report=dict(result='passed',newWords=752,newUnits=36,newReviewGroups=12,legacyWordsUnchanged=18659,newGrades=[6,8,9],physicalDeviceTested=False)
(ROOT/'output/english-grades-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
