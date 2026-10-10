"""Verify release identity and Android update compatibility without a connected device."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
JAVA=Path(os.environ.get('JAVA_HOME','C:/Program Files/Java/jdk-23'))/'bin/java.exe'
SDK=ROOT/'tools/android-sdk/android-15'
with tempfile.TemporaryDirectory(prefix='lingo-verify-') as tmp:
    tmp=Path(tmp);shutil.copytree(SDK,tmp/'sdk')
    certificates=[]
    for version in ['1.0.0','1.1.0','1.2.0','1.3.0','1.4.0','1.5.0']:
        apk=tmp/f'Lingo-{version}.apk';shutil.copy(ROOT/f'output/Lingo-SoTuVung-{version}.apk',apk)
        result=subprocess.run([str(JAVA),'-jar',str(tmp/'sdk/lib/apksigner.jar'),'verify','--verbose','--print-certs',str(apk)],capture_output=True,encoding='utf-8',errors='replace',check=True)
        assert 'Verified using v2 scheme (APK Signature Scheme v2): true' in result.stdout
        certificates.append(next(x.split(': ',1)[1] for x in result.stdout.splitlines() if 'certificate SHA-256 digest:' in x))
    assert len(set(certificates))==1
    badging=subprocess.run([str(tmp/'sdk/aapt2.exe'),'dump','badging',str(apk)],capture_output=True,encoding='utf-8',errors='replace',check=True).stdout
    assert "package: name='vn.lnb.sotuvung' versionCode='6' versionName='1.5.0'" in badging
    assert "minSdkVersion:'26'" in badging
    subprocess.run([str(tmp/'sdk/zipalign.exe'),'-c','-p','4',str(apk)],check=True)
report={'result':'passed','sameSigningCertificate':True,'certificateSha256':certificates[0],'versionCode':6,'versionName':'1.5.0','package':'vn.lnb.sotuvung','minSdk':26,'apkSha256':hashlib.sha256((ROOT/'output/Lingo-SoTuVung-1.5.0.apk').read_bytes()).hexdigest(),'limitation':'Metadata and signature compatibility; actual on-device update not yet tested.'}
(ROOT/'output/upgrade-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Release signature, version, minimum SDK and alignment checks passed.')
