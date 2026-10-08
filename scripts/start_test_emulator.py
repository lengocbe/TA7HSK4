"""Start the dedicated test AVD in a hidden window with software emulation."""
from pathlib import Path
import tempfile,subprocess,os,time
ROOT=Path(__file__).resolve().parents[1]
tmp=Path(tempfile.gettempdir());sdk=tmp/'lingo-stable-emulator-sdk';emu=sdk/'emulator'
avdroot=tmp/'lingo-test-avd';avd=avdroot/'LingoTest.avd'
avd.mkdir(parents=True,exist_ok=True)
(avdroot/'LingoTest.ini').write_text('avd.ini.encoding=UTF-8\npath='+str(avd)+'\ntarget=android-28\n')
if not (avd/'config.ini').exists():
    (avd/'config.ini').write_text('AvdId=LingoTest\nabi.type=x86_64\nhw.cpu.arch=x86_64\nhw.cpu.ncore=2\nhw.ramSize=1536\nhw.lcd.width=1080\nhw.lcd.height=1920\nhw.lcd.density=420\nhw.gpu.enabled=yes\nhw.gpu.mode=swiftshader_indirect\nhw.keyboard=yes\nhw.mainKeys=no\nimage.sysdir.1=system-images/android-28/default/x86_64/\ntag.id=default\ndisk.dataPartition.size=512M\n')
env=dict(os.environ,ANDROID_HOME=str(sdk),ANDROID_SDK_ROOT=str(sdk),ANDROID_AVD_HOME=str(avdroot))
env['PATH']=';'.join(str(p) for p in [emu,emu/'lib64',emu/'lib64/qt/lib',emu/'qemu/windows-x86_64'])+';'+env['PATH']
log=open(ROOT/'tmp/emulator-stable.log','w');err=open(ROOT/'tmp/emulator-stable-error.log','w')
args=[str(emu/'emulator.exe'),'-avd','LingoTest','-no-window','-no-audio','-no-boot-anim','-no-snapshot','-accel','off','-cores','1','-gpu','off','-camera-back','none','-camera-front','none','-show-kernel','-qemu','-cpu','qemu64,+ssse3,+sse4.1,+sse4.2']
proc=subprocess.Popen(args,env=env,cwd=emu,stdin=subprocess.DEVNULL,stdout=log,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
time.sleep(3)
print('Headless Android test emulator PID',proc.pid,'status',proc.poll(),flush=True)
(ROOT/'tmp/emulator-pid.txt').write_text(str(proc.pid))
