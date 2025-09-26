#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codeforces数据挖掘项目Windows启动脚本
针对Windows环境优化的启动脚本
"""

import os
import sys
import subprocess
import argparse

def install_dependencies_windows():
    """Windows环境下安装依赖"""
    print("正在为Windows环境安装依赖...")
    
    # Windows下推荐的依赖安装顺序
    windows_packages = [
        "Flask>=2.0.0",
        "numpy>=1.21.0",  # 先安装numpy
        "pandas>=1.5.0",  # 使用较老但稳定的版本
        "matplotlib>=3.5.0", 
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0",
        "requests>=2.25.0",
        "joblib>=1.0.0"
    ]
    
    try:
        # 升级pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # 逐个安装包，避免依赖冲突
        for package in windows_packages:
            print(f"安装 {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"⚠ {package} 安装失败，尝试使用预编译版本...")
                # 尝试使用conda-forge或其他源
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--only-binary=all"])
                    print(f"✓ {package} (预编译版本) 安装成功")
                except subprocess.CalledProcessError:
                    print(f"✗ {package} 安装失败，请手动安装")
                    
        print("✓ 依赖安装完成")
        return True
        
    except Exception as e:
        print(f"✗ 依赖安装失败: {e}")
        print("\n建议解决方案:")
        print("1. 安装Microsoft Visual Studio Build Tools")
        print("2. 使用Anaconda环境")
        print("3. 使用预编译的Python包")
        return False

def check_data():
    """检查数据文件"""
    if not os.path.exists("codeforces_problems_with_solved.csv"):
        print("⚠ 数据文件不存在，正在获取数据...")
        try:
            subprocess.check_call([sys.executable, "api.py"])
            print("✓ 数据获取完成")
        except subprocess.CalledProcessError:
            print("✗ 数据获取失败")
            print("您可以稍后手动运行: python api.py")
            return False
    else:
        print("✓ 数据文件已存在")
    return True

def train_model():
    """训练机器学习模型"""
    print("开始训练机器学习模型...")
    try:
        subprocess.check_call([sys.executable, "run.py"])
        print("✓ 模型训练完成")
        return True
    except subprocess.CalledProcessError:
        print("✗ 模型训练失败")
        print("您可以稍后手动运行: python run.py")
        return False

def start_app(host="127.0.0.1", port=5000, debug=False):
    """启动Flask应用"""
    print(f"启动Web应用: http://{host}:{port}")
    os.environ["FLASK_HOST"] = host
    os.environ["FLASK_PORT"] = str(port)
    os.environ["FLASK_DEBUG"] = str(debug)
    
    try:
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n应用已停止")
    except subprocess.CalledProcessError as e:
        print(f"✗ 应用启动失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="Codeforces数据挖掘项目Windows启动脚本")
    parser.add_argument("--host", default="127.0.0.1", help="Flask应用主机地址")
    parser.add_argument("--port", type=int, default=5000, help="Flask应用端口")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--skip-deps", action="store_true", help="跳过依赖检查")
    parser.add_argument("--skip-data", action="store_true", help="跳过数据检查")
    parser.add_argument("--skip-model", action="store_true", help="跳过模型训练")
    parser.add_argument("--deps-only", action="store_true", help="仅安装依赖后退出")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Codeforces数据挖掘项目Windows启动器")
    print("=" * 60)
    
    # 仅安装依赖
    if args.deps_only:
        success = install_dependencies_windows()
        if success:
            print("\n依赖安装完成！现在可以运行:")
            print("python start_windows.py --skip-deps")
        sys.exit(0 if success else 1)
    
    # 检查依赖
    if not args.skip_deps:
        success = install_dependencies_windows()
        if not success:
            print("\n建议先单独安装依赖:")
            print("python start_windows.py --deps-only")
            sys.exit(1)
    
    # 检查数据
    if not args.skip_data:
        if not check_data():
            print("数据获取失败，但程序将继续运行...")
    
    # 训练模型
    if not args.skip_model:
        if not train_model():
            print("模型训练失败，但程序将继续运行...")
    
    # 启动应用
    start_app(args.host, args.port, args.debug)

if __name__ == "__main__":
    main()