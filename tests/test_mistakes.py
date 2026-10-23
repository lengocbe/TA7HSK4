"""Incorrect-answer persistence, end-of-round retry, voluntary practice and old backups."""
from pathlib import Path
import json,copy,zipfile,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(ROOT/'output/Lingo-SoTuVung-1.3.0.apk') as previous:
 old=json.loads(previous.read('assets/www/data.js').decode('utf-8').removeprefix('const DATA = ').strip().removesuffix(';'))
current_words={w['id']:w for w in data['words']}
current_lessons={l['id']:l for l in data['lessons']}
assert all(current_words[w['id']]==w for w in old['words']),'Prior vocabulary records must stay unchanged'
assert all(current_lessons[l['id']]==l for l in old['lessons']),'Prior lesson records must stay unchanged'
backup={'schema':1,'progress':{'en-01-01':{'due':1,'interval':4,'reps':3,'lapses':0,'last':'2026-10-08'}},'favorites':['en-01-01'],'last':{'en':'en-u1','zh':'zh5-u19'},'lastCourses':{'5.2':'zh5-u19'},'daily':{},'settings':{'dark':False,'slow':False,'goal':15}}
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
 context.add_init_script('''window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}};''')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto((ROOT/'www/index.html').as_uri())
 assert page.evaluate('Object.keys(state.mistakes).length')==0
 page.locator('[data-action="open-mistakes"]').click()
 assert 'Chưa có từ cần luyện' in page.locator('.empty').inner_text()
 # v1.3 restores normally, initializing only the new history collection.
 page.evaluate('(s)=>localStorage.setItem("test-state",JSON.stringify(s))',backup);page.reload()
 assert page.evaluate('Object.keys(state.mistakes).length')==0
 assert page.evaluate("state.progress['en-01-01'].reps")==3
 page.evaluate("openLesson('en-u1');startStudy([BYID['en-01-01'],BYID['en-01-02']], 'meaning', 'Test')")
 first=page.evaluate('study.queue[0].id')
 wrong=page.evaluate('study.options.find(w=>w.id!==study.queue[0].id).id')
 page.locator(f'[data-action="answer"][data-id="{wrong}"]').click()
 assert page.evaluate('study.wrongIds')==[first]
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
 reps=page.evaluate('(id)=>state.progress[id].reps',first)
 # Function guard also protects double taps or calls from stale controls.
 page.evaluate('(id)=>{answerQuestion(id);answerQuestion(id)}',wrong)
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
 assert page.evaluate('(id)=>state.progress[id].reps',first)==reps
 page.locator('[data-action="next-question"]').click()
 index=page.evaluate('study.index')
 page.evaluate("document.dispatchEvent(new Event('unused'))")
 # A stale next-button event cannot skip a new unanswered question.
 page.evaluate("let b=document.createElement('button');b.dataset.action='next-question';document.body.appendChild(b);b.click();b.remove()")
 assert page.evaluate('study.index')==index
 current=page.evaluate('study.queue[study.index].id')
 page.locator(f'[data-action="answer"][data-id="{current}"]').click()
 page.locator('[data-action="next-question"]').click()
 assert page.locator('[data-action="retry-wrong"]').count()==1
 assert page.locator('.list-panel .word-row').count()==1
 assert page.evaluate('(id)=>!state.mistakes[id]',current)
 page.screenshot(path=str(ROOT/'output/screenshots/15-quiz-wrong-summary.png'),full_page=True)
 # Retry has only this round's missed word, the same quiz mode, and a fresh result.
 page.locator('[data-action="retry-wrong"]').click()
 assert page.evaluate('study.queue.map(w=>w.id)')==[first]
 assert page.evaluate('study.mode')=='meaning'
 page.locator(f'[data-action="answer"][data-id="{first}"]').click()
 page.locator('[data-action="next-question"]').click()
 assert page.locator('[data-action="retry-wrong"]').count()==0
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
 assert page.evaluate('(id)=>state.mistakes[id].mastered',first)==False
 page.locator('[data-action="open-mistakes"]').click()
 assert page.locator('.mistake-item').count()==1
 page.locator('[data-action="audio"]').click();assert page.evaluate('audioCalls.at(-1).id')==first
 page.locator('[data-action="master-mistake"]').click()
 assert page.locator('.mistake-item').count()==0
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==1
 page.locator('[data-action="mistake-status"][data-status="mastered"]').click()
 assert page.locator('.mistake-item').count()==1
 page.locator('[data-action="restore-mistake"]').click()
 page.locator('[data-action="mistake-status"][data-status="active"]').click()
 assert page.locator('.mistake-item').count()==1
 # Every quiz type records errors. Flashcard ratings don't count as wrong answers.
 for mode in ['reverse','listening','typing']:
  page.evaluate('(args)=>startStudy([BYID[args.id]],args.mode,"Test","mistakes")',{'id':first,'mode':mode})
  if mode=='typing':
   page.locator('#typed-answer').fill('not-the-answer');page.locator('[data-action="check-typing"]').click()
  else:
   bad=page.evaluate('study.options.find(w=>w.id!==study.queue[0].id).id')
   page.locator(f'[data-action="answer"][data-id="{bad}"]').click()
  page.locator('[data-action="next-question"]').click()
  page.locator('[data-action="retry-wrong"]').click()
  assert page.evaluate('study.mode')==mode
  if mode=='typing':
   value=page.evaluate('(id)=>BYID[id].text',first);page.locator('#typed-answer').fill(value);page.locator('[data-action="check-typing"]').click()
  else:page.locator(f'[data-action="answer"][data-id="{first}"]').click()
  page.locator('[data-action="next-question"]').click()
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==4
 page.evaluate('(id)=>startStudy([BYID[id]],"cards","Test","mistakes")',first)
 page.locator('[data-action="reveal"]').click();page.locator('[data-action="rate"][data-rating="again"]').click()
 assert page.evaluate('(id)=>state.mistakes[id].count',first)==4
 assert page.locator('[data-action="retry-wrong"]').count()==0
 # Add real failures from every Chinese course, then check independent filters.
 chinese=['zh-01-01','zh4-01-01','zh4-11-01','zh5-01-01','zh5-19-01']
 for id in chinese:
  page.evaluate('(id)=>{startStudy([BYID[id]],"typing","Test","mistakes");}',id)
  page.locator('#typed-answer').fill('错误答案');page.locator('[data-action="check-typing"]').click()
  page.locator('[data-action="next-question"]').click()
 page.locator('[data-action="open-mistakes"]').click()
 assert page.locator('.mistake-item').count()==6
 page.locator('[data-action="mistake-scope"][data-scope="en"]').click()
 assert page.locator('.mistake-item').count()==1
 page.locator('[data-action="mistake-scope"][data-scope="zh"]').click()
 for level,book,id in [(4,'legacy',chinese[0]),(4,'4.1',chinese[1]),(4,'4.2',chinese[2]),(5,'5.1',chinese[3]),(5,'5.2',chinese[4])]:
  page.locator(f'[data-action="hsk-level"][data-level="{level}"]').click()
  page.locator(f'[data-action="hsk-book"][data-book="{book}"]').click()
  assert page.locator('.mistake-item').count()==1
  assert page.locator('.mistake-item').get_attribute('data-word-id')==id
 # Marked words come back automatically if a later test answer is wrong.
 page.locator('[data-action="master-mistake"]').click()
 page.evaluate("startStudy([BYID['zh5-19-01']], 'typing', 'Test', 'mistakes')")
 page.locator('#typed-answer').fill('错');page.locator('[data-action="check-typing"]').click()
 assert page.evaluate("state.mistakes['zh5-19-01'].mastered")==False
 assert page.evaluate("state.mistakes['zh5-19-01'].count")==2
 page.locator('[data-action="next-question"]').click();page.locator('[data-action="open-mistakes"]').click()
 # History ordering, multi-select, subset practice, hidden-selection isolation.
 assert page.locator('.mistake-item').first.get_attribute('data-word-id')==first
 chosen=[first,'zh5-19-01']
 for id in chosen:page.locator(f'[data-action="select-mistake"][data-id="{id}"]').check()
 page.locator('[data-action="review-mistakes"][data-selection="selected"]').click()
 assert set(page.evaluate('study.queue.map(w=>w.id)'))==set(chosen)
 assert page.evaluate('study.options.every(w=>w.lang===study.queue[0].lang && (w.course||"legacy") === (study.queue[0].course||"legacy"))')
 page.locator('[data-action="exit-study"]').click()
 page.locator('[data-action="mistake-scope"][data-scope="en"]').click()
 assert page.evaluate('mistakeSelection')==[]
 page.locator('[data-action="select-visible-mistakes"]').click()
 assert page.evaluate('mistakeSelection')==[first]
 page.locator('#mistake-search').fill('not-found-anywhere')
 assert page.locator('.mistake-item').count()==0 and page.evaluate('mistakeSelection')==[]
 page.locator('#mistake-search').fill('')
 page.locator('[data-action="review-mistakes"][data-selection="all"]').click()
 assert page.evaluate('study.queue.map(w=>w.id)')==[first]
 page.locator('[data-action="exit-study"]').click()
 # One-word voluntary practice and detail back navigation retain the list.
 page.locator('[data-action="word"]').click();page.locator('[data-action="back"]').click()
 assert page.evaluate('page')=='mistakes'
 page.locator('[data-action="review-mistake"]').click()
 assert page.evaluate('study.queue.map(w=>w.id)')==[first]
 page.locator('[data-action="exit-study"]').click()
 # Completed mistakes data (including mastered archive) survives reload/backup.
 page.locator('[data-action="master-mistake"]').click()
 expected=page.evaluate('state.mistakes');old_progress=page.evaluate('state.progress')
 exported=page.evaluate('backup()');page.evaluate('state=defaults()');page.evaluate('(raw)=>receiveBackup(raw)',exported)
 assert page.evaluate('state.mistakes')==expected and page.evaluate('state.progress')==old_progress
 page.reload();assert page.evaluate('state.mistakes')==expected
 for changes in [{'count':0},{'count':1.2},{'lastWrong':-1},{'lastWrong':1e20},{'mastered':'yes'},{'mode':'unknown'}]:
  bad=json.loads(exported);bad['mistakes'][first].update(changes)
  page.evaluate('(raw)=>receiveBackup(raw)',json.dumps(bad))
  assert page.evaluate('state.mistakes')==expected,'Malformed history must not replace live data'
 # Unknown vocabulary IDs are safely discarded on import.
 raw=json.loads(exported);raw['mistakes']['unknown-word']={'count':1,'lastWrong':1,'mastered':False,'mode':'meaning'}
 page.evaluate('(raw)=>receiveBackup(raw)',json.dumps(raw));assert page.evaluate('state.mistakes')==expected
 # Navigation from the word library, mobile layouts, dark archive and empty states.
 page.evaluate("page='words';lang='zh';hskLevel=5;hsk5Book='5.2';render()")
 page.locator('[data-action="open-mistakes"]').click();assert page.evaluate('mistakeScope')=='zh'
 assert page.locator('.mistake-item').count()==1
 page.locator('[data-action="mistake-scope"][data-scope="all"]').click()
 page.screenshot(path=str(ROOT/'output/screenshots/16-mistakes-list.png'),full_page=True)
 for width in [320,360,390,700]:
  page.set_viewport_size({'width':width,'height':844})
  for dark in [False,True]:
   for status in ['active','mastered']:
    page.evaluate('(args)=>{state.settings.dark=args.dark;mistakeStatus=args.status;render()}',{'dark':dark,'status':status})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(width,dark,status)
 page.set_viewport_size({'width':390,'height':844});page.evaluate("mistakeStatus='mastered';state.settings.dark=true;render()")
 page.screenshot(path=str(ROOT/'output/screenshots/17-mistakes-mastered-dark.png'),full_page=True)
 assert not errors,errors
 browser.close()
report=dict(result='passed',checks=['All vocabulary records remain identical to version 1.3','Fresh installs and older backups have empty new history','All four quiz modes track incorrect answers exactly once','Stale answer/next events do not count twice or skip questions','Round retry contains only missed words and retains quiz mode','Correct answers and flashcard ratings retain history','Mastered archive, restore and later-error reactivation','All language/course filters and sorted counts','Subset, all and one-word practice','Search and filter changes clear hidden selections','Native audio bridge','Reload, backup round trip and malformed import rejection','Light/dark layouts at 320/360/390/700 px'],limitation='Browser with mocked Android bridge; actual Android device not tested.')
(ROOT/'output/mistakes-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Wrong-answer history, end-of-round retry and voluntary practice checks passed.')
