"""Read the two word-list columns independently to avoid joined one-character words."""
from pathlib import Path
import json,sys
import pymupdf as f,numpy as np
from rapidocr_onnxruntime import RapidOCR
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'tmp/hsk5-intensive/grid';out.mkdir(parents=True,exist_ok=True)
doc=f.open(Path('X:/GTTH/drive-download-20261029T083803Z-1-001/HSK5词汇精讲精练.pdf'))
ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
for n in ([int(v) for v in sys.argv[1:]] if len(sys.argv)>1 else range(1,82)):
 dest=out/f'{n:02}.json'
 if dest.exists():continue
 page=9+4*(n-1);pg=doc[page-1];items=[]
 for left,right in [(.27,.49),(.55,.78)]:
  clip=f.Rect(left*pg.rect.width,.58*pg.rect.height,right*pg.rect.width,.94*pg.rect.height)
  pix=pg.get_pixmap(matrix=f.Matrix(6,6),clip=clip);im=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
  rs,_=ocr(im,use_cls=False)
  items.extend(dict(text=r[1],confidence=float(r[2]),box=r[0],column=left) for r in rs or [])
 dest.write_text(json.dumps(dict(page=page,unit=n,rows=items),ensure_ascii=False,indent=2),encoding='utf-8');print(n,len(items),flush=True)
