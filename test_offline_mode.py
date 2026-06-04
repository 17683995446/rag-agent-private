#!/usr/bin/env python3
"""
测试离线运行模式
"""
import os
import sys

print("=" * 50)
print("测试全局离线运行模式")
print("=" * 50)

# 导入 src 模块会自动设置离线模式
import src

print()
print("验证环境变量设置：")
print(f"LANGCHAIN_TRACING_V2: {os.environ.get('LANGCHAIN_TRACING_V2', '未设置')}")
print(f"LANGCHAIN_TELEMETRY_ENABLED: {os.environ.get('LANGCHAIN_TELEMETRY_ENABLED', '未设置')}")
print(f"HF_HUB_OFFLINE: {os.environ.get('HF_HUB_OFFLINE', '未设置')}")
print(f"TRANSFORMERS_OFFLINE: {os.environ.get('TRANSFORMERS_OFFLINE', '未设置')}")

print()
print("✅ 离线运行模式配置完成")
print("=" * 50)
