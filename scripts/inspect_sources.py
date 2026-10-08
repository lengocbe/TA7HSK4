"""Extract source text and OCR the scanned English glossary for editorial review."""
from pathlib import Path
import json, sys
import pypdfium2 as pdfium
from pypdf import PdfReader
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tmp' / 'sources'
OUT.mkdir(parents=True, exist_ok=True)
ocr = RapidOCR()
book = pdfium.PdfDocument('D:/Desktop/Tiếng Anh 7 Global Success.pdf')
for i in [9,10,11,137,138,139,140,141,142]:
    image = book[i].render(scale=2.3).to_pil()
    path = OUT / f'english-{i+1}.png'
    image.save(path)
    result, _ = ocr(str(path))
    lines = [{'text': row[1], 'confidence': float(row[2]), 'box': row[0]} for row in (result or [])]
    (OUT / f'english-{i+1}.json').write_text(json.dumps(lines, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PAGE', i+1, '\n'+'\n'.join(x['text'] for x in lines), flush=True)
for path in sorted(Path('D:/Desktop/SSS').glob('H4*.pdf')):
    reader = PdfReader(path)
    pages = [{'page':i+1,'text':p.extract_text() or ''} for i,p in enumerate(reader.pages)]
    (OUT / (path.stem+'.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
print('Source extraction completed',flush=True)
