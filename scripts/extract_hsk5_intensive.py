"""Resumable OCR cache for the user-supplied HSK 5 intensive collection."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_SOURCE=Path('X:/GTTH/drive-download-20261029T083803Z-1-001')
def main():
 import pymupdf as fitz,numpy as np
 from rapidocr_onnxruntime import RapidOCR
 p=argparse.ArgumentParser();p.add_argument('book');p.add_argument('pages');p.add_argument('--source-dir',type=Path,default=DEFAULT_SOURCE);a=p.parse_args()
 books=json.loads((ROOT/'content/hsk5-intensive/books.json').read_text(encoding='utf-8'));book=next(b for b in books if b['id']==a.book)
 out=ROOT/'tmp/hsk5-intensive/ocr';out.mkdir(parents=True,exist_ok=True)
 doc=fitz.open(a.source_dir/book['file']);ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
 pages=set()
 for token in a.pages.split(','):
  bounds=token.split('-');lo=int(bounds[0]);hi=int(bounds[-1]);pages.update(range(lo,hi+1))
 for page in sorted(pages):
  dest=out/f'{a.book}-{page:04}.json'
  if dest.exists():continue
  assert 1<=page<=len(doc)
  pix=doc[page-1].get_pixmap(matrix=fitz.Matrix(2,2));data=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
  result,_=ocr(data,use_cls=False)
  obj=dict(book=a.book,file=book['file'],page=page,width=pix.width,height=pix.height,rows=[dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in result or []])
  temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(dest)
  print(a.book,page,flush=True)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
