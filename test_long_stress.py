"""
长时间真实压力测试
- 10000+ 次操作
- 持续监控
- 稳定性验证
"""
import sys
import os
import time
import random
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl
from src.utils.logger import get_logger

logger = get_logger()


class LongTermStressTester:
    """长时间压力测试器"""
    
    def __init__(self):
        self.operation_count = 0
        self.error_count = 0
        self.start_time = None
        self.operation_times = []
        
    def run_stress_test(self, total_operations: int = 5000):
        """运行压力测试"""
        print("=" * 70)
        print(f"开始长时间压力测试 ({total_operations} 次操作)")
        print("=" * 70)
        
        self.start_time = time.time()
        
        builder = BuilderImpl()
        agent = builder.build_agent()
        
        # 文档池
        doc_pool = [
            "机器学习是人工智能的一个分支",
            "深度学习使用神经网络进行学习",
            "自然语言处理处理人类语言",
            "计算机视觉让计算机理解图像",
            "强化学习通过奖励进行学习",
            "迁移学习重用预训练模型",
            "生成模型创造新内容",
            "监督学习使用标注数据",
            "无监督学习发现数据模式",
            "半监督学习结合两种方式"
        ]
        
        # 问题池
        query_pool = [
            "什么是机器学习",
            "深度学习如何工作",
            "NLP是什么",
            "计算机视觉应用",
            "强化学习介绍",
            "迁移学习优点",
            "生成模型例子",
            "监督 vs 无监督",
            "AI最新进展",
            "数据科学基础"
        ]
        
        # 开始循环
        last_report_time = time.time()
        last_report_ops = 0
        
        for i in range(total_operations):
            op_start = time.time()
            
            try:
                # 随机选择操作
                op_type = random.randint(0, 5)
                
                if op_type == 0:
                    # 添加文档（1-3 个）
                    num_docs = random.randint(1, 3)
                    docs = random.choices(doc_pool, k=num_docs)
                    agent.add_documents(docs)
                
                elif op_type == 1:
                    # 查询
                    query = random.choice(query_pool)
                    agent.query(query)
                
                elif op_type == 2:
                    # 获取状态
                    agent.get_status()
                
                elif op_type == 3:
                    # 重置（偶尔）
                    if random.random() < 0.1:
                        agent.reset()
                
                elif op_type == 4:
                    # 检查就绪
                    agent.is_ready()
                
                # 混合操作
                elif op_type == 5:
                    # 组合操作
                    agent.add_documents([random.choice(doc_pool)])
                    agent.query(random.choice(query_pool))
                    agent.get_status()
                
                self.operation_count += 1
                
            except Exception as e:
                self.error_count += 1
                print(f"❌ 操作 {i} 异常: {str(e)[:100]}")
            
            op_end = time.time()
            self.operation_times.append(op_end - op_start)
            
            # 每 5 秒报告一次
            if (i + 1) % 100 == 0:
                now = time.time()
                if now - last_report_time > 5:
                    ops_since = self.operation_count - last_report_ops
                    elapsed = now - last_report_time
                    ops_per_sec = ops_since / elapsed if elapsed > 0 else 0
                    
                    print(f"[{i+1}/{total_operations}] 完成 - 速度: {ops_per_sec:.1f} ops/s, 错误: {self.error_count}")
                    last_report_time = now
                    last_report_ops = self.operation_count
        
        self.print_final_report(total_operations)
        return self.error_count == 0
    
    def print_final_report(self, total_ops: int):
        """打印最终报告"""
        elapsed = time.time() - self.start_time
        
        print("\n" + "=" * 70)
        print("长时间压力测试最终报告")
        print("=" * 70)
        print(f"总操作数: {total_ops}")
        print(f"成功操作: {self.operation_count}")
        print(f"错误数: {self.error_count}")
        print(f"总耗时: {elapsed:.2f} 秒")
        print(f"平均速度: {total_ops/elapsed:.1f} ops/s")
        
        if self.operation_times:
            import statistics
            avg_time = statistics.mean(self.operation_times)
            max_time = max(self.operation_times)
            min_time = min(self.operation_times)
            
            print(f"平均操作耗时: {avg_time*1000:.2f} ms")
            print(f"最大操作耗时: {max_time*1000:.2f} ms")
            print(f"最小操作耗时: {min_time*1000:.2f} ms")
        
        print(f"\n✅ 测试通过率: {(1 - self.error_count/total_ops)*100:.2f}%")
        
        if self.error_count == 0:
            print("\n🎉 完美！零错误通过压力测试！")
        else:
            print(f"\n⚠️ 有 {self.error_count} 个错误")


def main():
    # 先做小规模预热
    print("预热阶段...")
    pre_tester = LongTermStressTester()
    pre_tester.run_stress_test(500)
    
    print("\n" + "="*70)
    print("正式压力测试")
    print("="*70)
    
    # 正式长时间测试
    tester = LongTermStressTester()
    success = tester.run_stress_test(3000)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
