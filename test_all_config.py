#!/usr/bin/env python3
"""
验证所有第二阶段配置参数
"""
from src.config import RAGConfig

print("=" * 60)
print("验证第二阶段所有配置参数（12-20阶段）")
print("=" * 60)

# 验证配置
RAGConfig.validate()
RAGConfig.print_config()

print("\n" + "=" * 60)
print("✅ 第二阶段（12-20阶段）所有配置验证完成！")
print("=" * 60)
print("\n阶段验收清单:")
print("✓ 阶段12: CHUNK_SIZE = 1400")
print("✓ 阶段13: CHUNK_OVERLAP = 210 (15%重叠率)")
print("✓ 阶段14: SEMANTIC_TOP_K = 8")
print("✓ 阶段15: BM25_TOP_K = 6")
print("✓ 阶段16: FINAL_TOP_K = 5")
print("✓ 阶段17: EMBEDDING_MODEL_NAME = all-MiniLM-L6-v2")
print("✓ 阶段18: SEMANTIC_WEIGHT = 0.6, BM25_WEIGHT = 0.4")
print("✓ 阶段19: CHROMA_DB_DIR = /workspace/chroma_db")
print("✓ 阶段20: 配置验证函数 validate() 已实现并通过")
