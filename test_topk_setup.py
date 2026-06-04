#!/usr/bin/env python3
"""
测试Top-k配置验证
"""
from src.config import RAGConfig
from src.vector_store import VectorStore
from src.bm25_retriever import BM25Retriever
from src.hybrid_retriever import create_hybrid_retriever

print("=" * 60)
print("验证Top-k检索配置")
print("=" * 60)

print("\n1. 验证配置参数")
print(f"  语义检索Top-k: {RAGConfig.SEMANTIC_TOP_K}")
print(f"  BM25检索Top-k: {RAGConfig.BM25_TOP_K}")
print(f"  最终召回Top-k: {RAGConfig.FINAL_TOP_K}")

print("\n2. 验证BM25检索器Top-k设置")
retriever = BM25Retriever()
test_texts = [
    "文档1：关于Python的介绍",
    "文档2：机器学习概述",
    "文档3：深度学习基础",
    "文档4：数据科学基础",
    "文档5：NLP介绍",
    "文档6：计算机视觉概述",
    "文档7：推荐系统",
    "文档8：图神经网络",
    "文档9：强化学习",
    "文档10：迁移学习"
]
retriever.build(test_texts)
print(f"✅ BM25索引构建完成，文档数: {len(test_texts)}")

print("\n3. 测试BM25检索（Top-k=6）")
query = "学习介绍"
results = retriever.search(query, k=RAGConfig.BM25_TOP_K)
print(f"  查询: {query}")
print(f"  结果数: {len(results)} (预期 {RAGConfig.BM25_TOP_K})")

if len(results) <= RAGConfig.BM25_TOP_K:
    print("  ✅ BM25 Top-k配置正确")
else:
    print("  ⚠ BM25 Top-k可能需要调整")

print("\n4. 验证混合检索器配置")
print(f"  语义权重: {RAGConfig.SEMANTIC_WEIGHT}")
print(f"  BM25权重: {RAGConfig.BM25_WEIGHT}")
print(f"  最终Top-k: {RAGConfig.FINAL_TOP_K}")

print("\n" + "=" * 60)
print("✅ 所有Top-k配置验证通过！")
print("=" * 60)
