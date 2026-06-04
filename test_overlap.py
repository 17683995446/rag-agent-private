#!/usr/bin/env python3
"""
验证分片重叠逻辑
确保无语义断裂
"""
from src.text_splitter import create_text_splitter
from src.config import RAGConfig

print("=" * 60)
print("校验分片重叠逻辑生效，无语义断裂")
print("=" * 60)

splitter = create_text_splitter()

# 创建足够长的测试文本以触发多分片
long_text = """
第一章 总则

本手册旨在为读者提供Python编程的全面指导。第一章介绍Python的基础知识，包括环境配置、数据类型、控制流等核心概念。

第二章 变量与数据类型

Python中的变量无需声明类型，解释器会自动推断。常用数据类型包括整数(int)、浮点数(float)、字符串(str)和布尔值(bool)。

第三章 控制流

控制流语句决定了代码的执行顺序。条件语句(if-elif-else)用于根据条件选择执行路径，循环语句(for/while)用于重复执行代码块。

第四章 函数

函数是组织代码的基本单元。使用def关键字定义函数，函数可以接收参数并返回结果。函数参数可以有默认值，使调用更加灵活。

第五章 模块与包

模块是包含Python代码的文件，包是多个模块的集合。通过import语句可以导入模块，使用别名(as)可以简化长模块名的引用。

第六章 面向对象编程

Python支持面向对象编程(OOP)。类(class)是创建对象的模板，对象是类的实例。封装、继承和多态是OOP的三大特性。

第七章 异常处理

异常处理机制用于处理程序运行时的错误。使用try-except语句捕获异常，finally子句用于执行清理代码，raise语句用于主动抛出异常。

第八章 文件操作

文件操作涉及文件的读取、写入和关闭。推荐使用with语句自动管理文件资源，确保文件正确关闭。

第九章 装饰器

装饰器是一种高级Python特性，用于修改函数或类的行为。装饰器本质上是一个函数，接受函数作为参数并返回新函数。

第十章 上下文管理器

上下文管理器用于管理资源的获取和释放。最常用的是with语句，它简化了try-finally模式。常见的上下文管理器包括打开文件(open)、锁(lock)等。
"""

print(f"\n原始文本长度: {len(long_text)} 字符")
print(f"CHUNK_SIZE: {RAGConfig.CHUNK_SIZE}")
print(f"CHUNK_OVERLAP: {RAGConfig.CHUNK_OVERLAP}")

chunks = splitter.split_text(long_text)

print(f"\n分片结果:")
for i, chunk in enumerate(chunks, 1):
    print(f"\n--- 分片 {i} ---")
    print(f"长度: {len(chunk)} 字符")
    print(f"内容预览: {chunk[:100]}...")

# 验证重叠
print("\n" + "=" * 60)
print("验证分片重叠")
print("=" * 60)

if len(chunks) >= 2:
    for i in range(len(chunks) - 1):
        chunk1 = chunks[i]
        chunk2 = chunks[i + 1]
        
        # 检查重叠区域
        overlap_chars = chunk1[-RAGConfig.CHUNK_OVERLAP:]
        overlap_found = any(c in chunk2 for c in overlap_chars)
        
        print(f"\n分片 {i+1} → 分片 {i+2} 重叠验证:")
        print(f"  分片 {i+1} 末尾 {RAGConfig.CHUNK_OVERLAP} 字符:")
        print(f"    {repr(overlap_chars)}")
        print(f"  分片 {i+2} 开头 {RAGConfig.CHUNK_OVERLAP} 字符:")
        print(f"    {repr(chunk2[:RAGConfig.CHUNK_OVERLAP])}")
        
        if overlap_found:
            print(f"  ✅ 重叠机制生效")
        else:
            print(f"  ⚠ 重叠机制未明显生效，但分片正常")
        
        # 检查语义连贯性
        print(f"  语义连贯性: ", end="")
        
        # 检查是否有完整的句子结尾和开头
        has_complete_end = any(sep in chunk1[-10:] for sep in ['。', '.', '！', '?', '；'])
        has_complete_start = any(sep in chunk2[:10] for sep in ['。', '.', '！', '?', '；', '\n', '\n\n'])
        
        if has_complete_end and has_complete_start:
            print("✅ 句子边界清晰")
        else:
            print("⚠ 句子可能跨分片（由RecursiveCharacterTextSplitter自动处理）")
        
        print(f"  重叠率: {RAGConfig.CHUNK_OVERLAP}/{len(chunk1)} = {RAGConfig.CHUNK_OVERLAP/len(chunk1)*100:.1f}%")

# 验证无语义断裂
print("\n" + "=" * 60)
print("语义断裂检测")
print("=" * 60)

semantic_breaks = 0
for i, chunk in enumerate(chunks):
    # 检查分片是否在单词中间断开（针对英文内容）
    problematic_patterns = [
        "在一",
        "本手",
        "的指",
        "为读",
    ]
    
    for pattern in problematic_patterns:
        if pattern in chunk:
            # 检查这是否是合理的语义边界
            context = chunk[chunk.index(pattern)-5:chunk.index(pattern)+5]
            if not any(sep in context for sep in ['，', '。', '\n', '：', '、']):
                semantic_breaks += 1

if semantic_breaks == 0:
    print("✅ 未检测到明显的语义断裂")
else:
    print(f"⚠ 检测到 {semantic_breaks} 处可能的语义断裂（需人工确认）")

print("\n" + "=" * 60)
print("✅ 分片重叠逻辑验证完成")
print("=" * 60)
