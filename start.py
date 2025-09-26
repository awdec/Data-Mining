#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codeforces数据挖掘项目启动脚本
"""

import os
import sys
import subprocess
import argparse

def check_dependencies():
    """检查Python依赖"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖检查完成")
    except subprocess.CalledProcessError:
        print("✗ 依赖安装失败")
        sys.exit(1)

def check_data():
    """检查数据文件"""
    if not os.path.exists("codeforces_problems_with_solved.csv"):
        print("⚠ 数据文件不存在，正在获取数据...")
        try:
            subprocess.check_call([sys.executable, "api.py"])
            print("✓ 数据获取完成")
        except subprocess.CalledProcessError:
            print("✗ 数据获取失败")
            sys.exit(1)
    else:
        print("✓ 数据文件已存在")

def train_model():
    """训练机器学习模型"""
    print("开始训练机器学习模型...")
    try:
        subprocess.check_call([sys.executable, "run.py"])
        print("✓ 模型训练完成")
    except subprocess.CalledProcessError:
        print("✗ 模型训练失败")
        sys.exit(1)

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

def main():
    parser = argparse.ArgumentParser(description="Codeforces数据挖掘项目启动脚本")
    parser.add_argument("--host", default="127.0.0.1", help="Flask应用主机地址")
    parser.add_argument("--port", type=int, default=5000, help="Flask应用端口")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--skip-deps", action="store_true", help="跳过依赖检查")
    parser.add_argument("--skip-data", action="store_true", help="跳过数据检查")
    parser.add_argument("--skip-model", action="store_true", help="跳过模型训练")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Codeforces数据挖掘项目启动器")
    print("=" * 50)
    
    # 检查依赖
    if not args.skip_deps:
        check_dependencies()
    
    # 检查数据
    if not args.skip_data:
        check_data()
    
    # 训练模型
    if not args.skip_model:
        train_model()
    
    # 启动应用
    start_app(args.host, args.port, args.debug)

if __name__ == "__main__":
    main()