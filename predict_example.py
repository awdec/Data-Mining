#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codeforces题目难度预测示例
展示如何使用已训练的模型进行预测
"""

import sys
import os
from run import load_model_and_preprocessors, predict_rating

def predict_single_problem():
    """预测单个题目的难度"""
    print("=" * 50)
    print("Codeforces题目难度预测器")
    print("=" * 50)
    
    # 加载模型和预处理器
    print("正在加载模型...")
    model, ohe, mlb = load_model_and_preprocessors()
    
    if model is None:
        print("❌ 模型未找到，请先训练模型:")
        print("   python run.py")
        return
    
    print("✅ 模型加载成功！")
    
    # 获取用户输入
    print("\n请输入题目信息进行预测:")
    
    # 题目索引
    index = input("题目索引 (如 A, B, C, D): ").strip().upper()
    if not index:
        index = "A"
    
    # 题目标签
    print("\n常见标签: implementation, greedy, math, dp, graphs, strings, number theory")
    tags_input = input("题目标签 (用逗号分隔): ").strip()
    if tags_input:
        tags_list = [tag.strip() for tag in tags_input.split(',')]
    else:
        tags_list = ["implementation"]  # 默认标签
    
    # 解决人数
    solved_input = input("预估解决人数 (默认1000): ").strip()
    try:
        solved_count = int(solved_input) if solved_input else 1000
    except ValueError:
        solved_count = 1000
    
    # 进行预测
    print(f"\n正在预测...")
    print(f"题目索引: {index}")
    print(f"题目标签: {tags_list}")
    print(f"解决人数: {solved_count}")
    
    try:
        predicted_rating = predict_rating(model, ohe, mlb, index, tags_list, solved_count)
        
        print("\n" + "=" * 30)
        print(f"🎯 预测难度: {predicted_rating:.0f}")
        print("=" * 30)
        
        # 提供难度解释
        if predicted_rating <= 1000:
            difficulty = "新手 (Newbie)"
        elif predicted_rating <= 1200:
            difficulty = "初学者 (Pupil)"
        elif predicted_rating <= 1400:
            difficulty = "专家 (Specialist)"
        elif predicted_rating <= 1600:
            difficulty = "专家 (Expert)"
        elif predicted_rating <= 1900:
            difficulty = "候选大师 (Candidate Master)"
        elif predicted_rating <= 2100:
            difficulty = "大师 (Master)"
        elif predicted_rating <= 2300:
            difficulty = "国际大师 (International Master)"
        else:
            difficulty = "特级大师 (Grandmaster)"
        
        print(f"难度等级: {difficulty}")
        
    except Exception as e:
        print(f"❌ 预测失败: {e}")

def predict_batch_problems():
    """批量预测题目难度"""
    print("\n" + "=" * 50)
    print("批量预测模式")
    print("=" * 50)
    
    # 加载模型
    model, ohe, mlb = load_model_and_preprocessors()
    if model is None:
        print("❌ 模型未找到，请先训练模型")
        return
    
    # 预定义的测试用例
    test_cases = [
        ("A", ["implementation", "greedy"], 2000),
        ("B", ["math", "number theory"], 1500),
        ("C", ["dp", "graphs"], 800),
        ("D", ["implementation"], 500),
        ("E", ["math", "combinatorics"], 200),
        ("A", ["strings", "implementation"], 1800),
        ("B", ["greedy", "sortings"], 1200),
        ("C", ["dp", "trees"], 600),
    ]
    
    print("预测结果:")
    print("-" * 60)
    print(f"{'索引':<6} {'标签':<25} {'解决数':<8} {'预测难度':<10}")
    print("-" * 60)
    
    for index, tags, solved in test_cases:
        try:
            predicted = predict_rating(model, ohe, mlb, index, tags, solved)
            tags_str = ", ".join(tags)
            print(f"{index:<6} {tags_str:<25} {solved:<8} {predicted:.0f}")
        except Exception as e:
            print(f"{index:<6} {'错误':<25} {solved:<8} {'失败'}")

def main():
    """主函数"""
    if not os.path.exists("models"):
        print("❌ 模型目录不存在，请先训练模型:")
        print("   python run.py")
        return
    
    while True:
        print("\n" + "=" * 50)
        print("选择预测模式:")
        print("1. 单个题目预测")
        print("2. 批量预测示例")
        print("3. 退出")
        print("=" * 50)
        
        choice = input("请选择 (1-3): ").strip()
        
        if choice == "1":
            predict_single_problem()
        elif choice == "2":
            predict_batch_problems()
        elif choice == "3":
            print("再见！")
            break
        else:
            print("无效选择，请重试")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()