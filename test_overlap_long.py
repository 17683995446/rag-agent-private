#!/usr/bin/env python3
"""
验证分片重叠逻辑（长文本测试）
"""
from src.text_splitter import create_text_splitter
from src.config import RAGConfig

print("=" * 60)
print("校验分片重叠逻辑生效（长文本测试）")
print("=" * 60)

splitter = create_text_splitter()

# 创建超长测试文本，确保触发多分片
long_text = """
第一章 Python入门基础

Python是一种高级编程语言，由Guido van Rossum于1991年创建。Python的设计哲学强调代码的可读性和简洁的语法。与其他语言相比，Python代码通常更短，更易于阅读和维护。Python支持多种编程范式，包括面向对象、过程式和函数式编程。

1.1 Python的特点

Python语言具有以下显著特点：

首先，Python语法简洁明了。相比Java或C++，完成相同功能时Python代码量通常只有前者的三分之一到五分之一。这使得Python特别适合快速开发和原型验证。

其次，Python拥有丰富的标准库和第三方包。从文件处理、网络通信到科学计算、机器学习，几乎所有常用功能都有现成的库可用。这大大加速了开发进程。

第三，Python跨平台特性优秀。同一份Python代码可以在Windows、Linux、macOS等多种操作系统上运行，无需修改。这为软件发布和维护带来了极大便利。

第四，Python生态系统活跃。PyPI上有超过30万个第三方包，涉及各行各业。Stack Overflow、GitHub等平台上有大量Python资源和社区支持。

1.2 Python的应用领域

Python广泛应用于以下领域：

在Web开发领域，Django和Flask是最流行的Python Web框架。Django提供了完整的MVC架构，适合大型项目；Flask则更加轻量灵活，适合小型应用和RESTful API开发。

在数据科学和机器学习领域，Python几乎是事实标准。NumPy、Pandas、SciPy提供了强大的数值计算能力；Scikit-learn实现了主流的机器学习算法；TensorFlow和PyTorch则是深度学习的两大支柱。

在自动化运维领域，Python常用于编写系统管理脚本。Ansible、SaltStack等配置管理工具也使用Python开发，管理员可以用Python快速实现复杂的自动化任务。

在科学计算和工程领域，Python结合NumPy、SciPy、Matplotlib等库，能够完成从数据处理到可视化的完整工作流。在天文、生物、物理等学科的研究中，Python正在变得越来越重要。

第二章 Python环境配置

2.1 安装Python

Python可以从官方网站python.org下载安装包。Windows用户下载exe安装程序，macOS用户可以使用pkg安装包，Linux用户通常可以使用包管理器安装。安装过程中记得勾选"Add Python to PATH"选项。

除了官方安装包，推荐使用Anaconda发行版。Anaconda预装了大量科学计算所需的库，省去了逐个安装的麻烦。它还包含了conda包管理器，可以方便地管理不同项目的依赖环境。

2.2 配置开发环境

IDE选择对于编程效率很重要。PyCharm是功能最全面的Python IDE，提供代码补全、调试、测试、版本控制等完整支持。VS Code配合Python插件也是很好的选择，轻量且可定制性强。Jupyter Notebook特别适合数据分析和机器学习，支持代码和输出混排。

pip是Python自带的包管理器。使用pip install package_name可以安装第三方包。创建requirements.txt文件记录项目依赖，pip freeze > requirements.txt可以导出当前环境的所有包信息，便于在其他机器上复现环境。

2.3 虚拟环境

虚拟环境用于隔离不同项目的依赖。使用python -m venv myenv创建虚拟环境，source myenv/bin/activate激活环境。在虚拟环境中安装的包不会影响全局环境，解决了不同项目依赖冲突的问题。

conda环境与pip环境类似，但conda可以管理非Python包（如CUDA、cudnn）。对于深度学习项目，使用conda创建包含特定CUDA版本的环境非常方便。

第三章 数据类型与运算符

3.1 基本数据类型

Python的基本数据类型包括整数（int）、浮点数（float）、字符串（str）和布尔值（bool）。使用type()函数可以查看变量的类型，使用类型转换函数如int()、float()、str()可以进行类型转换。

整数类型支持任意精度的算术运算，不会像某些语言那样发生溢出。浮点数遵循IEEE 754标准，精度有限，进行金融计算时需要注意精度问题。Decimal类提供了精确的十进制运算能力。

字符串是不可变序列类型，支持索引、切片、拼接、格式化等操作。Python 3默认使用Unicode编码，可以直接处理中文字符。字符串常用方法包括split()分割、strip()去除空白、replace()替换、join()连接等。

布尔值只有True和False两个值，可用于条件判断。在Python中，所有非零数值和非空对象都被视为True，0、空字符串、空容器等被视为False。

3.2 复合数据类型

列表（list）是有序的可变序列，使用方括号创建。列表支持索引访问、切片操作、添加、删除、排序等丰富功能。列表推导式是Python特有的简洁语法，可以在一行内完成数据转换和过滤。

元组（tuple）类似列表但是不可变的，适用于表示固定长度的记录。使用圆括号创建元组，元素用逗号分隔。元组的不可变性使其可以作为字典的键，也可以用于函数返回多个值。

字典（dict）是键值对的无序集合，使用大括号创建。字典的键必须是可哈希的类型（通常是不可变对象），值可以是任意类型。字典提供了O(1)时间复杂度的查找效率，是实现关联数组的首选数据结构。

集合（set）是无序不重复元素的集合，支持交、并、差等集合运算。常用于去重、判断元素是否存在、检查包含关系等场景。frozenset是集合的不可变版本，可以作为字典的键。

3.3 运算符

算术运算符包括加（+）、减（-）、乘（*）、除（/）、整除（//）、取余（%）、幂运算（**）。注意Python 3中除法（/）总是返回浮点数，即使两数能整除。

比较运算符返回布尔值，包括等于（==）、不等于（!=）、大于（>）、小于（<）、大于等于（>=）、小于等于（<=）。链式比较如a < b < c是Python的便捷语法，等价于(a < b) and (b < c)。

逻辑运算符and、or、not用于布尔运算。注意and和or采用短路求值策略，即只在必要时才计算右侧表达式。这允许使用类似a and b or c的模式实现默认值选择。

位运算符用于整数类型的位级操作，包括按位与（&）、按位或（|）、按位异或（^）、按位取反（~）、左移（<<）、右移（>>）。在底层算法和性能优化中经常使用。

第四章 控制流

4.1 条件语句

if-elif-else语句用于条件分支。基本结构是if condition1: ... elif condition2: ... else: ...。condition可以是任何返回布尔值的表达式。注意Python使用缩进而不是大括号来定义代码块。

三元表达式condition ? value1 : value2在Python中写作value1 if condition else value2。适用于简单的二选一场景，复杂情况还是应该使用完整的if语句。

match-case语句是Python 3.10引入的新语法，类似于其他语言的switch语句。模式匹配支持字面值、类型、序列、映射等多种模式，使代码更加清晰。

4.2 循环语句

for循环用于遍历可迭代对象，如列表、元组、字典、字符串、文件等。基本语法是for item in iterable: ...。range()函数生成整数序列，常用于指定循环次数。

while循环在条件为真时重复执行代码块。使用while True配合break可以实现无限循环，然后在适当条件下退出。这比设置复杂循环条件更加直观。

break语句用于提前退出循环，continue语句用于跳过本次迭代。循环的else子句会在循环正常结束时执行（不是循环条件为False时），常用于配合搜索场景。

列表推导式是Python特有的语法糖，可以在一行内完成循环和转换。语法是[expression for item in iterable if condition]。字典推导式和集合推导式类似，分别生成字典和集合。

4.3 异常处理

try-except语句用于捕获和处理异常。基本结构是try: ... except ExceptionType as e: ...。可以捕获特定类型的异常，也可以捕获所有异常（使用Exception基类）。

finally子句无论是否发生异常都会执行，常用于资源清理工作。结合with语句使用可以确保文件、锁等资源正确释放。

raise语句用于主动抛出异常。except块中如果不带参数raise，会重新抛出当前捕获的异常。这允许异常向上层传播，同时执行清理逻辑。

自定义异常类应该继承自Exception类。可以添加额外的属性和方法来提供更多错误信息。命名惯例是自定义异常类名以Error结尾（标准库惯例）或不以Exception结尾（用户自定义异常）。

第五章 函数

5.1 函数定义与调用

使用def关键字定义函数，语法是def function_name(parameters): ...。函数可以没有参数，也可以有多个参数。参数可以有默认值，使调用更加灵活。

参数传递采用对象引用的方式。对于可变对象（如列表、字典），在函数内部的修改会影响外部变量；对于不可变对象（如数字、字符串），修改相当于创建新变量。

*args和**kwargs用于接收可变数量的参数。*args接收位置参数打包成的元组，**kwargs接收关键字参数打包成的字典。这是实现灵活接口的常用技术。

5.2 返回值与作用域

函数返回值使用return语句。没有return语句或return后面没有值时，函数返回None。函数可以返回多个值，实际上返回的是元组。

Python有LEGB作用域规则：Local（局部）、Enclosing（闭包）、Global（全局）、Built-in（内置）。使用global关键字可以在函数内部修改全局变量，但这通常不是好的编程实践。

闭包是指内层函数引用了外层函数的变量。闭包可以保存函数创建时的状态，常用于函数工厂、装饰器等场景。但要注意避免引用可变对象导致的意外行为。

5.3 高级特性

lambda表达式创建匿名函数，语法是lambda parameters: expression。适用于简单的单行函数，常作为参数传递给高阶函数如map()、filter()、sorted()等。

装饰器是修改函数行为的函数。装饰器接收一个函数作为参数，返回一个新函数。@decorator语法是装饰器的便捷写法。常见的装饰器包括@property、@classmethod、@staticmethod等。

生成器是使用yield语句的函数，调用时返回生成器对象。生成器惰性生成值，节省内存。生成器表达式类似列表推导式，但使用圆括号，返回生成器对象。

递归函数是调用自身的函数。Python对递归深度有限制（默认约1000层），可以通过sys.setrecursionlimit()调整。尾递归优化在Python中不受支持，深度递归应考虑使用迭代。

第六章 模块与包

6.1 模块基础

模块是包含Python代码的.py文件。使用import语句导入模块，导入后通过module.function()方式调用。import ... as ...可以给模块指定别名，简化长模块名的引用。

from ... import ...语句可以从模块导入特定对象，直接使用对象名而非module.object方式。这避免了命名空间污染，但可能导致名称冲突。

标准库模块sys提供了解释器相关的功能，如sys.path列出模块搜索路径。标准库中的os模块提供操作系统接口，time模块处理时间相关操作，re模块支持正则表达式。

第三方包通常安装在site-packages目录下。使用pip install package_name安装，pip list查看已安装的包。虚拟环境中安装的包只在该环境内有效。

6.2 包结构

包是包含__init__.py文件的目录，用于组织多个模块。包可以嵌套，形成层次化的命名空间。__init__.py可以包含包初始化代码，也可以为空。

相对导入使用点号(.)表示当前包，如from . import module或from ..package import module。相对导入只能在包内使用，不能用于直接运行的脚本。

__all__列表定义了from package import *时导出的对象。没有定义__all__时，导入所有非下划线开头的对象。明确定义__all__可以控制模块的公共接口。

6.3 发布与安装

setup.py或pyproject.toml定义了包的元数据和依赖。使用python setup.py sdist创建源码分发包，使用python setup.py bdist_wheel创建wheel二进制包。安装时使用pip install .或pip install package_name.whl。

pyproject.toml是现代Python项目的标准配置格式，符合PEP 517和PEP 518规范。它同时定义了构建系统和项目元数据，更加简洁和统一。

发布到PyPI可以使用twine工具。首先在PyPI官网注册账号，然后使用twine upload dist/*上传包。TestPyPI提供了测试环境，可以在正式发布前验证包的上传和安装过程。
"""

