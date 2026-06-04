"""
超极端深度测试 - 超大规模、超长时间、错误注入
"""
import sys
import os
import random
import gc
import time
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl
from Vector.impl.EmbeddingImpl import EmbeddingImpl
from Vector.impl.StoreImpl import StoreImpl
from Retrieve.impl.Bm25Impl import Bm25Impl
from src.utils.logger import get_logger

logger = get_logger()


class UltraExtremeTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failure_details = []
        self.test_start_time = None
        
    def log(self, msg, is_error=False):
        prefix = "❌" if is_error else "✅"
        print(f"{prefix} {msg}")
        
    def assert_ok(self, condition, test_name, msg=""):
        if condition:
            self.passed += 1
            self.log(f"{test_name}: PASS")
        else:
            self.failed += 1
            self.failure_details.append(f"{test_name}: {msg}")
            self.log(f"{test_name}: FAIL - {msg}", is_error=True)
    
    def test_1_ultra_large_scale(self):
        """超大规模数据测试: 10,000+ 文档片段"""
        print("\n" + "="*70)
        print("测试 1: 超大规模数据测试")
        print("="*70)
        
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 生成大规模文档
            num_batches = 50
            docs_per_batch = 200
            total_docs = num_batches * docs_per_batch
            
            print(f"准备添加 {total_docs} 个文档片段...")
            
            start_time = time.time()
            
            for batch in range(num_batches):
                docs = []
                for i in range(docs_per_batch):
                    content = f"超大规模测试文档 batch{batch}_doc{i} " * 10
                    content += f"关键词{random.randint(1, 100)} 关键词{random.randint(1, 100)}"
                    docs.append(content)
                
                agent.add_documents(docs)
                
                if (batch + 1) % 10 == 0:
                    print(f"  已完成 {batch + 1}/{num_batches} 批次...")
            
            add_time = time.time() - start_time
            print(f"文档添加完成，耗时: {add_time:.2f} 秒")
            
            # 验证状态
            status = agent.get_status()
            print(f"状态检查: {status}")
            
            # 执行大量查询
            print("\n开始大规模查询测试 (500次)...")
            query_start = time.time()
            
            for i in range(500):
                query = f"关键词{random.randint(1, 100)}"
                result = agent.query(query)
                assert len(result) > 0, "查询不应返回空"
            
            query_time = time.time() - query_start
            print(f"查询测试完成，耗时: {query_time:.2f} 秒")
            
            # 重置测试
            print("\n重置系统...")
            agent.reset()
            
            reset_status = agent.get_status()
            assert reset_status['document_count'] == 0, "重置后文档计数应为0"
            assert reset_status['vector_count'] == 0, "重置后向量计数应为0"
            assert reset_status['bm25_index_size'] == 0, "重置后BM25索引应为0"
            
            self.assert_ok(True, "超大规模数据测试")
            
        except Exception as e:
            self.assert_ok(False, "超大规模数据测试", str(e))
    
    def test_2_memory_stress(self):
        """内存压力测试"""
        print("\n" + "="*70)
        print("测试 2: 内存压力测试")
        print("="*70)
        
        try:
            initial_count = len(gc.get_objects())
            print(f"初始对象数: {initial_count}")
            
            # 多次创建与销毁
            for round in range(10):
                builder = BuilderImpl()
                agent = builder.build_agent()
                
                # 添加一些数据
                docs = [f"内存测试文档 {i}" * 10 for i in range(100)]
                agent.add_documents(docs)
                
                # 查询几次
                for _ in range(50):
                    agent.query(f"测试查询 {_}")
                
                # 重置
                agent.reset()
                
                # 强制GC
                gc.collect()
                
                # 内存检查
                current_count = len(gc.get_objects())
                print(f"  Round {round+1}: 对象数 {current_count}")
            
            final_count = len(gc.get_objects())
            growth = final_count - initial_count
            print(f"总对象数增长: {growth}")
            
            # 允许合理的内存增长
            self.assert_ok(growth < 500000, "内存压力测试", f"对象增长过多: {growth}")
            
        except Exception as e:
            self.assert_ok(False, "内存压力测试", str(e))
    
    def test_3_error_injection(self):
        """错误注入与容错测试"""
        print("\n" + "="*70)
        print("测试 3: 错误注入与容错测试")
        print("="*70)
        
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 各种错误输入
            error_cases = [
                ("空查询", lambda: agent.query("")),
                ("空格查询", lambda: agent.query("   ")),
                ("None查询", lambda: agent.query(None)),  # type: ignore
                ("空列表添加", lambda: agent.add_documents([])),
                ("None列表", lambda: agent.add_documents(None)),  # type: ignore
                ("全空文档", lambda: agent.add_documents(["", "", ""])),
            ]
            
            for name, action in error_cases:
                try:
                    result = action()
                    self.log(f"  {name}: OK - 系统平稳处理")
                except Exception as e:
                    # 即使异常也要保证系统不崩溃
                    self.log(f"  {name}: Exception caught - {str(e)}")
            
            # 确保系统仍然可用
            agent.add_documents(["验证文档 测试内容"])
            result = agent.query("测试")
            self.assert_ok(len(result) > 0, "错误注入后系统仍然可用")
            
        except Exception as e:
            self.assert_ok(False, "错误注入测试", str(e))
    
    def test_4_rapid_state_changes(self):
        """快速状态变更测试"""
        print("\n" + "="*70)
        print("测试 4: 快速状态变更测试")
        print("="*70)
        
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            # 快速交替操作
            for cycle in range(100):
                # 添加
                agent.add_documents([f"快速变更文档 {cycle}"])
                # 查询
                agent.query(f"查询 {cycle}")
                # 获取状态
                agent.get_status()
                # 偶尔重置
                if cycle % 25 == 0:
                    agent.reset()
            
            self.assert_ok(True, "快速状态变更测试")
            
        except Exception as e:
            self.assert_ok(False, "快速状态变更测试", str(e))
    
    def test_5_bm25_efficiency(self):
        """BM25 效率与正确性测试"""
        print("\n" + "="*70)
        print("测试 5: BM25 效率与正确性测试")
        print("="*70)
        
        try:
            bm25 = Bm25Impl()
            
            # 索引大量文档
            print("索引文档...")
            docs = []
            for i in range(1000):
                if i == 500:
                    docs.append("特殊文档 唯一关键词 XYZ123 测试内容")
                else:
                    docs.append(f"普通文档 {i} 测试内容 随机内容")
            
            bm25.index_documents(docs)
            print(f"索引完成: {len(docs)} 文档")
            
            # 测试特殊关键词搜索
            print("搜索测试...")
            results = bm25.search("XYZ123", top_k=5)
            print(f"找到 {len(results)} 个结果")
            
            self.assert_ok(len(results) >= 1, "BM25 正确性测试", "应能找到特殊文档")
            
            # 性能测试
            start = time.time()
            for _ in range(1000):
                bm25.search(f"测试 {_}", top_k=3)
            search_time = time.time() - start
            print(f"1000次搜索耗时: {search_time:.3f}秒")
            
            self.assert_ok(search_time < 5.0, "BM25 效率测试", "搜索速度过慢")
            
        except Exception as e:
            self.assert_ok(False, "BM25 测试", str(e))
    
    def test_6_ultra_long_stress(self):
        """超长压力测试: 30分钟模拟（加速版）"""
        print("\n" + "="*70)
        print("测试 6: 超长压力测试 (加速版)")
        print("="*70)
        
        try:
            builder = BuilderImpl()
            agent = builder.build_agent()
            
            operations = 10000
            print(f"执行 {operations} 次操作...")
            
            start_time = time.time()
            errors = 0
            
            for i in range(operations):
                try:
                    action = random.randint(0, 4)
                    
                    if action == 0:
                        agent.add_documents([f"压力测试文档 {random.randint(1, 1000)}"])
                    elif action == 1:
                        agent.query(f"查询 {random.randint(1, 1000)}")
                    elif action == 2:
                        agent.get_status()
                    elif action == 3:
                        if random.random() < 0.02:  # 2% 概率重置
                            agent.reset()
                    else:
                        agent.is_ready()
                        
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # 只打印前5个
                        print(f"  操作 {i} 异常: {str(e)[:100]}")
                
                if (i + 1) % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(f"  已完成 {i+1}/{operations} 次操作, 耗时 {elapsed:.1f}s, 错误 {errors}")
            
            total_time = time.time() - start_time
            print(f"\n总计: {operations} 次操作, {errors} 错误, 耗时 {total_time:.1f} 秒")
            
            error_rate = errors / operations
            self.assert_ok(error_rate < 0.01, "超长压力测试", f"错误率过高: {error_rate:.2%}")
            
        except Exception as e:
            self.assert_ok(False, "超长压力测试", str(e))
    
    def run_all(self):
        self.test_start_time = time.time()
        
        self.test_1_ultra_large_scale()
        self.test_2_memory_stress()
        self.test_3_error_injection()
        self.test_4_rapid_state_changes()
        self.test_5_bm25_efficiency()
        self.test_6_ultra_long_stress()
        
        total_time = time.time() - self.test_start_time
        
        print("\n" + "="*70)
        print("超极端深度测试总结")
        print("="*70)
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"总计: {self.passed + self.failed}")
        print(f"总耗时: {total_time:.2f} 秒")
        
        if self.failure_details:
            print("\n失败详情:")
            for detail in self.failure_details:
                print(f"  - {detail}")
        
        return self.failed == 0


if __name__ == "__main__":
    print("="*70)
    print("超极端深度测试开始")
    print("="*70)
    
    tester = UltraExtremeTester()
    success = tester.run_all()
    sys.exit(0 if success else 1)
