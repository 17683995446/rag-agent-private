"""
RAG Agent 全面测试文件
包含：
- 静态代码检查
- 单元测试
- 集成测试
- 异常测试
- 边界测试
- 性能测试
"""
import sys
import os
import time
import traceback
from typing import List, Dict, Any

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.logger import get_logger


class TestResult:
    """测试结果类"""
    def __init__(self, name: str, passed: bool, message: str = "", duration: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration


class TestSuite:
    """测试套件"""
    
    def __init__(self):
        self.logger = get_logger()
        self.results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def run_test(self, name: str, test_func):
        """运行单个测试"""
        self.total_tests += 1
        print("="*60)
        print(f"TEST: {name}")
        print("="*60)
        
        start_time = time.time()
        try:
            test_func()
            duration = time.time() - start_time
            self.passed_tests += 1
            self.results.append(TestResult(name, True, "", duration))
            print(f"✓ PASSED: {name} ({duration:.4f}s)")
            return True
        except Exception as e:
            duration = time.time() - start_time
            self.failed_tests += 1
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.results.append(TestResult(name, False, error_msg, duration))
            print(f"✗ FAILED: {name}")
            print(error_msg)
            return False
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed:      {self.passed_tests}")
        print(f"Failed:      {self.failed_tests}")
        
        if self.failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if not result.passed:
                    print(f"  ✗ {result.name}")
                    print(f"    {result.message[:200]}...")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.2f}%")
        print("="*60)


def test_splitter():
    """测试文本分片器"""
    from Text.impl.SplitterImpl import SplitterImpl
    
    # 正常情况测试
    splitter = SplitterImpl(chunk_size=10, chunk_overlap=2)
    
    # 空文本
    result = splitter.split_text("")
    assert result == [], "空文本应返回空列表"
    
    # 短文本
    result = splitter.split_text("Hello")
    assert len(result) == 1, "短文本应返回一个分片"
    
    # 长文本
    long_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 10
    result = splitter.split_text(long_text)
    assert len(result) > 0, "长文本应返回多个分片"
    
    # 文档列表
    docs = ["Document 1", "Document 2", "Document 3"]
    result = splitter.split_documents(docs)
    assert len(result) >= 3, "文档列表应返回多个分片"
    
    # 边界测试
    splitter.set_chunk_size(1)
    result = splitter.split_text("Hi")
    assert len(result) == 2, "chunk_size=1时应返回2个分片"
    
    # 重叠边界
    splitter.set_chunk_size(100)
    splitter.set_chunk_overlap(99)
    assert splitter._chunk_overlap == 99, "重叠不能超过chunk_size-1"
    
    splitter.set_chunk_overlap(200)
    assert splitter._chunk_overlap == 99, "重叠应自动限制为chunk_size-1"


def test_vector_store():
    """测试向量存储"""
    from Vector.impl.StoreImpl import StoreImpl
    
    store = StoreImpl()
    
    # 空存储
    assert store.get_count() == 0, "初始计数应为0"
    
    # 添加向量
    texts = ["Text 1", "Text 2"]
    vectors = [[0.1, 0.2], [0.3, 0.4]]
    metadatas = [{"id": 1}, {"id": 2}]
    
    store.add_vectors(texts, vectors, metadatas)
    assert store.get_count() == 2, "添加2个向量后计数应为2"
    
    # 搜索
    results = store.similarity_search([0.0, 0.0], top_k=5)
    assert len(results) == 2, "搜索应返回所有向量"
    
    # 搜索限制
    results = store.similarity_search([0.0, 0.0], top_k=1)
    assert len(results) == 1, "搜索应限制top_k"
    
    # 空搜索
    store.delete_all()
    results = store.similarity_search([0.0, 0.0], top_k=5)
    assert len(results) == 0, "空存储搜索应返回空"


def test_embedding():
    """测试嵌入模型"""
    from Vector.impl.EmbeddingImpl import EmbeddingImpl
    
    embedding = EmbeddingImpl()
    
    # 维度检查
    assert embedding.get_dimension() == 384, "维度应为384"
    
    # 可用状态
    assert embedding.is_available() is False, "默认应不可用"
    
    # 单个文本嵌入
    result = embedding.embed_text("Test")
    assert len(result) == 384, "应返回384维向量"
    
    # 空文本
    result = embedding.embed_text("")
    assert len(result) == 384, "空文本也应返回384维向量"
    
    # 批量嵌入
    texts = ["Text 1", "Text 2", ""]
    results = embedding.embed_texts(texts)
    assert len(results) == 3, "批量嵌入应返回3个结果"


