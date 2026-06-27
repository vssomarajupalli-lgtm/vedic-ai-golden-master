import json

def test():
    with open("D:/HoroscopeCleaner_Final/OUTPUT/raju_canonical_content.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    pages = data.get("pages", [])
    
    bav_tables = []
    sav_table = None
    
    for p in pages:
        blocks = p.get("content_blocks", [])
        for i, b in enumerate(blocks):
            if b["type"] == "table":
                rows = b["rows"]
                for r in rows:
                    txt = " ".join([str(c) for c in r])
                    if "సాముదాయక" in txt and ("అష్టకవర్గ" in txt or "అషటకవరు" in txt):
                        sav_table = rows
                        break
                    elif "అషటకవరగ" in txt or "అష్టకవర్గ" in txt:
                        if "సాముదాయక" not in txt:
                            # get all text blocks before this table in the page
                            prev_txts = [blk.get("text", "") for blk in blocks[:i] if blk["type"] in ["text", "heading"]]
                            bav_tables.append({"rows": rows, "prev": prev_txts})
                            break

    print(f"Found {len(bav_tables)} BAV tables.")
    if bav_tables:
        print("BAV Table 0:")
        for r in bav_tables[0]['rows']:
            print(r)
        
    if sav_table:
        print("Found SAV table:")
        for r in sav_table:
            print(r)

test()
