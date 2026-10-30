# -*- coding: utf-8 -*-
"""检查 college.db 实况与前端 AI/预测逻辑细节"""
import pathlib
import re
import sqlite3

DB = pathlib.Path(r"C:\Users\郭耀彬\Desktop\gybct\chatbot-main\chatbot-main\college-ai-erp\database\college.db")
T = pathlib.Path(r"C:\Users\郭耀彬\Desktop\gybct\chatbot-main\chatbot-main\college-ai-erp\templates")

print("=== college.db 表与行数 ===")
conn = sqlite3.connect(str(DB))
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("tables:", tables)
for t in tables:
    try:
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} 行")
    except Exception as e:
        print(f"  {t}: 查询失败 {e}")
conn.close()

print("\n=== dashboard.html /chat 上下文 ===")
text = pathlib.Path(T / "dashboard.html").read_text(encoding="utf-8", errors="replace")
m = re.search(r"/chat[\s\S]{0,400}", text)
print(m.group(0)[:450] if m else "无")

print("\n=== prediction.html 关键逻辑 ===")
ptext = pathlib.Path(T / "prediction.html").read_text(encoding="utf-8", errors="replace")
print("  /chat 引用:", "/chat" in ptext, "| fetch:", len(re.findall(r"fetch\(", ptext)), "处")
for mm in re.findall(r"fetch\([\s\S]{0,120}", ptext)[:3]:
    print("  ", mm.replace("\n", " ")[:130])

print("\n=== analytics.html 图表 ===")
atext = pathlib.Path(T / "analytics.html").read_text(encoding="utf-8", errors="replace")
print("  chart 引用:", re.findall(r"(Chart\.[A-Za-z]+|new Chart|\.png|chart\.js)", atext)[:8])
print("  /api 引用:", sorted(set(re.findall(r"['\"]/(api|analytics|dashboard)[^'\"]*['\"]", atext))))

print("\n=== 文件规模 ===")
for p in sorted(T.glob("*.html")):
    print(f"  {p.name}: {len(p.read_text(encoding='utf-8', errors='replace'))} 字符")
