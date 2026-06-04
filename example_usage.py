#!/usr/bin/env python3
"""
LocalLongTextRAG 使用示例
"""

from src.rag_agent import create_rag_agent
from data.test_long_text import test_contract_text, test_tech_text

def main():
    print("=" * 70)
    print("LocalLongTextRAG 使用示例")
    print("=" * 70)
    print()

    # 1. 创建Agent实例
    print("1. 创建Agent实例...")
    agent = create_rag_agent()
    print("   ✓ Agent创建成功！")
    print()

    # 2. 设置全局摘要
    print("2. 设置全局摘要...")
    agent.set_global_summary("这是一份商业合同和技术文档的测试用例，包含合同金额、签约方信息、技术参数等细节。")
    print("   ✓ 全局摘要已设置")
    print()

    # 3. 加载文档
    print("3. 加载测试文档...")
    test_text = test_contract_text + "\n" + test_tech_text
    agent.load_document(test_text)
    print("   ✓ 文档加载成功！")
    print()

    # 4. 测试查询1 - 查合同金额
    print("4. 测试查询1：查找合同金额")
    prompt1, docs1 = agent.query("合同金额是多少？")
    print("   - 查询成功！")
    print()
    print("=" * 70)
    print("生成的Prompt1：")
    print("=" * 70)
    print(prompt1)
    print()

    # 5. 测试查询2 - 查技术参数
    print("5. 测试查询2：查找技术文档中的参数")
    prompt2, docs2 = agent.query("技术文档中提到的系统配置是什么？")
    print("   - 查询成功！")
    print()
    print("=" * 70)
    print("生成的Prompt2：")
    print("=" * 70)
    print(prompt2)
    print()

    print("=" * 70)
    print("使用完成！你可以把生成的Prompt直接给任何LLM使用！")
    print("=" * 70)

if __name__ == "__main__":
    main()
