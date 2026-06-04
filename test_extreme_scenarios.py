"""
极端复杂场景深度测试
- 极端边界条件
- 大规模数据
- 压力测试
- 并发/多轮测试
- 错误注入
- 内存和性能监控
"""
import sys
import os
import time
import gc
import random
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl
from src.utils.logger import get_logger

logger = get_logger()


class ExtremeTester:
    """极端场景测试器"""
    
    def __init__(self):
        self.all_passed = 0
        self.all_failed = 0
        self.test_results = []
        
    def log_result(self, test_name: str, passed: bool, msg: str = "", duration: float = 0):
        """记录测试结果"""
        self.test_results.append({
            "name": test_name,
            "passed": passed,
            "message": msg,
            "duration": duration
        })
        if passed:
            self.all_passed += 1
            print("="*60)
            print(f"✅ PASS: {test_name} ({duration:.3f}s)")
            print("="*60)
        else:
            self.all_failed += 1
            print("="*60)
            print(f"❌ FAIL: {test_name}")
            print(msg)
            print("="*60)
    
    def test_1_empty_inputs(self):
        """测试 1: 各种空输入场景"""
        test_name = "test_1_empty_inputs"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 测试空查询
            result = agent.query("")
            assert "错误" in result or len(result) > 0
            
            # 测试空文档列表
            agent.add_documents([])
            
            # 测试全是空白的文档
            agent.add_documents(["   ", "", "\n", "\t"])
            
            status = agent.get_status()
            assert status["document_count"] == 0
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_2_giant_documents(self):
        """测试 2: 超大规模文档"""
        test_name = "test_2_giant_documents"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 1000 字符的文档
            large_text = "a" * 1000 + " 测试人工智能技术" + "b" * 1000
            
            # 500 个这样的文档
            docs = [large_text for _ in range(500)]
            agent.add_documents(docs)
            
            status = agent.get_status()
            assert status["document_count"] == 500
            assert status["vector_count"] > 500
            assert status["bm25_index_size"] > 500
            
            result = agent.query("人工智能")
            assert len(result) > 0
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_3_consecutive_operations(self):
        """测试 3: 连续操作压力测试"""
        test_name = "test_3_consecutive_operations"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 连续多次添加文档
            for i in range(50):
                docs = [f"文档 {i} 内容: 人工智能 {random.random()}", 
                        f"机器学习 {random.random()}", 
                        f"深度学习 {random.random()}"]
                agent.add_documents(docs)
            
            status = agent.get_status()
            assert status["document_count"] == 150
            
            # 连续多次查询
            queries = ["人工智能", "机器学习", "深度学习", "测试", "其他"]
            for _ in range(100):
                for q in queries:
                    result = agent.query(q)
                    assert len(result) > 0
            
            # 重置再继续
            agent.reset()
            status = agent.get_status()
            assert status["document_count"] == 0
            
            agent.add_documents(["新文档内容"])
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_4_edge_chunk_sizes(self):
        """测试 4: 极端分片大小"""
        test_name = "test_4_edge_chunk_sizes"
        start = time.time()
        try:
            from Text.impl.SplitterImpl import SplitterImpl
            
            splitter = SplitterImpl(chunk_size=1, chunk_overlap=0)
            chunks = splitter.split_text("测试文本内容")
            assert len(chunks) > 0
            
            splitter = SplitterImpl(chunk_size=100000, chunk_overlap=0)
            chunks = splitter.split_text("短文本")
            assert len(chunks) == 1
            
            splitter.set_chunk_size(0)  # 会自动修正为 1
            chunks = splitter.split_text("a")
            assert len(chunks) == 1
            
            splitter.set_chunk_overlap(1000)
            assert splitter._chunk_overlap == 0
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_5_retrieval_weights(self):
        """测试 5: 权重设置和边界值"""
        test_name = "test_5_retrieval_weights"
        start = time.time()
        try:
            builder = BuilderImpl()
            builder.initialize_components()
            
            # 测试极端权重
            builder._retriever.set_semantic_weight(-100)  # 应该修正为 0
            builder._retriever.set_semantic_weight(100)   # 应该修正为 1
            builder._retriever.set_semantic_weight(0.5)
            
            # 测试关键词权重
            builder._retriever.set_keyword_weight(-100)
            builder._retriever.set_keyword_weight(100)
            builder._retriever.set_keyword_weight(0.7)
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_6_memory_stress(self):
        """测试 6: 内存压力测试（创建和释放）"""
        test_name = "test_6_memory_stress"
        start = time.time()
        try:
            initial_objects = len(gc.get_objects())
            
            for i in range(10):
                builder = BuilderImpl()
                agent = builder.build_agent()
                docs = [f"测试文档 {j}" for j in range(100)]
                agent.add_documents(docs)
                agent.query("测试")
                agent.reset()
                
                # 强制垃圾回收
                gc.collect()
            
            final_objects = len(gc.get_objects())
            diff = abs(final_objects - initial_objects)
            # 允许一定的增量
            assert diff < 50000, f"对象数量增长过大: {diff}"
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_7_invalid_input_types(self):
        """测试 7: 错误输入类型"""
        test_name = "test_7_invalid_input_types"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            try:
                agent.add_documents(None)  # type: ignore
            except Exception as e:
                print(f"TypeError expected: {e}")
            
            try:
                agent.query(None)  # type: ignore
            except Exception as e:
                print(f"TypeError expected: {e}")
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_8_unicode_and_special_chars(self):
        """测试 8: Unicode 和特殊字符"""
        test_name = "test_8_unicode_and_special_chars"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            special_docs = [
                "🌍 全球人工智能应用 🚀",
                "测试\t换行符\n中文\n",
                "Mix of 中文 and English",
                '符号测试: "‘’“”„‟',
                "日文: 日本語 カタカナ",
                "数学: ∑∞n=1 1/n² = π²/6",
                "🤖 AI in 2024 and beyond!"
            ]
            
            agent.add_documents(special_docs)
            
            # 特殊查询
            result = agent.query("🌍")
            assert len(result) > 0
            result = agent.query("日本語")
            assert len(result) > 0
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_9_rapid_successive_queries(self):
        """测试 9: 快速连续查询"""
        test_name = "test_9_rapid_successive_queries"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            agent.add_documents(["测试文档 1", "测试文档 2"])
            
            # 1000 次快速查询
            results = []
            for i in range(1000):
                query = f"测试查询 {i}"
                result = agent.query(query)
                results.append(result)
                if i % 100 == 0:
                    print(f"Query {i} completed")
            
            assert len(results) == 1000
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def test_10_data_consistency(self):
        """测试 10: 数据一致性检查"""
        test_name = "test_10_data_consistency"
        start = time.time()
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 添加 3 批文档，每批 50 个
            total_docs = 0
            for batch in range(3):
                docs = [f"Batch {batch} Doc {i}" for i in range(50)]
                agent.add_documents(docs)
                total_docs += 50
            
            status = agent.get_status()
            assert status["document_count"] == 150, f"Expected 150, got {status['document_count']}"
            
            # 重置
            agent.reset()
            status = agent.get_status()
            assert status["document_count"] == 0
            assert status["vector_count"] == 0
            assert status["bm25_index_size"] == 0
            
            # 再次添加
            agent.add_documents(["验证文档"])
            status = agent.get_status()
            assert status["document_count"] == 1
            
            self.log_result(test_name, True, duration=time.time()-start)
        except Exception as e:
            self.log_result(test_name, False, str(e), time.time()-start)
    
    def run_all(self):
        """运行所有极端测试"""
        print("="*60)
        print("开始极端复杂场景深度测试")
        print("="*60)
        
        self.test_1_empty_inputs()
        self.test_2_giant_documents()
        self.test_3_consecutive_operations()
        self.test_4_edge_chunk_sizes()
        self.test_5_retrieval_weights()
        self.test_6_memory_stress()
        self.test_7_invalid_input_types()
        self.test_8_unicode_and_special_chars()
        self.test_9_rapid_successive_queries()
        self.test_10_data_consistency()
        
        print("\n" + "="*60)
        print("极端场景测试总结")
        print("="*60)
        print(f"Passed: {self.all_passed}")
        print(f"Failed: {self.all_failed}")
        print(f"Total: {self.all_passed + self.all_failed}")
        
        if self.all_failed > 0:
            print("❌ 有失败测试！")
            for res in self.test_results:
                if not res["passed"]:
                    print(f"Fail: {res['name']}: {res['message']}")
        else:
            print("✅ 所有极端场景测试通过！")
        
        return self.all_failed == 0


if __name__ == "__main__":
    tester = ExtremeTester()
    success = tester.run_all()
    sys.exit(0 if success else 1)
