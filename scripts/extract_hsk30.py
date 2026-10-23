"""Read-only OCR cache for supplied New HSK Course PDF pages."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
FILES={'1':'新HSK1教程3.0 (Ban dep)_983a0d8e5bc691cfe23ee0f230cd12eb.pdf','2':'New HSK Course 2 (HSK3.0)_5fd2480441d0188f0146a064f46d9bf5.pdf','3':'New HSK Course 3 (HSK3.0)_05ef5108197b72f8449132f026e4f09f.pdf','4.1':'New_HSK_Course_Textbook_4_1_HSK3_0_62f6b1437a7279090c330aa944369695.pdf','4.2':'New_HSK_Course_Textbook_4_2_HSK3_0_d7d2d9f65253bd5f18956b8ec25b822f.pdf'}
def main():
 import pymupdf as f,numpy as np
 from rapidocr_onnxruntime import RapidOCR
 p=argparse.ArgumentParser();p.add_argument('book',choices=FILES);p.add_argument('pages',help='Comma separated pages or inclusive ranges');p.add_argument('--source-dir',type=Path,default=Path('D:/LeNgocBE/Download/Telegram Desktop'));a=p.parse_args()
 out=ROOT/'tmp/hsk30';out.mkdir(parents=True,exist_ok=True);d=f.open(a.source_dir/FILES[a.book]);ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
 pages=[]
 for s in a.pages.split(','):
  if '-' in s:lo,hi=map(int,s.split('-'));pages.extend(range(lo,hi+1))
  else:pages.append(int(s))
 for n in sorted(set(pages)):
  dest=out/f'{a.book}-{n:03}.json'
  if dest.exists():continue
  pix=d[n-1].get_pixmap(matrix=f.Matrix(1.5,1.5));rs,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  dest.write_text(json.dumps([dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in rs or []],ensure_ascii=False,indent=2),encoding='utf-8');print(a.book,n,flush=True)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
