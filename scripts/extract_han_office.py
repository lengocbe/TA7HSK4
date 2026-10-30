"""Cache read-only OCR of user supplied Han/office textbooks."""
from pathlib import Path
import argparse,json,sys
FILES={**{str(i):f'HAN {i}.pdf' for i in range(1,7)},'office':'Giáo trình chuẩn tiếng Trung công sở.pdf'}
ROOT=Path(__file__).resolve().parents[1]
def main():
 import pymupdf as f,numpy as np
 from rapidocr_onnxruntime import RapidOCR
 p=argparse.ArgumentParser();p.add_argument('book',choices=FILES);p.add_argument('pages');p.add_argument('--source-dir',type=Path,default=Path('X:/Han'));a=p.parse_args()
 out=ROOT/'tmp/han/ocr';out.mkdir(parents=True,exist_ok=True);d=f.open(a.source_dir/FILES[a.book]);ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
 pages=[]
 for s in a.pages.split(','):
  if '-' in s:lo,hi=map(int,s.split('-'));pages.extend(range(lo,hi+1))
  else:pages.append(int(s))
 for n in sorted(set(pages)):
  dest=out/f'{a.book}-{n:03}.json'
  if dest.exists():continue
  pix=d[n-1].get_pixmap(matrix=f.Matrix(2,2));rs,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  dest.write_text(json.dumps(dict(width=pix.width,height=pix.height,rows=[dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in rs or []]),ensure_ascii=False,indent=2),encoding='utf-8');print(a.book,n,flush=True)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
