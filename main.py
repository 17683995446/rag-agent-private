"""
RAG Agent 入口文件
严格按照严格二叉树层级模块化工程刚性规范实现
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Rag.impl.BuilderImpl import BuilderImpl


def create_agent():
    """创建RAG Agent实例"""
    builder = BuilderImpl()
    builder.initialize_components()
    return builder.build_agent()


def main():
    """主函数演示"""
    print("=" * 60)
    print("RAG Agent - 严格二叉树模块化架构")
    print("=" * 60)
    print("\n正在初始化Agent...")
    agent = create_agent()
    print("Agent初始化完成\n")
    print(f"状态: {agent.get_status()}")
    print("\n" + "=" * 60)
    sample_docs = [
        "这是一段关于人工智能的文档。",
        "人工智能技术正在改变世界。",
        "机器学习和深度学习是AI的核心技术。"
    ]
    print("添加示例文档...")
    agent.add_documents(sample_docs)
    print("文档添加完成\n")
    print(f"更新状态: {agent.get_status()}")
    print("\n" + "=" * 60)
    print("\n测试查询:")
    query = "人工智能有哪些核心技术？"
    print(f"问题: {query}")
    answer = agent.query(query)
    print(f"回答:\n{answer}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
