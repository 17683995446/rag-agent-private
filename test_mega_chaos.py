"""
超大规模混乱场景测试
- 10000+ 文档
- 随机中断
- 错误注入
- 状态混乱
"""
import sys
import os
import random
import time
import gc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl


def test_mega_scale():
    """超大规模测试: 10000+ 文档"""
    print("="*70)
    print("测试: 超大规模 (10000+ 文档)")
    print("="*70)
    
    try:
        builder = BuilderImpl()
        agent = builder.build_agent()
        
        # 生成10000个文档
        total_docs = 10000
        batch_size = 500
        
        start = time.time()
        for batch in range(total_docs // batch_size):
            docs = [f"大规模文档 batch{batch}_doc{i} 内容测试 " * 5 
                   for i in range(batch_size)]
            agent.add_documents(docs)
            
            if (batch + 1) % 5 == 0:
                print(f"  已完成 {(batch+1)*batch_size}/{total_docs} 文档")
        
        add_time = time.time() - start
        
        status = agent.get_status()
        print(f"✅ 添加完成: {status['document_count']} 文档, 耗时 {add_time:.1f}s")
        
        # 大量查询
        query_start = time.time()
        for i in range(1000):
            agent.query(f"查询测试 {random.randint(1, 1000)}")
        query_time = time.time() - query_start
        print(f"✅ 1000次查询完成, 耗时 {query_time:.1f}s")
        
        # 重置
        agent.reset()
        status = agent.get_status()
        assert status['document_count'] == 0
        print(f"✅ 重置后状态正确")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_chaos_operations():
    """混乱操作测试"""
    print("\n" + "="*70)
    print("测试: 混乱操作序列")
    print("="*70)
    
    try:
        builder = BuilderImpl()
        agent = builder.build_agent()
        
        operations = 5000
        errors = 0
        
        for i in range(operations):
            try:
                op = random.randint(0, 6)
                
                if op == 0:
                    # 正常添加
                    agent.add_documents([f"文档{i}"])
                elif op == 1:
                    # 空添加
                    agent.add_documents([])
                elif op == 2:
                    # 查询
                    agent.query(f"查询{i}")
                elif op == 3:
                    # 空查询
                    agent.query("")
                elif op == 4:
                    # 获取状态
                    agent.get_status()
                elif op == 5:
                    # 重置（偶尔）
                    if random.random() < 0.05:
                        agent.reset()
                else:
                    # 检查就绪
                    agent.is_ready()
                    
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"  操作{i}异常: {str(e)[:80]}")
        
        print(f"✅ {operations}次操作完成, 错误: {errors} ({errors/operations*100:.2f}%)")
        return errors < operations * 0.01  # 错误率<1%
        
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        return False


def test_memory_stability():
    """内存稳定性测试"""
    print("\n" + "="*70)
    print("测试: 内存稳定性")
    print("="*70)
    
    try:
        initial = len(gc.get_objects())
        
        for round in range(20):
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 添加数据
            docs = [f"内存测试{i}" * 50 for i in range(200)]
            agent.add_documents(docs)
            
            # 查询
            for _ in range(100):
                agent.query("测试")
            
            # 重置
            agent.reset()
            gc.collect()
        
        final = len(gc.get_objects())
        growth = final - initial
        print(f"✅ 内存对象增长: {growth} (初始{initial} -> 最终{final})")
        return growth < 1000000
        
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        return False


def main():
    print("="*70)
    print("超大规模混乱场景测试")
    print("="*70)
    
    results = []
    results.append(("超大规模", test_mega_scale()))
    results.append(("混乱操作", test_chaos_operations()))
    results.append(("内存稳定性", test_memory_stability()))
    
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    
    passed = sum(1 for _, r in results if r)
    for name, result in results:
        print(f"{'✅' if result else '❌'} {name}")
    
    print(f"\n总计: {passed}/{len(results)} 通过")
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
