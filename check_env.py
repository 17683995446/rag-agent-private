#!/usr/bin/env python3
"""
环境自检脚本
验证全部依赖可正常导入
"""
import os
import sys
from pathlib import Path


def print_section(title):
    """打印分节标题"""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    """检查Python版本"""
    print_section("Python 版本检查")
    
    version = sys.version_info
    print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 9 <= version.minor <= 11:
        print("✓ Python 版本符合要求 (3.9-3.11)")
        return True
    else:
        print(f"✗ Python 版本不在推荐范围 (3.9-3.11)")
        return False


def check_dependencies():
    """检查所有依赖包"""
    print_section("依赖包检查")
    
    required_packages = {
        "langchain": "LangChain",
        "langchain_core": "LangChain Core",
        "langchain_chroma": "LangChain Chroma",
        "chromadb": "ChromaDB",
        "sentence_transformers": "Sentence-Transformers",
        "rank_bm25": "Rank-BM25",
        "numpy": "NumPy",
        "transformers": "Transformers",
        "torch": "PyTorch",
    }
    
    all_ok = True
    for module, name in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {name} ({module}) - 正常")
        except ImportError as e:
            print(f"✗ {name} ({module}) - 导入失败: {e}")
            all_ok = False
    
    return all_ok


def check_advanced_features():
    """检查高级功能模块"""
    print_section("高级功能模块检查")
    
    features = [
        ("langchain_text_splitters", "RecursiveCharacterTextSplitter", "LangChain 文本分割器"),
        ("langchain_chroma", "Chroma", "LangChain Chroma 集成"),
        ("sentence_transformers", "SentenceTransformer", "Sentence-Transformer 模型"),
        ("rank_bm25", "BM25Okapi", "BM25 检索器"),
    ]
    
    all_ok = True
    for module, attr, name in features:
        try:
            mod = __import__(module, fromlist=[attr])
            getattr(mod, attr)
            print(f"✓ {name} - 正常")
        except (ImportError, AttributeError) as e:
            print(f"✗ {name} - 失败: {e}")
            all_ok = False
    
    return all_ok


def check_directory_structure():
    """检查目录结构"""
    print_section("目录结构检查")
    
    project_root = Path(__file__).parent
    required_dirs = ["src", "chroma_db", "logs", "data"]
    
    all_ok = True
    for dirname in required_dirs:
        dirpath = project_root / dirname
        if dirpath.exists() and dirpath.is_dir():
            print(f"✓ {dirname}/ 目录存在")
        else:
            print(f"✗ {dirname}/ 目录不存在")
            all_ok = False
    
    return all_ok


def check_offline_mode():
    """检查离线模式配置"""
    print_section("离线模式检查")
    
    from src.offline_config import set_offline_mode, get_cache_dir
    
    # 检查关键环境变量
    offline_vars = [
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_TELEMETRY_ENABLED",
        "HF_HUB_OFFLINE",
        "TRANSFORMERS_OFFLINE",
    ]
    
    all_ok = True
    for var in offline_vars:
        value = os.environ.get(var)
        if value and value.lower() in ["true", "false"]:
            print(f"✓ {var} = {value}")
        else:
            print(f"✗ {var} 未设置或设置不正确")
            all_ok = False
    
    # 检查缓存目录
    cache_dir = get_cache_dir()
    print(f"✓ 缓存目录: {cache_dir}")
    
    return all_ok


def check_basic_functionality():
    """检查基本功能"""
    print_section("基本功能测试")
    
    # 测试 BM25 基本功能
    try:
        from rank_bm25 import BM25Okapi
        
        corpus = [
            "这是一个测试文档",
            "这是另一个文档",
            "这是第三个文档用于测试"
        ]
        tokenized_corpus = [doc.split() for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        
        query = "测试 文档"
        scores = bm25.get_scores(query.split())
        
        print(f"✓ BM25 功能测试通过 (得分: {scores})")
        bm25_ok = True
    except Exception as e:
        print(f"✗ BM25 功能测试失败: {e}")
        bm25_ok = False
    
    # 测试 NumPy 基本功能
    try:
        import numpy as np
        arr = np.array([1, 2, 3, 4, 5])
        mean_val = np.mean(arr)
        print(f"✓ NumPy 功能测试通过 (平均值: {mean_val})")
        numpy_ok = True
    except Exception as e:
        print(f"✗ NumPy 功能测试失败: {e}")
        numpy_ok = False
    
    return bm25_ok and numpy_ok


def check_configuration_files():
    """检查配置文件"""
    print_section("配置文件检查")
    
    project_root = Path(__file__).parent
    required_files = [
        "requirements.txt",
        ".gitignore",
        ".python-version",
    ]
    
    all_ok = True
    for filename in required_files:
        filepath = project_root / filename
        if filepath.exists():
            print(f"✓ {filename} 存在")
        else:
            print(f"✗ {filename} 不存在")
            all_ok = False
    
    return all_ok


def main():
    """主函数"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "环境自检脚本 v1.0" + " " * 25 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {
        "Python 版本": check_python_version(),
        "依赖包": check_dependencies(),
        "高级功能": check_advanced_features(),
        "目录结构": check_directory_structure(),
        "离线模式": check_offline_mode(),
        "基本功能": check_basic_functionality(),
        "配置文件": check_configuration_files(),
    }
    
    print_section("检查结果汇总")
    
    all_passed = True
    for name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name:15s}: {status}")
        if not passed:
            all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("🎉 所有检查项通过！环境配置正确。")
    else:
        print("⚠ 部分检查项失败，请检查上述输出。")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
