#!/usr/bin/env python3
"""
验证所有包版本兼容性
"""

import sys
import traceback

print("=" * 50)
print("开始验证所有包版本兼容性")
print("=" * 50)
print(f"Python版本: {sys.version}")
print()

# 测试所有需要导入的包
test_modules = [
    ("langchain", "LangChain"),
    ("langchain_core", "LangChain Core"),
    ("chromadb", "ChromaDB"),
    ("sentence_transformers", "Sentence-Transformers"),
    ("rank_bm25", "Rank-BM25"),
    ("numpy", "NumPy"),
    ("transformers", "Transformers"),
    ("torch", "PyTorch"),
]

all_success = True

for module, name in test_modules:
    try:
        __import__(module)
        print(f"✅ {name} - 导入成功")
    except ImportError as e:
        print(f"❌ {name} - 导入失败: {e}")
        all_success = False
    except Exception as e:
        print(f"❌ {name} - 导入异常: {e}")
        all_success = False

print()
print("=" * 50)
print("测试各模块协同工作")
print("=" * 50)

# 测试 LangChain + ChromaDB
try:
    from langchain_chroma import Chroma
    print("✅ LangChain Chroma 模块 - 导入成功")
except Exception as e:
    print(f"❌ LangChain Chroma 模块 - 导入失败: {e}")
    traceback.print_exc()
    all_success = False

# 测试 Sentence-Transformers 嵌入模型
try:
    from sentence_transformers import SentenceTransformer
    print("✅ Sentence-Transformers 模型 - 导入成功")
except Exception as e:
    print(f"❌ Sentence-Transformers 模型 - 导入失败: {e}")
    traceback.print_exc()
    all_success = False

# 测试 BM25
try:
    from rank_bm25 import BM25Okapi
    corpus = [
        "Hello there good man!",
        "It is quite windy in London",
        "How is the weather today?"
    ]
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    query = "windy London"
    tokenized_query = query.split(" ")
    scores = bm25.get_scores(tokenized_query)
    print(f"✅ BM25 功能测试 - 正常运行，得分为: {scores}")
except Exception as e:
    print(f"❌ BM25 功能测试 - 失败: {e}")
    traceback.print_exc()
    all_success = False

print()
print("=" * 50)
if all_success:
    print("✅ 所有包版本兼容性验证通过！")
else:
    print("❌ 部分包版本兼容性验证失败！")
print("=" * 50)

sys.exit(0 if all_success else 1)
