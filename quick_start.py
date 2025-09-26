#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 跳过复杂的依赖安装，直接启动应用
适用于已经有基础Python环境的情况
"""

import sys
import os

def check_basic_imports():
    """检查基本导入"""
    missing_packages = []
    
    try:
        import flask
        print("✓ Flask 可用")
    except ImportError:
        missing_packages.append("Flask")
    
    try:
        import pandas
        print("✓ Pandas 可用")
    except ImportError:
        missing_packages.append("pandas")
    
    try:
        import matplotlib
        print("✓ Matplotlib 可用")
    except ImportError:
        missing_packages.append("matplotlib")
    
    try:
        import sklearn
        print("✓ Scikit-learn 可用")
    except ImportError:
        missing_packages.append("scikit-learn")
    
    return missing_packages

def main():
    print("=" * 50)
    print("Codeforces数据挖掘项目快速启动")
    print("=" * 50)
    
    # 检查基本依赖
    missing = check_basic_imports()
    
    if missing:
        print(f"\n缺少以下包: {', '.join(missing)}")
        print("请手动安装:")
        for pkg in missing:
            print(f"  pip install {pkg}")
        return
    
    print("\n所有基本依赖已满足！")
    
    # 检查数据文件
    if not os.path.exists("codeforces_problems_with_solved.csv"):
        print("\n数据文件不存在，您可以:")
        print("1. 运行 'python api.py' 获取数据")
        print("2. 或者直接启动应用（使用示例数据）")
        
        choice = input("\n是否现在获取数据？(y/n): ").lower().strip()
        if choice == 'y':
            try:
                import subprocess
                subprocess.check_call([sys.executable, "api.py"])
                print("✓ 数据获取成功")
            except:
                print("数据获取失败，但应用仍可运行")
    
    # 启动应用
    print("\n启动Web应用...")
    print("访问 http://127.0.0.1:5000 开始使用")
    
    try:
        # 设置环境变量
        os.environ["FLASK_HOST"] = "127.0.0.1"
        os.environ["FLASK_PORT"] = "5000"
        os.environ["FLASK_DEBUG"] = "True"
        
        # 直接导入并运行
        import app
    except KeyboardInterrupt:
        print("\n应用已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        print("\n请检查错误信息并手动运行 'python app.py'")

if __name__ == "__main__":
    main()