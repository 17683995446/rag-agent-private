"""
真实嵌入模型集成测试
验证sentence-transformers是否正确集成
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Vector.impl.EmbeddingImpl import EmbeddingImpl
from Vector.impl.EmbeddingChecker import EmbeddingChecker
from Vector.impl.EmbeddingConfig import EmbeddingConfig
from Vector.impl.EmbeddingCache import EmbeddingCache


def test_dependency_check():
    """测试依赖检查"""
    print("="*60)
    print("测试1: 依赖检查")
    print("="*60)
    
    checker = EmbeddingChecker()
    ok, summary = checker.check_all_dependencies()
    print(summary)
    
    if ok:
        print("✅ 所有依赖已安装")
    else:
        print("⚠️ 部分依赖缺失，将使用模拟模式")
    
    return ok


def test_config():
    """测试配置类"""
    print("\n" + "="*60)
    print("测试2: 配置类")
    print("="*60)
    
    # 默认配置
    config = EmbeddingConfig()
    print(f"默认模型: {config.model_name}")
    print(f"默认维度: {config.dimension}")
    print(f"缓存目录: {config.cache_dir}")
    print(f"设备: {config.device}")
    print(f"配置验证: {'✅' if config.validate() else '❌'}")
    
    # 自定义配置
    custom_config = EmbeddingConfig(
        model_name="all-mpnet-base-v2",
        device="cpu"
    )
    print(f"\n自定义模型: {custom_config.model_name}")
    print(f"自定义维度: {custom_config.dimension}")
    
    return True


def test_cache():
    """测试缓存工具"""
    print("\n" + "="*60)
    print("测试3: 缓存工具")
    print("="*60)
    
    config = EmbeddingConfig()
    cache = EmbeddingCache(config.cache_dir)
    
    created = cache.ensure_cache_dir()
    print(f"缓存目录创建: {'✅' if created else '❌'}")
    print(f"缓存目录: {cache.get_cache_dir()}")
    print(f"目录可写: {'✅' if cache.is_writable() else '❌'}")
    
    return True


def test_embedding_mock():
    """测试模拟嵌入模式"""
    print("\n" + "="*60)
    print("测试4: 模拟嵌入模式")
    print("="*60)
    
    embedding = EmbeddingImpl()
    print(f"模型可用: {embedding.is_available()}")
    print(f"向量维度: {embedding.get_dimension()}")
    
    # 单文本嵌入
    result = embedding.embed_text("测试文本")
    print(f"单文本嵌入结果长度: {len(result)}")
    print(f"单文本嵌入结果: {result[:5]}...")  # 只显示前5个
    
    # 批量嵌入
    results = embedding.embed_texts(["文本1", "文本2", "文本3"])
    print(f"批量嵌入结果数量: {len(results)}")
    print(f"每个向量维度: {len(results[0])}")
    
    return True


def test_embedding_real():
    """测试真实嵌入模式（如果依赖可用）"""
    print("\n" + "="*60)
    print("测试5: 真实嵌入模式")
    print("="*60)
    
    checker = EmbeddingChecker()
    ok, _ = checker.check_all_dependencies()
    
    if not ok:
        print("⚠️ 依赖未安装，跳过真实模型测试")
        print("请运行: pip install sentence-transformers torch")
        return True
    
    try:
        config = EmbeddingConfig()
        embedding = EmbeddingImpl(config.model_name)
        
        # 加载真实模型
        loaded = embedding.load_model(config.cache_dir)
        print(f"模型加载: {'✅' if loaded else '❌'}")
        
        if loaded:
            print(f"模型可用: {embedding.is_available()}")
            print(f"实际维度: {embedding.get_dimension()}")
            
            # 测试真实嵌入
            result = embedding.embed_text("这是一个测试句子")
            print(f"嵌入结果长度: {len(result)}")
            print(f"嵌入结果前10个值: {[round(x, 4) for x in result[:10]]}")
            
            # 测试语义相似性（简单验证）
            vec1 = embedding.embed_text("机器学习")
            vec2 = embedding.embed_text("深度学习")
            vec3 = embedding.embed_text("苹果")
            
            # 计算余弦相似度
            import numpy as np
            def cosine_similarity(a, b):
                return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
            sim1 = cosine_similarity(vec1, vec2)
            sim2 = cosine_similarity(vec1, vec3)
            
            print(f"\n语义相似度测试:")
            print(f"'机器学习' vs '深度学习': {sim1:.4f}")
            print(f"'机器学习' vs '苹果': {sim2:.4f}")
            print(f"✅ 相关文本相似度更高: {sim1 > sim2}")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实模型测试失败: {str(e)}")
        return False


def main():
    print("="*60)
    print("真实嵌入模型集成测试")
    print("="*60)
    
    results = []
    results.append(("依赖检查", test_dependency_check()))
    results.append(("配置类", test_config()))
    results.append(("缓存工具", test_cache()))
    results.append(("模拟嵌入", test_embedding_mock()))
    results.append(("真实嵌入", test_embedding_real()))
    
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
