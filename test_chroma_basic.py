#!/usr/bin/env python3
"""
基础Chroma向量库测试（禁用自动下载
只测试集合管理功能
"""
from chromadb import Client
from chromadb.config import Settings
from src.config import RAGConfig

print("=" * 60)
print("测试Chroma向量库基础功能")
print("=" * 60)

print("\n1. 初始化内存Chroma客户端")
client = Client(Settings(anonymized_telemetry=False))
print("✅ 内存Chroma客户端初始化成功")

print("\n2. 创建测试集合")
collection = client.create_collection(
    name="test_collection",
    metadata={"description": "测试集合"}
)
print("✅ 测试集合创建成功")

print("\n3. 只测试集合管理（不添加文档）")
count = collection.count()
print(f"✅ 集合为空，文档数: {count}")

print("\n4. 测试查询集合元数据")
print(f"  集合名: {collection.name}")
print(f"  集合元数据: {collection.metadata}")

print("\n5. 测试集合操作")
all_collections = client.list_collections()
print(f"  所有集合数: {len(all_collections)}")

print("\n6. 测试删除集合")
client.delete_collection("test_collection")
print("✅ 集合删除成功")

print("\n7. 验证本地持久化目录")
print(f"  持久化目录: {RAGConfig.CHROMA_DB_DIR}")
if not RAGConfig.CHROMA_DB_DIR.exists():
    RAGConfig.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
    print("✅ 持久化目录创建成功")
else:
    print("✅ 持久化目录已存在")

print("\n" + "=" * 60)
print("✅ Chroma基础功能测试通过！")
print("=" * 60)
