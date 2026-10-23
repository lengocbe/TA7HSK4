"""HSK course separation, original backup migration, new study flows and narrow layouts."""
from pathlib import Path
import hashlib,json,subprocess,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
old=json.loads(subprocess.check_output(['git','show','8f38002:content/catalog.json'],cwd=ROOT).decode('utf-8'))
byid={w['id']:w for w in catalog['words']}
for w in old['words']:
    assert all(byid[w['id']][k]==v for k,v in w.items()),w['id']
new=[w for w in catalog['words'] if w.get('level')==5 and w.get('course','5.1')=='5.1']
assert len(new)==723 and len({w['id'] for w in new})==723
counts=[38,39,41,40,46,41,45,43,38,37,41,43,37,41,39,41,33,40]
for i,count in enumerate(counts,1):
    ws=[w for w in new if w['lesson']==f'zh5-u{i}']
    assert len(ws)==count
    assert [w['bookNumber'] for w in ws]==list(range(1,count+1))
    assert all(w['sourcePage']>0 and w['examplePages'] for w in ws)
assert [w['id'] for w in new if w['exampleKind']=='pending']==['zh5-13-14']
for id,pron in {'zh5-02-12':'zhèng','zh5-02-35':'pū','zh5-04-01':'bēi','zh5-05-41':'wéi','zh5-07-40':'gǎn','zh5-10-18':'jì','zh5-14-23':'zhòng','zh5-14-30':'wèi'}.items():assert byid[id]['pron']==pron
old_state={'schema':1,'progress':{'en-01-01':{'due':1,'interval':2,'reps':3,'lapses':0,'last':'2026-10-07'},'zh-01-01':{'due':1,'interval':4,'reps':2,'lapses':0,'last':'2026-10-07'}},'favorites':['zh-01-01'],'last':{'en':'en-u1','zh':'zh-t1'},'daily':{'2026-10-07':5},'settings':{'dark':False,'slow':False,'goal':15}}
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    context.add_init_script('''window.audioCalls=[];window.Android={load(){return localStorage.getItem('test-state')||''},save(s){localStorage.setItem('test-state',s);return true},theme(){},stop(){},play(id,slow){audioCalls.push({id,slow})}};''')
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'www/index.html').as_uri())
    page.evaluate('(s)=>localStorage.setItem("test-state",JSON.stringify(s))',old_state);page.reload()
    assert page.evaluate('state.progress["zh-01-01"].reps')==2
    assert page.evaluate('state.lastCourses[4]')=='zh-t1'
    page.locator('[data-action="open-language"][data-lang="zh"]').click()
    assert page.locator('.lesson').count()==10
    page.locator('[data-action="hsk-level"][data-level="5"]').click()
    assert page.locator('.lesson').count()==18
    assert page.locator('[data-section="tests"]').count()==0
    page.screenshot(path=str(ROOT/'output/screenshots/09-hsk5-lessons.png'),full_page=True)
    page.locator('[data-action="lesson"][data-id="zh5-u1"]').click()
    assert page.locator('.word-row').count()==38
    page.locator('[data-action="audio"]').first.click()
    assert page.evaluate('audioCalls.at(-1).id')=='zh5-01-01'
    page.locator('[data-action="learn"][data-mode="new"]').click()
    page.locator('[data-action="reveal"]').click()
    assert 'chi tiết' in page.locator('.meaning').inner_text()
    assert 'Trích tiêu đề' in page.locator('.study-card').inner_text()
    page.locator('[data-action="rate"][data-rating="good"]').click()
    assert page.evaluate('state.progress["zh5-01-01"].reps')==1
    assert page.evaluate('state.progress["zh-01-01"].reps')==2
    page.reload();page.locator('[data-action="open-language"][data-lang="zh"]').click()
    page.locator('[data-action="hsk-level"][data-level="5"]').click()
    assert page.get_by_role('button',name='Học tiếp HSK 5.1 · Bài 01').count()==1
    page.locator('.nav [data-page="words"]').click()
    assert '723 từ' in page.locator('.filter-count').inner_text()
    page.locator('#search').fill('治')
    assert page.locator('.word-row').count()==1
    page.locator('[data-action="word"]').click()
    assert '白玉壶' in page.locator('.example').inner_text()
    assert 'pinyin' not in page.locator('.example').inner_text() # rendered pronunciation, not a placeholder
    page.screenshot(path=str(ROOT/'output/screenshots/10-hsk5-word.png'),full_page=True)
    page.locator('[data-action="back"]').click()
    page.locator('.nav [data-page="stats"]').click()
    assert page.locator('.lesson').count()==18
    assert page.locator('.stat strong').first.inner_text()=='1'
    page.locator('[data-action="hsk-level"][data-level="4"]').click()
    assert page.locator('.lesson').count()==10
    assert page.locator('.stat strong').first.inner_text()=='1'
    page.locator('[data-action="hsk-level"][data-level="5"]').click()
    page.evaluate('state.progress["zh5-01-01"].due=1;render()')
    page.locator('[data-action="review"]').click()
    assert page.evaluate('study.queue.every(w=>w.level===5)')
    page.on('dialog',lambda dialog:dialog.accept())
    page.locator('[data-action="exit-study"]').click()
    page.evaluate('openLesson("zh5-u2")')
    page.locator('[data-action="quiz-menu"]').click()
    page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
    assert page.evaluate('study.options.every(w=>w.level===5)')
    correct=page.evaluate('study.queue[0].id')
    page.locator('[data-action="answer"][data-id="'+correct+'"]').click()
    assert 'Chính xác' in page.locator('.feedback').inner_text()
    # Exercise accepted short forms from the parenthesized textbook headwords.
    page.evaluate('startStudy([BYID["zh5-02-04"]],"typing","Test")')
    page.locator('#typed-answer').fill('屋');page.locator('[data-action="check-typing"]').click()
    assert 'Chính xác' in page.locator('.feedback').inner_text()
    # The missing example is visible; no fabricated sentence is substituted.
    page.evaluate('page="detail";currentWord="zh5-13-14";render()')
    assert 'Chưa tìm được câu ví dụ' in page.locator('.notice').inner_text()
    page.evaluate('state.settings.dark=true;page="library";lang="zh";hskLevel=5;render()')
    page.screenshot(path=str(ROOT/'output/screenshots/11-hsk5-dark.png'),full_page=True)
    for width in [320,360,390,700]:
        page.set_viewport_size({'width':width,'height':844})
        for action in ['page="library";render()','page="words";search="";render()','page="stats";render()','page="detail";currentWord="zh5-07-20";render()','page="detail";currentWord="zh5-13-09";render()']:
            page.evaluate(action)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,action)
    # Export/import round trip includes both levels and legacy progress.
    exported=page.evaluate('backup()')
    page.evaluate('state=defaults();receiveBackup('+json.dumps(exported)+')')
    assert page.evaluate('state.progress["en-01-01"].reps')==3
    assert page.evaluate('state.progress["zh-01-01"].reps')==2
    assert page.evaluate('state.progress["zh5-01-01"].reps')==1
    assert not errors,errors
    browser.close()
report={'result':'passed','hsk5Lessons':18,'hsk5Words':723,'pendingExampleIds':['zh5-13-14'],'checks':['All original 414 word records preserved','723 new words in printed order','Contextual pronunciations','Version 1 backups migrate without losing progress','HSK 4/5 filters and due queues are separate','HSK 5 cards, native audio calls, quiz choices and short-form typing','Combined backup restore','Long Chinese words and examples at widths 320/360/390/700','Dark mode'],'limitation':'Browser and mocked native bridge; physical Android testing is still required.'}
(ROOT/'output/hsk5-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('HSK 5.1 integration and migration checks passed.')
