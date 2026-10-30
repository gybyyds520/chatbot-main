# -*- coding: utf-8 -*-
"""提取 chatbot 前端页面引用的后端路由接口，还原缺失主程序的功能面。"""
import pathlib
import re

T = pathlib.Path(r"C:\Users\郭耀彬\Desktop\gybct\chatbot-main\chatbot-main\college-ai-erp\templates")
PATTERNS = [
    (r"url_for\('([^']+)'\)", "url_for"),
    (r"action\s*=\s*['\"]([^'\"]+)['\"]", "action"),
    (r"fetch\(['\"]([^'\"]+)['\"]", "fetch"),
    (r"href=['\"](/[^'\"]*)['\"]", "href"),
    (r"src=['\"](/[^'\"]*)['\"]", "src"),
    (r"@app\.route\('([^']+)'\)", "route"),
]

for f in sorted(T.glob("*.html")):
    print(f"=== {f.name} ===")
    text = f.read_text(encoding="utf-8", errors="replace")
    seen = set()
    for pattern, label in PATTERNS:
        for m in re.findall(pattern, text):
            key = (label, m)
            if key not in seen:
                seen.add(key)
                print(f"  [{label}] {m}")
    if not seen:
        print("  (无后端接口引用)")
