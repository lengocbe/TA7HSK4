"""Native smoke test using a dedicated emulator (not a user's phone)."""
from pathlib import Path
import subprocess,time,tempfile,xml.etree.ElementTree as ET,re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
ADB=ROOT/'tools/android-sdk/platform-tools/adb.exe'
PKG='vn.lnb.sotuvung'
OUT=ROOT/'output/screenshots';OUT.mkdir(exist_ok=True)
checks=[]

def adb(*args,timeout=45):
    proc=subprocess.run([str(ADB),'-s','emulator-5554',*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    if proc.returncode:raise RuntimeError(proc.stderr.decode('utf-8',errors='replace'))
    return proc.stdout.decode('utf-8',errors='replace')

def hierarchy():
    adb('shell','uiautomator','dump','/sdcard/lingo-ui.xml')
    text=adb('shell','cat','/sdcard/lingo-ui.xml')
    (ROOT/'tmp/native-ui.xml').write_text(text,encoding='utf-8')
    return ET.fromstring(text)

def tap(label,exact=False):
    root=hierarchy();candidates=[]
    for node in root.iter('node'):
        text=node.get('text','') or node.get('content-desc','')
        if (text==label if exact else label in text):
            values=[int(x) for x in re.findall(r'\d+',node.get('bounds',''))]
            if len(values)==4 and values[2]>values[0] and values[3]>values[1]:
                candidates.append(((values[2]-values[0])*(values[3]-values[1]),values,text))
    if not candidates:raise AssertionError('UI label missing: '+label)
    _,(x1,y1,x2,y2),_=min(candidates)
    adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2));time.sleep(2)

def screenshot(name):
    adb('shell','screencap','-p','/sdcard/lingo-screen.png')
    adb('pull','/sdcard/lingo-screen.png',str(OUT/name))

def text_present(text):
    root=hierarchy()
    return any(text in ((n.get('text','') or '')+' '+(n.get('content-desc','') or '')) for n in root.iter('node'))

assert adb('shell','getprop','sys.boot_completed').strip()=='1','Emulator is not ready'
assert '28'==adb('shell','getprop','ro.build.version.sdk').strip()
print(adb('install','-r',str(Path(tempfile.gettempdir())/'lingo-android-build/Lingo-SoTuVung-1.0.0.apk'),timeout=90),flush=True)
checks.append('Release APK installation on Android 9 / API 28')
adb('shell','settings','put','global','airplane_mode_on','1')
adb('shell','svc','wifi','disable')
adb('shell','am','start','-n',PKG+'/.MainActivity');time.sleep(7)
assert text_present('Chọn ngôn ngữ')
screenshot('09-native-home.png')
checks.append('Offline startup and language home screen')
tap('Tiếng Anh',True)
assert text_present('Hobbies')
tap('Hobbies',True)
assert text_present('belong to')
tap('Nghe phát âm',True)
audio_logs=adb('logcat','-d','-s','LingoAudio:I')
assert 'Prepared en-01-01' in audio_logs,audio_logs
assert 'Playback failed' not in audio_logs,audio_logs
checks.append('Native MediaPlayer prepared and started packaged MP3 in airplane mode')
tap('Học từ mới')
tap('Hiện nghĩa')
assert text_present('thuộc về')
screenshot('10-native-flashcard.png')
tap('Nhớ')
adb('shell','input','keyevent','4');time.sleep(2)
assert text_present('Thoát lượt học?')
tap('OK',True)
checks.append('Flashcard, rating and Android back confirmation dialog')
adb('shell','am','force-stop',PKG)
adb('shell','am','start','-n',PKG+'/.MainActivity');time.sleep(5)
assert text_present('1 từ đã học')
checks.append('SharedPreferences persistence across process restart')
tap('Cài đặt',True)
assert text_present('Giao diện tối')
tap('Giao diện tối',True)
screenshot('11-native-dark-settings.png')
checks.append('Native dark-mode screen')
logs=adb('logcat','-d','-t','800')
(ROOT/'tmp/native-logcat.txt').write_text(logs,encoding='utf-8')
assert 'FATAL EXCEPTION' not in logs,'Android crash detected'
assert 'Error preparing MediaPlayer' not in logs
report={'result':'passed','androidApi':28,'checks':checks,'limitations':['Tested on software emulator, not a physical phone','Android 15 inset handling requires a device/API 35 run','Technical audio playback and decoding tested; not an individual human pronunciation audit of every recording']}
(ROOT/'output/android-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Native Android smoke checks passed.',flush=True)
