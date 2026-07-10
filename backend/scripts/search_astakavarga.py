import json

with open('d:/HoroscopeCleaner_Final/OUTPUT/B.Rajasekhar Reddy_canonical_content.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for p in d['pages']:
    for b in p['content_blocks']:
        if b['type'] == 'table':
            text = ''.join(''.join(str(c) for c in r) for r in b['rows']).replace(' ', '')
            if 'అష' in text and 'కవర' in text:
                try:
                    print(f"Page {p.get('physical_page_number', '?')} / Canonical {p.get('canonical_page_number', '?')}")
                    for r in b['rows'][:15]:
                        print(r)
                    print('-'*40)
                except Exception:
                    pass
