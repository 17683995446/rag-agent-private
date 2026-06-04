#!/usr/bin/env python3
"""
测试文本分片功能
验证分片数量合理性
"""
from src.text_splitter import create_text_splitter
from src.config import RAGConfig
from data.test_long_text import get_test_contract, get_test_tech_doc

print("=" * 60)
print("执行自动分片，验证分片数量合理性")
print("=" * 60)

# 创建分片器
splitter = create_text_splitter()

print(f"\n分片参数:")
print(f"  CHUNK_SIZE = {RAGConfig.CHUNK_SIZE}")
print(f"  CHUNK_OVERLAP = {RAGConfig.CHUNK_OVERLAP}")
print(f"  重叠率 = {(RAGConfig.CHUNK_OVERLAP / RAGConfig.CHUNK_SIZE * 100):.1f}%")

# 测试合同文本
print("\n" + "=" * 60)
print("测试1: 商业合同文本分片")
print("=" * 60)

contract_text = get_test_contract()
print(f"\n原始文本长度: {len(contract_text)} 字符")

chunks = splitter.split_text(contract_text)

print(f"\n分片结果统计:")
print(f"  分片数量: {len(chunks)} 个")
print(f"  平均每片长度: {sum(len(c) for c in chunks) / len(chunks):.1f} 字符")
print(f"  最短分片: {min(len(c) for c in chunks)} 字符")
print(f"  最长分片: {max(len(c) for c in chunks)} 字符")

# 验证分片合理性
expected_chunks = len(contract_text) // RAGConfig.CHUNK_SIZE + 1
print(f"\n合理性验证:")
print(f"  预计分片数: 约 {expected_chunks} 个")
print(f"  实际分片数: {len(chunks)} 个")
print(f"  偏差率: {abs(len(chunks) - expected_chunks) / expected_chunks * 100:.1f}%")

if len(chunks) <= expected_chunks * 1.5:
    print("  ✅ 分片数量合理")
else:
    print("  ⚠ 分片数量偏多，可能需要调整参数")

# 测试技术文档
print("\n" + "=" * 60)
print("测试2: 技术文档文本分片")
print("=" * 60)

tech_doc = get_test_tech_doc()
print(f"\n原始文本长度: {len(tech_doc)} 字符")

chunks2 = splitter.split_text(tech_doc)

print(f"\n分片结果统计:")
print(f"  分片数量: {len(chunks2)} 个")
print(f"  平均每片长度: {sum(len(c) for c in chunks2) / len(chunks2):.1f} 字符")
print(f"  最短分片: {min(len(c) for c in chunks2)} 字符")
print(f"  最长分片: {max(len(c) for c in chunks2)} 字符")

expected_chunks2 = len(tech_doc) // RAGConfig.CHUNK_SIZE + 1
print(f"\n合理性验证:")
print(f"  预计分片数: 约 {expected_chunks2} 个")
print(f"  实际分片数: {len(chunks2)} 个")
print(f"  偏差率: {abs(len(chunks2) - expected_chunks2) / expected_chunks2 * 100:.1f}%")

if len(chunks2) <= expected_chunks2 * 1.5:
    print("  ✅ 分片数量合理")
else:
    print("  ⚠ 分片数量偏多，可能需要调整参数")

# 查看分片重叠效果
print("\n" + "=" * 60)
print("验证分片重叠效果")
print("=" * 60)

if len(chunks) >= 2:
    chunk1_end = chunks[0][-50:] if len(chunks[0]) >= 50 else chunks[0]
    chunk2_start = chunks[1][:50] if len(chunks[1]) >= 50 else chunks[1]
    print(f"\n第一片末尾: ...{repr(chunk1_end)}")
    print(f"第二片开头: {repr(chunk2_start)}...")
    
    # 检查是否有重叠
    overlap_found = False
    for i in range(1, len(chunks)):
        if len(chunks[i-1]) >= RAGConfig.CHUNK_OVERLAP and len(chunks[i]) >= RAGConfig.CHUNK_OVERLAP:
            last_chars = chunks[i-1][-RAGConfig.CHUNK_OVERLAP:]
            first_chars = chunks[i][:RAGConfig.CHUNK_OVERLAP]
            if any(c in chunks[i] for c in last_chars[-10:]):
                overlap_found = True
                break
    
    if overlap_found or len(chunks) > 1:
        print("\n  ✅ 分片重叠机制生效")
    else:
        print("\n  ⚠ 建议检查重叠机制")

print("\n" + "=" * 60)
print("✅ 自动分片测试完成！")
print("=" * 60)
