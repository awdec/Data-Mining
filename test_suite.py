#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codeforces数据挖掘项目单元测试
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import pandas as pd

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestAPIModule(unittest.TestCase):
    """测试API数据采集模块"""
    
    def setUp(self):
        """测试前的设置"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """测试后的清理"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    @patch('api.requests.get')
    def test_fetch_all_problems_success(self, mock_get):
        """测试成功获取数据"""
        import api
        
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "result": {
                "problems": [
                    {
                        "contestId": 1,
                        "index": "A",
                        "name": "Test Problem",
                        "rating": 800,
                        "tags": ["implementation"]
                    }
                ],
                "problemStatistics": [
                    {
                        "contestId": 1,
                        "index": "A",
                        "solvedCount": 1000
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        problems, stats = api.fetch_all_problems_and_stats()
        
        self.assertEqual(len(problems), 1)
        self.assertEqual(len(stats), 1)
        self.assertEqual(problems[0]["name"], "Test Problem")
    
    def test_write_to_csv(self):
        """测试CSV写入功能"""
        import api
        
        problems = [
            {
                "contestId": 1,
                "index": "A", 
                "name": "Test Problem",
                "rating": 800,
                "tags": ["implementation", "greedy"]
            }
        ]
        
        stats = [
            {
                "contestId": 1,
                "index": "A",
                "solvedCount": 1000
            }
        ]
        
        filename = "test_output.csv"
        api.write_to_csv(problems, stats, filename)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filename))
        
        # 验证内容
        df = pd.read_csv(filename)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['name'], "Test Problem")
        self.assertEqual(df.iloc[0]['solvedCount'], 1000)

class TestAppModule(unittest.TestCase):
    """测试Flask应用模块"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建测试数据文件
        test_data = {
            'contestId': [1, 2],
            'index': ['A', 'B'],
            'name': ['Problem A', 'Problem B'],
            'rating': [800, 1200],
            'solvedCount': [1000, 500],
            'tags': ['implementation;greedy', 'dp;graphs']
        }
        df = pd.DataFrame(test_data)
        df.to_csv('codeforces_problems_with_solved.csv', index=False)
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_app_import(self):
        """测试应用导入"""
        try:
            import app
            self.assertIsNotNone(app.app)
        except ImportError as e:
            self.fail(f"Failed to import app module: {e}")
    
    def test_cache_functions(self):
        """测试缓存功能"""
        import app
        
        # 测试缓存保存和加载
        test_data = {"test": "data"}
        cache_key = "test_key"
        
        app.save_to_cache(test_data, cache_key)
        loaded_data = app.load_from_cache(cache_key)
        
        self.assertEqual(test_data, loaded_data)

class TestRunModule(unittest.TestCase):
    """测试机器学习模块"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建测试数据
        test_data = {
            'contestId': [1, 2, 3, 4, 5],
            'index': ['A', 'B', 'C', 'A', 'B'],
            'name': ['Problem A', 'Problem B', 'Problem C', 'Problem A2', 'Problem B2'],
            'rating': [800, 1200, 1600, 900, 1300],
            'solvedCount': [1000, 500, 200, 800, 400],
            'tags': ['implementation;greedy', 'dp;graphs', 'math;number theory', 'implementation', 'dp;greedy']
        }
        df = pd.DataFrame(test_data)
        df.to_csv('codeforces_problems_with_solved.csv', index=False)
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_data_loading(self):
        """测试数据加载"""
        import run
        
        df = run.load_and_preprocess_data("codeforces_problems_with_solved.csv")
        self.assertGreater(len(df), 0)
        self.assertIn('tags_list', df.columns)
    
    def test_feature_creation(self):
        """测试特征创建"""
        import run
        
        df = run.load_and_preprocess_data("codeforces_problems_with_solved.csv")
        X, y, ohe, mlb = run.create_features(df)
        
        self.assertEqual(X.shape[0], len(df))
        self.assertEqual(len(y), len(df))
        self.assertIsNotNone(ohe)
        self.assertIsNotNone(mlb)

class TestVisualizationModule(unittest.TestCase):
    """测试可视化模块"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建测试数据
        test_data = {
            'contestId': [1, 2, 3],
            'index': ['A', 'B', 'C'],
            'name': ['Problem A', 'Problem B', 'Problem C'],
            'rating': [800, 1200, 1600],
            'solvedCount': [1000, 500, 200],
            'tags': ['implementation;greedy', 'dp;graphs', 'math;number theory']
        }
        df = pd.DataFrame(test_data)
        df.to_csv('codeforces_problems_with_solved.csv', index=False)
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_visualization_import(self):
        """测试可视化模块导入"""
        try:
            import Visualization
            self.assertTrue(hasattr(Visualization, 'generate_all_visualizations'))
        except ImportError as e:
            self.fail(f"Failed to import Visualization module: {e}")

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建完整的测试数据
        test_data = {
            'contestId': list(range(1, 21)),
            'index': ['A'] * 10 + ['B'] * 10,
            'name': [f'Problem {i}' for i in range(1, 21)],
            'rating': [800 + i * 100 for i in range(20)],
            'solvedCount': [1000 - i * 40 for i in range(20)],
            'tags': ['implementation;greedy'] * 5 + ['dp;graphs'] * 5 + ['math'] * 5 + ['strings'] * 5
        }
        df = pd.DataFrame(test_data)
        df.to_csv('codeforces_problems_with_solved.csv', index=False)
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_full_pipeline(self):
        """测试完整的数据处理流水线"""
        # 测试数据加载
        df = pd.read_csv('codeforces_problems_with_solved.csv')
        self.assertGreater(len(df), 0)
        
        # 测试数据预处理
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df_clean = df.dropna(subset=['rating'])
        self.assertGreater(len(df_clean), 0)
        
        # 测试标签处理
        df_clean['tag_list'] = df_clean['tags'].astype(str).str.split(';')
        exploded = df_clean.explode('tag_list')
        self.assertGreater(len(exploded), len(df_clean))

def run_tests():
    """运行所有测试"""
    print("=" * 50)
    print("运行Codeforces数据挖掘项目单元测试")
    print("=" * 50)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestAPIModule,
        TestAppModule, 
        TestRunModule,
        TestVisualizationModule,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 报告结果
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n测试状态: {'✓ 通过' if success else '✗ 失败'}")
    
    return success

if __name__ == '__main__':
    run_tests()