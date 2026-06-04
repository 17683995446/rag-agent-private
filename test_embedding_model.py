#!/usr/bin/env python3
"""
测试嵌入模型（包含首次下载逻辑）
"""
import os
import sys
from pathlib import Path

# 导入模块
from sentence_transformers import SentenceTransformer
from src.offline_config import get_cache_dir
from src.config import RAGConfig

print("=" * 60)
print("测试嵌入模型")
print("=" * 60)

cache_dir = Path(get_cache_dir())
model_name = RAGConfig.EMBEDDING_MODEL_NAME
model_path = cache_dir / model_name

print(f"\n模型名称: {model_name}")
print(f"缓存目录: {cache_dir}")

# 检查模型是否已存在
if model_path.exists() and any(model_path.iterdir()):
    print(f"\n✅ 找到本地模型: {model_path}")
    use_offline = True
else:
    print(f"\n⚠ 本地模型不存在: {model_path}")
    print("\n首次使用需要下载模型（约90MB）")
    print("请运行以下命令下载模型：")
    print("  python download_model.py")
    print("\n或者手动下载：")
    print(f"  1. 确保网络连接")
    print(f"  2. 运行: python -c \"from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', cache_folder='{cache_dir}')\"")
    
    # 尝试临时允许联网
    print("\n正在尝试临时允许联网下载...")
    os.environ.pop("HF_HUB_OFFLINE", None)
    os.environ.pop("TRANSFORMERS_OFFLINE", None)
    use_offline = False

try:
    print("\n正在加载模型...")
    if use_offline:
        model = SentenceTransformer(
            str(model_path),
            device='cpu'
        )
    else:
        model = SentenceTransformer(
            model_name,
            cache_folder=str(cache_dir),
            device='cpu'
        )
        print(f"✅ 模型已保存到: {cache_dir / model_name}")
    
    print(f"\n✅ 嵌入模型加载成功")
    print(f"   向量维度: {model.get_sentence_embedding_dimension()}")
    
    # 测试编码
    print("\n" + "-" * 60)
    print("测试文本编码")
    print("-" * 60)
    
    test_texts = [
        "这是一个测试句子",
        "这是另一个测试句子，用于验证嵌入模型",
        "Python是一种高级编程语言"
    ]
    
    print(f"\n测试文本: {len(test_texts)} 个")
    
    embeddings = model.encode(
        test_texts,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    
    print(f"✅ 编码完成")
    print(f"   向量形状: {embeddings.shape}")
    print(f"   向量维度: {embeddings.shape[1]}")
    
    # 验证
    print("\n" + "-" * 60)
    print("验证结果")
    print("-" * 60)
    
    expected_dim = model.get_sentence_embedding_dimension()
    if embeddings.shape[1] == expected_dim:
        print(f"✅ 向量维度正确: {expected_dim}")
    else:
        print(f"❌ 向量维度错误: 期望 {expected_dim}, 实际 {embeddings.shape[1]}")
    
    if len(embeddings) == len(test_texts):
        print(f"✅ 编码数量正确: {len(test_texts)}")
    else:
        print(f"❌ 编码数量错误: 期望 {len(test_texts)}, 实际 {len(embeddings)}")
    
    print("\n" + "=" * 60)
    print("✅ 嵌入模型测试完成！")
    print("=" * 60)
    
    if not use_offline:
        print("\n⚠ 重要提示:")
        print("  模型已下载到本地，后续使用将完全离线运行")
        print("  请确保 HF_HUB_OFFLINE=true 已设置")
    
except Exception as e:
    print(f"\n❌ 嵌入模型测试失败: {e}")
    print("\n可能的原因:")
    print("  1. 首次使用未联网下载模型")
    print("  2. 模型文件损坏")
    print("\n解决方案:")
    print("  1. 连接网络后运行: python download_model.py")
    print("  2. 或手动下载模型到缓存目录")
    sys.exit(1)
