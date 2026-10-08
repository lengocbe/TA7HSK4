"""Exercise learning flows, persistence, backups and mobile layout in actual Chromium."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/screenshots';OUT.mkdir(parents=True,exist_ok=True)
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1)
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto((ROOT/'www/index.html').as_uri())
    page.get_by_role('heading',name='Chọn ngôn ngữ').wait_for()
    page.wait_for_timeout(250)
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'01-home.png'),full_page=True)
    assert page.locator('.language-card').count()==2
    page.locator('[data-action="open-language"][data-lang="en"]').click()
    assert page.locator('.lesson').count()==12
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'02-english-units.png'),full_page=True)
    page.locator('[data-action="lesson"][data-id="en-u1"]').click()
    assert page.locator('.word-row').count()==21
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'03-unit-1.png'),full_page=True)
    page.locator('[data-action="learn"][data-mode="new"]').click()
    assert page.locator('.meaning').count()==0
    page.locator('[data-action="reveal"]').click()
    assert page.locator('.meaning').inner_text()=='thuộc về'
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'04-flashcard.png'),full_page=True)
    page.locator('[data-action="rate"][data-rating="good"]').click()
    saved=page.evaluate('JSON.parse(localStorage.getItem("lingo-state"))')
    assert saved['progress']['en-01-01']['reps']==1
    assert saved['progress']['en-01-01']['interval']==2
    page.reload()
    page.locator('[data-action="open-language"][data-lang="en"]').click()
    assert page.locator('.word-status.learned').count()==1
    page.locator('[data-action="quiz-menu"]').click()
    page.locator('[data-action="start-quiz"][data-mode="meaning"]').click()
    correct=page.evaluate('study.queue[study.index].id')
    page.locator('[data-action="answer"][data-id="'+correct+'"]').click()
    assert page.locator('.feedback').inner_text().startswith('Chính xác!')
    assert page.locator('.choice.correct').count()==1
    page.locator('[data-action="next-question"]').click()
    correct=page.evaluate('study.queue[study.index].id')
    wrong=page.locator('[data-action="answer"]').evaluate_all('(els)=>els.map(e=>e.dataset.id)').copy()
    wrong=next(x for x in wrong if x!=correct)
    page.locator('[data-action="answer"][data-id="'+wrong+'"]').click()
    assert page.locator('.choice.wrong').count()==1
    assert page.evaluate('state.progress[study.queue[study.index].id].lapses')==1
    page.on('dialog',lambda dialog:dialog.accept())
    page.locator('[data-action="exit-study"]').click()
    page.locator('[data-action="nav"][data-page="home"]').click()
    page.locator('[data-action="open-language"][data-lang="zh"]').click()
    assert page.locator('.lesson').count()==10
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'05-chinese-lessons.png'),full_page=True)
    page.locator('[data-action="lesson"][data-id="zh-t1"]').click()
    assert page.locator('.word-row').count()==15
    page.locator('[data-action="learn"][data-mode="new"]').click()
    assert page.locator('.pronunciation').inner_text()=='Đoán cách đọc và nghĩa'
    page.locator('[data-action="reveal"]').click()
    assert 'rèn wù' in page.locator('.pronunciation').inner_text()
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'06-chinese-card.png'),full_page=True)
    page.locator('[data-action="rate"][data-rating="again"]').click()
    assert page.evaluate('state.progress["zh-01-01"].lapses')==1
    page.locator('[data-action="exit-study"]').click()
    page.locator('[data-action="quiz-menu"]').click()
    page.locator('[data-action="start-quiz"][data-mode="typing"]').click()
    answer=page.evaluate('study.queue[study.index].text')
    page.locator('#typed-answer').fill(answer)
    page.locator('[data-action="check-typing"]').click()
    assert page.locator('.feedback').inner_text().startswith('Chính xác!')
    page.locator('[data-action="exit-study"]').click()
    page.locator('[data-action="nav"][data-page="words"]').click()
    page.locator('#search').fill('nhiệm vụ')
    assert page.locator('.word-row').count()==1
    page.locator('[data-action="word"]').click()
    page.locator('[data-action="favorite"]').click()
    assert page.locator('.favorite.saved').count()==1
    page.locator('[data-action="back"]').click()
    page.locator('#search').fill('')
    page.locator('[data-action="filter"][data-filter="saved"]').click()
    assert page.locator('.word-row').count()==1
    page.locator('[data-action="nav"][data-page="settings"]').click()
    page.locator('[data-action="dark"]').click()
    assert page.locator('body.dark').count()==1
    page.locator('#daily-goal').select_option('20')
    assert page.evaluate('state.settings.goal')==20
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'07-dark-settings.png'),full_page=True)
    old_state=page.evaluate('backup()')
    page.evaluate('state=defaults();save()')
    page.evaluate('(raw)=>receiveBackup(raw)',old_state)
    assert page.evaluate('state.favorites.includes("zh-01-01")')
    assert page.evaluate('state.settings.dark')
    page.evaluate('receiveBackup("{broken}")')
    assert 'không hợp lệ' in page.locator('#toast').inner_text()
    # Malformed nested values must not enter persisted state.
    malformed=json.loads(old_state);malformed['progress']['zh-01-01']['reps']='bad'
    page.evaluate('(raw)=>receiveBackup(raw)',json.dumps(malformed))
    assert 'không hợp lệ' in page.locator('#toast').inner_text()
    page.locator('[data-action="nav"][data-page="stats"]').click()
    page.wait_for_timeout(250)
    page.screenshot(path=str(OUT/'08-progress.png'),full_page=True)
    # Check for horizontal overflow at compact phone widths in every main screen.
    for width in [320,360,390,430,700]:
        page.set_viewport_size({'width':width,'height':800})
        for dest in ['home','library','words','stats','settings']:
            page.locator('[data-action="nav"][data-page="'+dest+'"]').click()
            assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),(width,dest)
    assert not errors,errors
    browser.close()
report={'result':'passed','checks':['12 English units / 10 Chinese topics','Flashcards and hidden Chinese pinyin','SRS scheduling and incorrect-answer lapses','Quiz and Chinese typing','Persistence after reload','Search and favorites','Dark mode / daily goal','Backup restore and invalid-backup rejection','320–700 px viewport overflow checks'],'browserErrors':errors}
(ROOT/'output/browser-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('All browser integration checks passed.')
