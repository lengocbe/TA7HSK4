"""Intensive course publishing gates and UI integration using isolated fixtures."""
from pathlib import Path
import copy,json,sys,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_hsk5_intensive import merge
base=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
base=dict(base,words=[w for w in base['words'] if w.get('level')!='intensive5'],lessons=[l for l in base['lessons'] if l.get('level')!='intensive5'])
books=json.loads((ROOT/'content/hsk5-intensive/books.json').read_text(encoding='utf-8'))
assert len(books)==24 and sum(b['category']=='vocabulary' for b in books)==5
for bad in [{},{'reviewComplete':False}]:
 try:merge(base,bad,books)
 except AssertionError:pass
 else:raise AssertionError('Unreviewed content accepted')
fixture={'reviewComplete':True,'courses':[{'book':'book-19','id':'intensive5-breakthrough','title':'Vocabulary Breakthrough','coverageNote':'Test fixture only','lessons':[{'title':'Test lesson','words':[{'text':'爱护','pron':'ài hù','meaning':'chăm sóc','page':2,'raw':'爱护 aihu v. care for','reviewed':True},{'text':'爱心','pron':'ài xīn','meaning':'lòng yêu thương','page':2,'raw':'爱心 aixin n. loving heart','reviewed':True}]}]}]}
result=merge(base,fixture,books)
assert result['words'][:len(base['words'])]==base['words']
assert result['lessons'][:len(base['lessons'])]==base['lessons']
assert merge(result,fixture,books)==result
invalid=copy.deepcopy(fixture);invalid['courses'][0]['lessons'][0]['words'][0]['reviewed']=False
try:merge(base,invalid,books)
except AssertionError:pass
else:raise AssertionError('Unreviewed word accepted')
with tempfile.TemporaryDirectory(prefix='lingo-intensive-test-') as tmp:
 tmp=Path(tmp)
 for name in ['index.html','style.css','app.compat.js']:(tmp/name).write_bytes((ROOT/'www'/name).read_bytes())
 (tmp/'data.js').write_text('const DATA = '+json.dumps(result,ensure_ascii=False)+';',encoding='utf-8')
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
  page=browser.new_page(viewport={'width':320,'height':800});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((tmp/'index.html').as_uri());page.locator('[data-action="open-language"][data-lang="zh"]').click()
  page.locator('[data-action="hsk-level"][data-level="intensive5"]').click()
  assert page.locator('[data-action="lesson"]').count()==1
  page.locator('[data-action="lesson"]').click()
  assert page.evaluate('WORDS.filter(inCourse).length')==2
  saved=page.evaluate('backup()');page.evaluate('(s)=>receiveBackup(s)',saved)
  assert page.evaluate("state.lastCourses['intensive5-breakthrough']!==undefined")
  for view in ['library','words','stats','mistakes']:
   page.evaluate('(view)=>{page=view;render()}',view)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  browser.close()
print('24-source inventory, publish gates, legacy preservation, idempotency, course navigation, backup and mobile layout passed. Fixtures were not published.')
