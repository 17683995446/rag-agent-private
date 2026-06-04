# RAG Agent 系统

## 版本: 2.0.0

## 功能特性

- ✅ 真实嵌入模型集成 (sentence-transformers)
- ✅ 向量数据库存储 (ChromaDB)
- ✅ LLM接口层 (支持扩展)
- ✅ 高级检索优化 (混合检索 + 重排序)
- ✅ 生产级配置管理 (YAML)
- ✅ 完整日志系统
- ✅ 模块化架构

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基础使用

```python
from Rag.impl.BuilderImpl import BuilderImpl

# 构建基础Agent
builder = BuilderImpl()
agent = builder.build_agent()

# 添加文档
agent.add_documents(["文档内容1", "文档内容2"])

# 查询
result = agent.query("你的问题")
print(result)
```

### 高级使用（推荐）

```python
from Rag.impl.BuilderImpl import BuilderImpl

# 构建高级Agent（带ChromaDB和重排序）
builder = BuilderImpl()
agent = builder.build_agent_advanced(
    model_name="all-MiniLM-L6-v2",
    use_reranker=True
)

# 添加文档
agent.add_documents(["文档内容1", "文档内容2"])

# 查询
result = agent.query("你的问题")
print(result)
```

## 配置

编辑 `config.yaml` 文件自定义配置：

```yaml
embedding:
  model_name: "all-MiniLM-L6-v2"
  device: "auto"

vector_store:
  type: "chroma"

retrieval:
  use_reranker: true
```

## 测试

```bash
python test_comprehensive.py
python test_chroma_store.py
python test_embedding_real.py
```

## 架构

严格遵循二叉树层级模块化工程规范：

```
src/
├── Config/      # 配置模块
├── Text/        # 文本处理模块
├── Vector/      # 向量模块
├── Retrieve/    # 检索模块
├── Prompt/      # 提示词模块
└── Rag/         # RAG核心模块
```

## License

MIT
