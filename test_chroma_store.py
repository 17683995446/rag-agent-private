"""
ChromaDB存储集成测试
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Vector.impl.ChromaStoreImpl import ChromaStoreImpl


def test_chroma_basic():
    """测试ChromaDB基本功能"""
    print("="*60)
    print("测试: ChromaDB基本功能")
    print("="*60)
    
    try:
        # 创建存储
        store = ChromaStoreImpl(collection_name="test_collection")
        print("✅ ChromaStore创建成功")
        
        # 添加向量
        texts = ["文档1 人工智能", "文档2 机器学习", "文档3 深度学习"]
        vectors = [[0.1]*384, [0.2]*384, [0.3]*384]
        metadatas = [{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}]
        
        store.add_vectors(texts, vectors, metadatas)
        count = store.get_count()
        print(f"✅ 添加向量成功，当前数量: {count}")
        assert count == 3, f"期望3个向量，实际{count}"
        
        # 搜索
        results = store.search([0.15]*384, top_k=2)
        print(f"✅ 搜索成功，返回{len(results)}个结果")
        assert len(results) > 0, "搜索结果不应为空"
        
        # 删除
        store.delete_all()
        count = store.get_count()
        print(f"✅ 删除成功，当前数量: {count}")
        assert count == 0, f"期望0个向量，实际{count}"
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


def test_chroma_with_builder():
    """测试通过Builder使用ChromaDB"""
    print("\n" + "="*60)
    print("测试: 通过Builder使用ChromaDB")
    print("="*60)
    
    try:
        from Rag.impl.BuilderImpl import BuilderImpl
        
        builder = BuilderImpl()
        agent = builder.build_agent_with_chroma(collection_name="test_rag")
        print("✅ Agent构建成功（带ChromaDB）")
        
        # 添加文档
        docs = ["人工智能是计算机科学的一个分支", "机器学习是人工智能的子领域"]
        agent.add_documents(docs)
        
        status = agent.get_status()
        print(f"✅ 文档添加成功，状态: {status}")
        
        # 查询
        result = agent.query("什么是人工智能")
        print(f"✅ 查询成功，结果: {result[:100]}...")
        
        # 重置
        agent.reset()
        status = agent.get_status()
        print(f"✅ 重置成功，状态: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("ChromaDB集成测试")
    print("="*60)
    
    results = []
    results.append(("基本功能", test_chroma_basic()))
    results.append(("Builder集成", test_chroma_with_builder()))
    
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
