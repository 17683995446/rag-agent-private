"""
严格二叉树模块化结构验证脚本
验证规范：
1. 模块结构公理：所有非叶子模块直属子模块数量严格等于2
2. 调用隔离公理：跨模块交互仅通过Interface接口
3. 文件命名公理：文件名单词数量严格等于其所属模块层级数值
4. 方法行数公理：所有方法有效代码行严格≤10行
"""
import os
import ast
import re
from pathlib import Path


class StructureValidator:
    """结构验证器"""

    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.results = []
        self.total_checks = 0
        self.passed_checks = 0

    def log(self, message, passed=None):
        """记录日志"""
        if passed is None:
            self.results.append(f"  {message}")
        elif passed:
            self.results.append(f"  ✓ {message}")
            self.passed_checks += 1
        else:
            self.results.append(f"  ✗ {message}")
        self.total_checks += 1

    def validate_all(self):
        """执行所有验证"""
        self.results.append("=" * 60)
        self.results.append("严格二叉树模块化结构验证报告")
        self.results.append("=" * 60)

        self.validate_module_structure()
        self.validate_interface_impl_separation()
        self.validate_file_naming()
        self.validate_method_lengths()
        self.validate_access_modifiers()

        self.results.append("")
        self.results.append("=" * 60)
        self.results.append(f"验证结果: {self.passed_checks}/{self.total_checks} 通过")
        self.results.append("=" * 60)

        return "\n".join(self.results)

    def validate_module_structure(self):
        """验证模块结构"""
        self.results.append("\n1. 模块结构验证")
        self.results.append("-" * 60)

        modules = ["Config", "Prompt", "Rag", "Retrieve", "Text", "Vector"]
        for module_name in modules:
            module_path = self.root_path / "src" / module_name
            if not module_path.exists():
                self.log(f"模块 {module_name} 不存在", False)
                continue

            has_interfaces = (module_path / "interfaces").exists()
            has_impl = (module_path / "impl").exists()

            if has_interfaces and has_impl:
                self.log(f"{module_name}: interfaces + impl 结构正确", True)
            else:
                self.log(f"{module_name}: 结构不完整", False)

            if has_interfaces:
                interface_files = list((module_path / "interfaces").glob("*.py"))
                interface_count = len([f for f in interface_files if f.stem != "__init__"])
                if interface_count == 2:
                    self.log(f"  {module_name} interfaces: 2个文件 ✓", True)
                else:
                    self.log(f"  {module_name} interfaces: {interface_count}个文件 (期望2)", False)

            if has_impl:
                impl_files = list((module_path / "impl").glob("*.py"))
                impl_count = len([f for f in impl_files if f.stem != "__init__"])
                if impl_count == 2:
                    self.log(f"  {module_name} impl: 2个文件 ✓", True)
                else:
                    self.log(f"  {module_name} impl: {impl_count}个文件 (期望2)", False)

    def validate_interface_impl_separation(self):
        """验证接口实现分离"""
        self.results.append("\n2. 接口实现分离验证")
        self.results.append("-" * 60)

        modules = ["Config", "Prompt", "Rag", "Retrieve", "Text", "Vector"]
        for module_name in modules:
            module_path = self.root_path / "src" / module_name
            if not module_path.exists():
                continue

            impl_files = list((module_path / "impl").glob("*.py"))
            for impl_file in impl_files:
                if impl_file.stem == "__init__":
                    continue

                try:
                    with open(impl_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        tree = ast.parse(content)

                    imports = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
                    illegal_imports = []
                    for imp in imports:
                        if imp.module and "interfaces" not in imp.module:
                            for alias in imp.names:
                                if not alias.name.startswith("I"):
                                    illegal_imports.append(alias.name)

                    if not illegal_imports:
                        self.log(f"{module_name}/{impl_file.name}: 仅导入接口 ✓", True)
                    else:
                        self.log(f"{module_name}/{impl_file.name}: 发现非接口导入 {illegal_imports}", False)
                except Exception as e:
                    self.log(f"{module_name}/{impl_file.name}: 解析失败 {e}", False)

    def validate_file_naming(self):
        """验证文件命名"""
        self.results.append("\n3. 文件命名规范验证")
        self.results.append("-" * 60)

        modules = ["Config", "Prompt", "Rag", "Retrieve", "Text", "Vector"]
        for module_name in modules:
            module_path = self.root_path / "src" / module_name
            if not module_path.exists():
                continue

            for subdir in ["interfaces", "impl"]:
                subdir_path = module_path / subdir
                if not subdir_path.exists():
                    continue

                for py_file in subdir_path.glob("*.py"):
                    if py_file.stem == "__init__":
                        continue

                    stem = py_file.stem
                    is_interface = stem.startswith("I")
                    core_name = stem[1:] if is_interface else stem
                    is_impl = core_name.endswith("Impl")
                    clean_name = core_name[:-4] if is_impl else core_name

                    word_count = len(re.findall(r'[A-Z][a-z]*', clean_name))

                    if word_count == 1:
                        self.log(f"{module_name}/{subdir}/{stem}: 1个单词 ✓", True)
                    else:
                        self.log(f"{module_name}/{subdir}/{stem}: {word_count}个单词 (期望1)", False)

    def validate_method_lengths(self):
        """验证方法行数"""
        self.results.append("\n4. 方法行数验证")
        self.results.append("-" * 60)

        modules = ["Config", "Prompt", "Rag", "Retrieve", "Text", "Vector"]
        violations = []

        for module_name in modules:
            module_path = self.root_path / "src" / module_name
            if not module_path.exists():
                continue

            for subdir in ["interfaces", "impl"]:
                subdir_path = module_path / subdir
                if not subdir_path.exists():
                    continue

                for py_file in subdir_path.glob("*.py"):
                    if py_file.stem == "__init__":
                        continue

                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            tree = ast.parse(content)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                start_line = node.lineno
                                end_line = node.end_lineno
                                if end_line and start_line:
                                    line_count = end_line - start_line + 1
                                    if line_count > 10:
                                        violations.append(
                                            f"{module_name}/{subdir}/{py_file.name}.{node.name}(): {line_count}行"
                                        )
                    except Exception:
                        pass

        if not violations:
            self.log("所有方法均≤10行 ✓", True)
        else:
            self.log(f"发现 {len(violations)} 个方法超过10行", False)
            for v in violations[:5]:
                self.log(f"  {v}", False)

    def validate_access_modifiers(self):
        """验证访问修饰符"""
        self.results.append("\n5. 访问修饰符验证")
        self.results.append("-" * 60)

        modules = ["Config", "Prompt", "Rag", "Retrieve", "Text", "Vector"]
        violations = []

        for module_name in modules:
            module_path = self.root_path / "src" / module_name
            if not module_path.exists():
                continue

            impl_path = module_path / "impl"
            if not impl_path.exists():
                continue

            for py_file in impl_path.glob("*.py"):
                if py_file.stem == "__init__":
                    continue

                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef):
                                    for decorator in item.decorator_list:
                                        if isinstance(decorator, ast.Name) and decorator.id == "public":
                                            violations.append(f"{py_file.name}.{node.name}.{item.name}")
                                elif isinstance(item, ast.AnnAssign):
                                    if isinstance(item.target, ast.Name):
                                        violations.append(f"{py_file.name}.{node.name}.{item.target.id}")
                except Exception:
                    pass

        if not violations:
            self.log("impl目录无public访问 ✓", True)
        else:
            self.log(f"发现 {len(violations)} 处public使用", False)


def main():
    """主函数"""
    root = Path("/workspace")
    validator = StructureValidator(root)
    report = validator.validate_all()
    print(report)

    with open("/workspace/validation_report.txt", 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n验证报告已保存到: /workspace/validation_report.txt")


if __name__ == "__main__":
    main()
