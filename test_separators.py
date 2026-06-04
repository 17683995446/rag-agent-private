#!/usr/bin/env python3
"""
验证优先级语义分隔符配置
"""
from src.config import RAGConfig

print("=" * 60)
print("验证优先级语义分隔符配置")
print("=" * 60)

print("\n分隔符优先级（从高到低）：")
for i, sep in enumerate(RAGConfig.CHUNK_SEPARATORS, 1):
    sep_repr = repr(sep)
    if sep == "\n\n":
        name = "段落分隔符"
    elif sep == "\n":
        name = "换行符"
    elif sep in ["。", "！", "？"]:
        name = "中文句号"
    elif sep in [".", "!", "?"]:
        name = "英文句号"
    elif sep in ["，", ","]:
        name = "逗号"
    elif sep == " ":
        name = "空格"
    else:
        name = "其他"
    
    print(f"  {i}. {sep_repr:10s} - {name}")

print("\n" + "=" * 60)
print("✅ 优先级语义分隔符配置完成")
print("优先级: 段落 → 换行 → 句号 → 逗号 → 空格")
print("=" * 60)