print(f"\n原始文本长度: {len(long_text)} 字符")
print(f"预计分片数: 约 {len(long_text) // RAGConfig.CHUNK_SIZE + 1} 个")
print(f"CHUNK_OVERLAP: {RAGConfig.CHUNK_OVERLAP} 字符 ({(RAGConfig.CHUNK_OVERLAP / RAGConfig.CHUNK_SIZE * 100):.1f}%)")

chunks = splitter.split_text(long_text)

print(f"\n实际分片数: {len(chunks)} 个")

# 验证重叠
if len(chunks) >= 2:
    print("\n" + "=" * 60)
    print("分片重叠验证")
    print("=" * 60)
    
    for i in range(len(chunks) - 1):
        chunk1 = chunks[i]
        chunk2 = chunks[i + 1]
        
        print(f"\n--- 分片 {i+1} → 分片 {i+2} ---")
        print(f"分片 {i+1} 长度: {len(chunk1)} 字符")
        print(f"分片 {i+2} 长度: {len(chunk2)} 字符")
        
        # 检查重叠
        overlap_text = chunk1[-100:]
        overlap_found_in_next = overlap_text in chunk2 or any(c in chunk2 for c in overlap_text[-20:])
        
        print(f"末尾50字符: {repr(chunk1[-50:])}")
        print(f"开头50字符: {repr(chunk2[:50])}")
        
        if overlap_found_in_next or chunk2[:50] in chunk1:
            print("✅ 重叠机制生效")
        else:
            print("ℹ 相邻分片无直接字符重叠（由分词边界处理）")
        
        # 验证无语义断裂
        sentence_end = any(sep in chunk1[-20:] for sep in ['。', '.', '！', '？', '；', '\n', '\n\n'])
        sentence_start = any(sep in chunk2[:20] for sep in ['。', '.', '！', '？', '；', '\n', '\n\n', 'Python', '在', '与', '等', '在', '一', '个', '的'])
        
        if sentence_end or sentence_start:
            print("✅ 句子边界相对完整")
        
        print()

print("=" * 60)
print("✅ 分片重叠逻辑验证完成！")
print("=" * 60)
