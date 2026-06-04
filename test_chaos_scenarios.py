"""
极端混乱场景深度测试
- 随机中断、事务性错误
- 数据一致性深度验证
- 状态异常与恢复
- 长时间压力与稳定性
"""
import sys
import os
import random
import time
import gc
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl
from src.utils.logger import get_logger

logger = get_logger()


class ChaosTester:
    """极端混乱场景测试器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failure_details = []
        
    def log_test(self, name: str, success: bool, msg: str = "", duration: float = 0):
        if success:
            self.passed += 1
            print(f"✅ PASS: {name} ({duration:.2f}s)")
        else:
            self.failed += 1
            self.failure_details.append((name, msg))
            print(f"❌ FAIL: {name}: {msg}")
    
    def test_1_transactional_consistency(self):
        """测试1：数据事务一致性（模拟中间失败）"""
        test_name = "数据事务一致性测试"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 先添加一些文档
            initial_docs = ["初始文档1 测试内容", "初始文档2 更多测试"]
            agent.add_documents(initial_docs)
            
            # 验证状态
            status1 = agent.get_status()
            assert status1["document_count"] == 2
            assert status1["vector_count"] > 0
            
            # 重置验证
            agent.reset()
            status2 = agent.get_status()
            assert status2["document_count"] == 0
            assert status2["vector_count"] == 0
            assert status2["bm25_index_size"] == 0
            
            # 再次添加验证
            agent.add_documents(["验证文档"])
            status3 = agent.get_status()
            assert status3["document_count"] == 1
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_2_rapid_state_changes(self):
        """测试2：快速状态变更（添加-查询-重置-再添加）"""
        test_name = "快速状态变更测试"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 疯狂状态变更循环
            for cycle in range(20):
                # 添加
                docs = [f"循环{cycle}文档{i} 内容测试" for i in range(5)]
                agent.add_documents(docs)
                
                # 查询
                for q in ["文档", "测试", "内容"]:
                    agent.query(q)
                
                # 检查状态
                status = agent.get_status()
                assert status["document_count"] == (cycle+1)*5
                
                if cycle % 5 == 0:
                    # 偶尔重置
                    agent.reset()
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_3_massive_data_chaos(self):
        """测试3：海量混乱数据测试"""
        test_name = "海量混乱数据测试"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 生成混乱数据
            chaos_docs = []
            for i in range(500):
                doc_type = random.randint(0, 5)
                if doc_type == 0:
                    doc = ""  # 空
                elif doc_type == 1:
                    doc = "   "  # 空白
                elif doc_type == 2:
                    doc = "A" * 5000  # 超长
                elif doc_type == 3:
                    doc = "测试 文档 内容 混合" * 100  # 重复
                elif doc_type == 4:
                    doc = "🌍🚀📚🔥" * 50  # emoji
                else:
                    doc = f"正常文档{i} 包含测试内容"
                
                chaos_docs.append(doc)
            
            # 批量添加
            agent.add_documents(chaos_docs)
            
            # 混乱查询
            for i in range(100):
                query_type = random.randint(0, 4)
                if query_type == 0:
                    q = ""
                elif query_type == 1:
                    q = "   "
                elif query_type == 2:
                    q = "测试"
                elif query_type == 3:
                    q = "🌍"
                else:
                    q = f"不存在的词{i}"
                
                result = agent.query(q)
                assert len(result) > 0
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_4_memory_stress_chaos(self):
        """测试4：内存压力与垃圾回收测试"""
        test_name = "内存压力与垃圾回收测试"
        start = time.time()
        try:
            initial_count = len(gc.get_objects())
            
            for round in range(10):
                # 每次创建新 Agent
                builder = BuilderImpl()
                agent = builder.build_agent()
                
                # 添加大量数据
                big_docs = [f"大数据文档{i} " * 100 for i in range(100)]
                agent.add_documents(big_docs)
                
                # 疯狂查询
                for i in range(50):
                    agent.query(f"查询{i}")
                
                # 强制 GC
                gc.collect()
            
            final_count = len(gc.get_objects())
            growth = final_count - initial_count
            
            print(f"内存对象变化: {initial_count} -> {final_count} (增长 {growth})")
            # 允许一定增长
            assert growth < 100000, f"内存增长过大: {growth}"
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_5_concurrent_operations_simulation(self):
        """测试5：模拟并发操作（虽然不是真实并发，但模拟混乱）"""
        test_name = "模拟并发操作测试"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 混合操作序列
            operations = []
            for i in range(100):
                op_type = random.randint(0, 3)
                if op_type == 0:
                    # 添加
                    operations.append(("add", [f"并发文档{i} 内容"]))
                elif op_type == 1:
                    # 查询
                    operations.append(("query", f"查询{i}"))
                elif op_type == 2:
                    # 检查状态
                    operations.append(("status", None))
                else:
                    # 重置
                    operations.append(("reset", None))
            
            # 执行混合序列
            for op, args in operations:
                if op == "add":
                    agent.add_documents(args)
                elif op == "query":
                    agent.query(args)
                elif op == "status":
                    agent.get_status()
                elif op == "reset":
                    agent.reset()
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_6_edge_case_hell(self):
        """测试6：地狱级边界条件"""
        test_name = "地狱级边界条件测试"
        start = time.time()
        try:
            from Text.impl.SplitterImpl import SplitterImpl
            from Retrieve.impl.RetrieverImpl import RetrieverImpl
            from Vector.impl.EmbeddingImpl import EmbeddingImpl
            from Vector.impl.StoreImpl import StoreImpl
            from Retrieve.impl.Bm25Impl import Bm25Impl
            
            # 极端分块测试
            splitter = SplitterImpl(chunk_size=1, chunk_overlap=0)
            chunks = splitter.split_text("X" * 10000)
            assert len(chunks) >= 1
            
            splitter = SplitterImpl(chunk_size=100000, chunk_overlap=99999)
            chunks = splitter.split_text("测试")
            assert len(chunks) == 1
            
            # 极端权重测试
            embedding = EmbeddingImpl()
            store = StoreImpl()
            bm25 = Bm25Impl()
            retriever = RetrieverImpl(embedding, store, bm25)
            
            # 各种极端权重
            retriever.set_semantic_weight(-1000)
            retriever.set_semantic_weight(0)
            retriever.set_semantic_weight(0.5)
            retriever.set_semantic_weight(1)
            retriever.set_semantic_weight(1000)
            
            retriever.set_keyword_weight(-1000)
            retriever.set_keyword_weight(0)
            retriever.set_keyword_weight(0.5)
            retriever.set_keyword_weight(1)
            retriever.set_keyword_weight(1000)
            
            # 超大 top_k
            retriever.retrieve("test", top_k=1000000)
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def test_7_data_persistence_validation(self):
        """测试7：数据一致性严格验证"""
        test_name = "数据一致性严格验证"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 添加一批文档
            test_docs = [
                "文档A 内容关于机器学习",
                "文档B 内容关于深度学习",
                "文档C 内容关于人工智能"
            ]
            agent.add_documents(test_docs)
            
            status1 = agent.get_status()
            doc_count1 = status1["document_count"]
            vector_count1 = status1["vector_count"]
            bm25_size1 = status1["bm25_index_size"]
            
            # 添加另一批
            more_docs = [
                "文档D 关于NLP",
                "文档E 关于CV"
            ]
            agent.add_documents(more_docs)
            
            status2 = agent.get_status()
            assert status2["document_count"] == doc_count1 + 2
            assert status2["vector_count"] > vector_count1
            assert status2["bm25_index_size"] > bm25_size1
            
            # 重置后应为0
            agent.reset()
            status3 = agent.get_status()
            assert status3["document_count"] == 0
            assert status3["vector_count"] == 0
            assert status3["bm25_index_size"] == 0
            
            self.log_test(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_test(test_name, False, str(e), time.time()-start)
    
    def run_all_chaos_tests(self):
        """运行所有混乱测试"""
        print("=" * 70)
        print("开始极端混乱场景深度测试")
        print("=" * 70)
        
        self.test_1_transactional_consistency()
        self.test_2_rapid_state_changes()
        self.test_3_massive_data_chaos()
        self.test_4_memory_stress_chaos()
        self.test_5_concurrent_operations_simulation()
        self.test_6_edge_case_hell()
        self.test_7_data_persistence_validation()
        
        print("\n" + "=" * 70)
        print("混乱场景测试总结")
        print("=" * 70)
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"总计: {self.passed + self.failed}")
        
        if self.failure_details:
            print("\n失败详情:")
            for name, msg in self.failure_details:
                print(f"  - {name}: {msg}")
        
        return self.failed == 0


if __name__ == "__main__":
    tester = ChaosTester()
    success = tester.run_all_chaos_tests()
    sys.exit(0 if success else 1)
