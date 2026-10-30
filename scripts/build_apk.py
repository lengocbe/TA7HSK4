"""Reproducible direct-SDK build. Requires JDK, SDK 35 and generated assets."""
from pathlib import Path
import subprocess, os, shutil, tempfile, zipfile, json, secrets, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
SDK=ROOT/'tools/android-sdk'
JAVA=Path(os.environ.get('JAVA_HOME','C:/Program Files/Java/jdk-23'))/'bin'
SDK_BT=SDK/'android-15'
SDK_JAR=SDK/'android-35/android.jar'
BUILD=Path(tempfile.gettempdir())/'lingo-android-build'
if BUILD.exists():
    if BUILD.resolve().parent!=Path(tempfile.gettempdir()).resolve():raise RuntimeError('Unsafe build cleanup')
    shutil.rmtree(BUILD)
BUILD.mkdir()
BT=BUILD/'sdk-tools'
JAR=BUILD/'android.jar'
shutil.copytree(SDK_BT,BT)
shutil.copy(SDK_JAR,JAR)
for name in ['classes','dex','assets','res']: (BUILD/name).mkdir()
shutil.copytree(ROOT/'www',BUILD/'assets/www')
shutil.copytree(ROOT/'android/res',BUILD/'res',dirs_exist_ok=True)
shutil.copy(ROOT/'android/AndroidManifest.xml',BUILD/'AndroidManifest.xml')
shutil.copytree(ROOT/'android/src',BUILD/'src')
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)

def run(args):
    env=dict(os.environ,JAVA_HOME=str(JAVA.parent))
    subprocess.run([str(x) for x in args],check=True,cwd=BUILD,env=env)

catalog=json.loads((ROOT/'content/catalog.json').read_text(encoding='utf-8'))
if not (ROOT/'www/app.compat.js').exists():raise RuntimeError('Run pnpm build:web before building APK')
for w in catalog['words']:
    if not (ROOT/'www/audio'/(w['id']+'.mp3')).exists():raise RuntimeError('Missing audio: '+w['id'])
run([JAVA/'javac.exe','-encoding','UTF-8','--release','8','-classpath',JAR,'-d',BUILD/'classes',*list((BUILD/'src').rglob('*.java'))])
run([JAVA/'jar.exe','cf',BUILD/'classes.jar','-C',BUILD/'classes','.'])
run([JAVA/'java.exe','-cp',BT/'lib/d8.jar','com.android.tools.r8.D8','--min-api','26','--lib',JAR,'--output',BUILD/'dex',BUILD/'classes.jar'])
run([BT/'aapt2.exe','compile','--dir',BUILD/'res','-o',BUILD/'resources.zip'])
run([BT/'aapt2.exe','link','-o',BUILD/'unsigned.apk','-I',JAR,'--manifest',BUILD/'AndroidManifest.xml','-A',BUILD/'assets','--min-sdk-version','26','--target-sdk-version','35','-0','mp3',BUILD/'resources.zip'])
# Rebuild the unsigned ZIP to keep local and central headers consistent.
# Appending with Python to aapt2's ZIP can leave data-descriptor flag mismatches.
shutil.move(BUILD/'unsigned.apk',BUILD/'resources.apk')
with zipfile.ZipFile(BUILD/'resources.apk') as source_zip, zipfile.ZipFile(BUILD/'unsigned.apk','w') as z:
    for entry in source_zip.infolist():
        clean=zipfile.ZipInfo(entry.filename,entry.date_time)
        clean.compress_type=entry.compress_type
        clean.external_attr=entry.external_attr
        z.writestr(clean,source_zip.read(entry.filename))
    z.write(BUILD/'dex/classes.dex','classes.dex',compress_type=zipfile.ZIP_DEFLATED)
run([BT/'zipalign.exe','-f','-p','4',BUILD/'unsigned.apk',BUILD/'aligned.apk'])
SIGNING=ROOT/'signing';SIGNING.mkdir(exist_ok=True)
password_file=SIGNING/'password.txt';key=SIGNING/'lingo-release.jks'
if not password_file.exists():password_file.write_text(secrets.token_urlsafe(32),encoding='ascii')
password=password_file.read_text(encoding='ascii').strip()
temp_key=BUILD/'lingo-release.jks'
temp_password=BUILD/'password.txt'
temp_password.write_text(password,encoding='ascii')
if key.exists():shutil.copy(key,temp_key)
if not key.exists():
    run([JAVA/'keytool.exe','-genkeypair','-keystore',temp_key,'-storepass',password,'-keypass',password,'-alias','lingo','-keyalg','RSA','-keysize','3072','-validity','10000','-dname','CN=Lingo Vocabulary, OU=Personal, O=LNB, C=VN'])
    shutil.copy(temp_key,key)
apk=OUT/'Lingo-SoTuVung-1.12.0.apk'
temp_apk=BUILD/'Lingo-SoTuVung-1.12.0.apk'
run([JAVA/'java.exe','-jar',BT/'lib/apksigner.jar','sign','--ks',temp_key,'--ks-key-alias','lingo','--ks-pass','file:'+str(temp_password),'--out',temp_apk,BUILD/'aligned.apk'])
run([JAVA/'java.exe','-jar',BT/'lib/apksigner.jar','verify','--verbose',temp_apk])
run([BT/'zipalign.exe','-c','-p','4',temp_apk])
shutil.copy(temp_apk,apk)
digest=hashlib.sha256(apk.read_bytes()).hexdigest()
(OUT/'SHA256.txt').write_text(digest+'  '+apk.name+'\n',encoding='utf-8')
print('APK READY:',apk,round(apk.stat().st_size/1048576,2),'MiB',flush=True)
