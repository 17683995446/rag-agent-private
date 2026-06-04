#!/usr/bin/env python3
"""
测试分片核心参数配置
"""
from src.config import RAGConfig

print("=" * 60)
print("验证分片核心参数")
print("=" * 60)

# 验证配置
RAGConfig.validate()

# 打印分片配置
print(f"\n✅ 分片核心参数已固化:")
print(f"   CHUNK_SIZE = {RAGConfig.CHUNK_SIZE}")
print(f"   CHUNK_OVERLAP = {RAGConfig.CHUNK_OVERLAP}")
print(f"   重叠率 = {(RAGConfig.CHUNK_OVERLAP / RAGConfig.CHUNK_SIZE * 100):.1f}%")
print(f"\n   分隔符优先级:")
for i, sep in enumerate(RAGConfig.CHUNK_SEPARATORS, 1):
    print(f"   {i}. {repr(sep)}")

print("\n" + "=" * 60)
print("✅ 分片核心参数验证通过！")
print("=" * 60)