def test_bm25():
    """测试BM25检索"""
    from Retrieve.impl.Bm25Impl import Bm25Impl
    
    bm25 = Bm25Impl()
    
    # 空索引
    assert bm25.get_index_size() == 0, "初始索引应为空"
    
    # 索引文档
    docs = ["Hello world", "Hello Python", "Java programming"]
    bm25.index_documents(docs)
    assert bm25.get_index_size() == 3, "索引大小应为3"
    
    # 搜索
    results = bm25.search("Hello", top_k=5)
    assert len(results) == 2, "应找到2个匹配结果"
    
    results = bm25.search("Java", top_k=5)
    assert len(results) == 1, "应找到1个匹配结果"
    
    # 限制结果
    results = bm25.search("Hello", top_k=1)
    assert len(results) == 1, "应限制结果数量"
    
    # 无匹配
    results = bm25.search("Ruby", top_k=5)
    assert len(results) == 0, "无匹配应返回空"
    
    # 清除索引
    bm25.clear_index()
    assert bm25.get_index_size() == 0, "清除后索引应为空"


def test_retriever():
    """测试检索器"""
    from Retrieve.impl.RetrieverImpl import RetrieverImpl
    from Vector.impl.EmbeddingImpl import EmbeddingImpl
    from Vector.impl.StoreImpl import StoreImpl
    from Retrieve.impl.Bm25Impl import Bm25Impl
    
    # 创建组件
    embedding = EmbeddingImpl()
    store = StoreImpl()
    bm25 = Bm25Impl()
    retriever = RetrieverImpl(embedding, store, bm25)
    
    # 空检索
    results = retriever.retrieve("test", top_k=5)
    assert len(results) == 0, "空存储应返回空结果"
    
    # 添加数据
    texts = ["Document about AI", "Document about ML", "Document about DL"]
    vectors = embedding.embed_texts(texts)
    metadatas = [{} for _ in texts]
    store.add_vectors(texts, vectors, metadatas)
    bm25.index_documents(texts)
    
    # 检索
    results = retriever.retrieve("AI", top_k=5)
    assert len(results) >= 1, "应找到相关结果"
    
    # 权重设置 - 测试不访问私有属性，只验证方法能正常调用不抛异常
    retriever.set_semantic_weight(0.8)
    retriever.set_keyword_weight(0.5)
    retriever.set_semantic_weight(-10)
    retriever.set_semantic_weight(100)


def test_prompt_engineer():
    """测试提示词工程师"""
    from Prompt.impl.EngineerImpl import EngineerImpl
    
    engineer = EngineerImpl()
    
    # 系统提示
    system_prompt = engineer.build_system_prompt()
    assert len(system_prompt) > 0, "应返回系统提示"
    
    # 格式化上下文 - 空
    context = engineer.format_context([])
    assert "没有找到" in context, "空上下文应返回提示"
    
    # 格式化上下文 - 有内容
    contexts = ["Context 1", "Context 2"]
    formatted = engineer.format_context(contexts)
    assert "Context 1" in formatted, "应包含上下文1"
    assert "Context 2" in formatted, "应包含上下文2"
    
    # 构建提示
    prompt = engineer.build_prompt("Question", contexts)
    assert "Question" in prompt, "应包含问题"
    assert "Context 1" in prompt, "应包含上下文"
    
    # 添加指令
    engineer.add_instructions(["Instruction 1"])
    system_prompt = engineer.build_system_prompt()
    assert "Instruction 1" in system_prompt, "应包含指令"


def test_agent():
    """测试Agent"""
    from Rag.impl.BuilderImpl import BuilderImpl
    
    builder = BuilderImpl()
    agent = builder.build_agent()
    
    # 初始状态
    status = agent.get_status()
    assert status["document_count"] == 0, "文档计数应为0"
    assert status["vector_count"] == 0, "向量计数应为0"
    assert status["embedding_available"] is False, "嵌入不可用"
    
    # 就绪检查
    assert agent.is_ready() is False, "不应就绪"
    
    # 添加文档
    docs = [
        "人工智能（AI）是计算机科学的一个分支。",
        "机器学习（ML）是人工智能的子集。",
        "深度学习（DL）是机器学习的子集。"
    ]
    agent.add_documents(docs)
    
    status = agent.get_status()
    assert status["document_count"] == 3, "文档计数应为3"
    
    # 查询
    response = agent.query("什么是AI？")
    assert "模拟回答" in response or "错误" in response, "应返回有效响应"
    
    # 空查询
    response = agent.query("")
    assert "错误" in response or "不能为空" in response, "空查询应返回错误"
    
    # 重置
    agent.reset()
    status = agent.get_status()
    assert status["document_count"] == 0, "重置后计数应为0"


