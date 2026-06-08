from wos_clean import WOSCleaner
from disambiguate import AuthorDisambiguator, PaperDeduplicator, KeywordDisambiguator
import pandas as pd

INPUT_DIR = r"D:\共被引分析\input"
OUTPUT_FILE = r"D:\共被引分析\wos_cleaned.csv"

# 初始化
cleaner = WOSCleaner()
author_dis = AuthorDisambiguator()
paper_dis = PaperDeduplicator()
kw_dis = KeywordDisambiguator()

# 1️⃣ 读数据
records = cleaner.parse_wos_folder(INPUT_DIR)

cleaned = []
for r in records:
    rec = cleaner.clean_record(r)

    # 2️⃣ 消歧
    rec["paper_id"] = paper_dis.deduplicate(rec)
    rec["author_ids"] = [author_dis.disambiguate(a) for a in rec["authors"]]
    rec["keyword_ids"] = [kw_dis.disambiguate(k) for k in rec["keywords"]]

    cleaned.append(rec)

# 3️⃣ 输出
df = pd.DataFrame(cleaned)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("✅ 清洗 + 消歧完成")
print("📄 输出文件：", OUTPUT_FILE)
print("📊 记录数：", len(df))