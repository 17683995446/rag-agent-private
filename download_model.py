#!/usr/bin/env python3
"""
首次下载嵌入模型（需要联网）
"""
import os
import sys
from pathlib import Path

# 临时禁用离线模式以下载模型
os.environ.pop("HF_HUB_OFFLINE", None)
os.environ.pop("TRANSFORMERS_OFFLINE", None)

# 导入模块
from sentence_transformers import SentenceTransformer
from src.offline_config import get_cache_dir

print("=" * 60)
print("首次下载嵌入模型")
print("=" * 60)

cache_dir = Path(get_cache_dir())
model_name = "all-MiniLM-L6-v2"
model_path = cache_dir / model_name

print(f"\n模型名称: {model_name}")
print(f"目标路径: {model_path}")

if model_path.exists() and any(model_path.iterdir()):
    print("\n✅ 模型已存在，无需下载")
    print(f"   路径: {model_path}")
    sys.exit(0)

print("\n⚠ 即将下载模型（约90MB）")
print("⚠ 下载完成后，后续使用将完全离线")
response = input("\n确认下载？(y/n): ")

if response.lower() != 'y':
    print("取消下载")
    sys.exit(1)

print("\n正在下载模型...")
try:
    model = SentenceTransformer(
        model_name,
        cache_folder=str(cache_dir),
        device='cpu'
    )
    
    print("\n✅ 模型下载成功！")
    print(f"   保存路径: {cache_dir / model_name}")
    print(f"   向量维度: {model.get_sentence_embedding_dimension()}")
    
    print("\n⚠ 后续使用请确保 HF_HUB_OFFLINE=true")
    print("⚠ 首次加载后，模型将在本地缓存，后续无需联网")
    
except Exception as e:
    print(f"\n❌ 下载失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
