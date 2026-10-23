"""Check the UI's Android bridge contract, including a fresh empty installation."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    context.add_init_script('''window.bridgeCalls=[];
    window.Android={
        load(){return localStorage.getItem('mock-native-state')||'';},
        save(value){localStorage.setItem('mock-native-state',value);return true;},
        theme(dark){window.bridgeDark=dark;},
        play(id,slow){window.bridgeCalls.push({id,slow});},
        stop(){},
        exportBackup(value){window.exportedBackup=value;},
        importBackup(){window.importCalled=true;}
    };''')
    page=context.new_page();page.goto((ROOT/'www/index.html').as_uri())
    assert page.locator('#toast').inner_text()==''
    page.evaluate('nativeReady()')
    assert page.locator('#toast').inner_text()==''
    page.locator('[data-action="open-language"][data-lang="en"]').click()
    page.locator('[data-action="lesson"][data-id="en-u1"]').click()
    page.locator('[data-action="audio"]').first.click()
    assert page.evaluate('bridgeCalls[0]')=={'id':'en-01-01','slow':False}
    page.locator('[data-action="learn"]').first.click()
    page.locator('[data-action="slow"]').click()
    page.locator('[data-action="audio"]').click()
    assert page.evaluate('bridgeCalls[1]')=={'id':'en-01-01','slow':True}
    page.locator('[data-action="reveal"]').click()
    page.locator('[data-action="rate"][data-rating="good"]').click()
    page.reload()
    assert page.evaluate('state.progress["en-01-01"].reps')==1
    page.locator('.nav [data-action="nav"][data-page="settings"]').click()
    page.locator('[data-action="dark"]').click()
    assert page.evaluate('bridgeDark') is True
    page.locator('[data-action="export"]').click()
    exported=json.loads(page.evaluate('exportedBackup'))
    assert exported['progress']['en-01-01']['reps']==1
    page.locator('[data-action="import"]').click()
    assert page.evaluate('importCalled') is True
    # Property names from JSON input must never resolve through Object.prototype.
    exported['favorites']=['__proto__','constructor','en-01-01']
    page.on('dialog',lambda d:d.accept())
    page.evaluate('(raw)=>receiveBackup(raw)',json.dumps(exported))
    assert page.evaluate('state.favorites')==['en-01-01']
    browser.close()
report={'result':'passed','checks':['Fresh Android install with empty preferences','Native-ready initialization','Word ID and normal/slow audio parameters','Save/load persistence contract','Native theme calls','Native backup export/import callbacks','Unknown prototype keys filtered'],'limitation':'JavaScript bridge tested against a mock; physical Android execution is separate.'}
(ROOT/'output/bridge-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('All Android UI bridge contract checks passed.')