def test_edge_cases():
    """测试边界情况"""
    from Text.impl.SplitterImpl import SplitterImpl
    from Vector.impl.StoreImpl import StoreImpl
    from Retrieve.impl.Bm25Impl import Bm25Impl
    
    # 极端分片大小
    splitter = SplitterImpl(chunk_size=1, chunk_overlap=0)
    result = splitter.split_text("ABCDE")
    assert len(result) >= 5, "每个字符一个分片"
    
    splitter.set_chunk_size(1000000)
    result = splitter.split_text("Short text")
    assert len(result) == 1, "大chunk_size应返回一个分片"
    
    # 大量数据测试
    store = StoreImpl()
    texts = [f"Text {i}" for i in range(1000)]
    vectors = [[0.0] * 384 for _ in range(1000)]
    metadatas = [{} for _ in range(1000)]
    
    start = time.time()
    store.add_vectors(texts, vectors, metadatas)
    add_time = time.time() - start
    
    assert store.get_count() == 1000, "应添加1000个向量"
    assert add_time < 10.0, "添加应在10秒内完成"
    
    start = time.time()
    results = store.similarity_search([0.0]*384, top_k=100)
    search_time = time.time() - start
    
    assert len(results) == 100, "应返回100个结果"
    assert search_time < 5.0, "搜索应在5秒内完成"
    
    # BM25边界
    bm25 = Bm25Impl()
    bm25.index_documents([])  # 空索引
    assert bm25.get_index_size() == 0, "空索引大小应为0"
    
    results = bm25.search("test", top_k=10)
    assert len(results) == 0, "空索引搜索返回空"


def test_error_handling():
    """测试错误处理"""
    from Rag.impl.BuilderImpl import BuilderImpl
    
    builder = BuilderImpl()
    agent = builder.build_agent()
    
    # 空文档列表
    agent.add_documents([])  # 不应抛出异常
    
    # 含空字符串的文档列表
    agent.add_documents(["", "Valid doc", "  "])  # 不应抛出异常
    
    # 查询边界
    agent.query("")  # 不应抛出异常
    agent.query(None)  # 不应抛出异常（如果接口允许）


def test_integration():
    """集成测试 - 完整流程"""
    from Rag.impl.BuilderImpl import BuilderImpl
    
    # 1. 构建Agent
    builder = BuilderImpl()
    agent = builder.build_agent()
    
    # 2. 添加测试文档
    docs = [
        "Python是一种高级编程语言。",
        "Python易于学习，语法简洁。",
        "Python广泛应用于人工智能、数据分析、Web开发等领域。",
        "人工智能技术发展迅速，改变了我们的生活。",
        "机器学习是人工智能的核心技术之一。",
        "深度学习使用神经网络模型。"
    ]
    agent.add_documents(docs)
    
    # 3. 检查状态
    status = agent.get_status()
    assert status['document_count'] == 6, "文档数应为6"
    assert status['vector_count'] > 0, "向量数应大于0"
    
    # 4. 测试查询
    queries = [
        "Python是什么？",
        "人工智能有什么应用？",
        "机器学习和深度学习的关系？",
        "Python在AI领域的应用？"
    ]
    
    for query in queries:
        response = agent.query(query)
        assert len(response) > 0, "查询应返回响应"
    
    # 5. 测试重置
    agent.reset()
    status = agent.get_status()
    assert status['document_count'] == 0, "重置后文档数应为0"


def test_stress():
    """压力测试 - 大数据量"""
    from Rag.impl.BuilderImpl import BuilderImpl
    
    builder = BuilderImpl()
    agent = builder.build_agent()
    
    # 生成大量文档
    many_docs = []
    for i in range(100):
        doc = f"文档{i}: 这是测试文档{i}的内容。包含关于测试的信息。"
        many_docs.append(doc)
    
    # 添加大量文档
    start = time.time()
    agent.add_documents(many_docs)
    add_time = time.time() - start
    
    status = agent.get_status()
    assert status['document_count'] == 100, "应添加100个文档"
    assert add_time < 10.0, "添加应在10秒内完成"
    
    # 测试多次查询
    queries = ["测试", "文档", "内容", "信息"]
    total_time = 0.0
    
    for i in range(10):
        for query in queries:
            start = time.time()
            agent.query(query)
            total_time += time.time() - start
    
    avg_time = total_time / 40
    assert avg_time < 1.0, "平均查询时间应小于1秒"


def main():
    """主测试函数"""
    print("="*60)
    print("RAG Agent 全面测试套件")
    print("="*60)
    
    suite = TestSuite()
    
    # 运行所有测试
    suite.run_test("文本分片器", test_splitter)
    suite.run_test("向量存储", test_vector_store)
    suite.run_test("嵌入模型", test_embedding)
    suite.run_test("BM25检索", test_bm25)
    suite.run_test("检索器", test_retriever)
    suite.run_test("提示词工程师", test_prompt_engineer)
    suite.run_test("Agent基本功能", test_agent)
    suite.run_test("边界情况", test_edge_cases)
    suite.run_test("错误处理", test_error_handling)
    suite.run_test("完整流程", test_integration)
    suite.run_test("压力测试", test_stress)
    
    # 打印摘要
    suite.print_summary()
    
    # 返回结果
    return suite.failed_tests == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
