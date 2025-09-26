# Codeforces数据挖掘项目

## 项目概述

这是一个基于Flask的Web应用系统，专门用于分析Codeforces编程竞赛平台的题目数据。系统通过数据采集、机器学习建模、可视化分析和Web界面交互，为用户提供题目标签分布、难度预测和数据洞察功能。

## 核心功能

- **标签分析**: 分析特定标签在不同难度区间的分布情况
- **百分比统计**: 计算标签在指定分数区间的占比
- **机器学习预测**: 使用随机森林模型预测题目难度评级
- **数据可视化**: 提供直观的图表展示分析结果
- **交互式界面**: 用户友好的Web界面进行数据探索

## 技术栈

- **后端**: Flask, Python 3.7+
- **数据处理**: Pandas, NumPy
- **机器学习**: Scikit-learn
- **可视化**: Matplotlib, Seaborn
- **前端**: HTML5, CSS3, JavaScript
- **数据源**: Codeforces API

## 快速开始

### 方法1: 使用启动脚本（推荐）

```bash
# 安装Python依赖、获取数据、训练模型并启动应用
python start.py

# 自定义启动参数
python start.py --host 0.0.0.0 --port 8080 --debug

# 跳过某些步骤
python start.py --skip-deps --skip-model
```

### 方法2: 手动步骤

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **获取数据**
```bash
python api.py
```

3. **训练模型（可选）**
```bash
python run.py
```

4. **启动Web应用**
```bash
python app.py
```

访问 http://127.0.0.1:5000 开始使用

## 项目结构

```
Data-Mining/
├── api.py                  # 数据采集脚本
├── app.py                  # Flask主应用
├── run.py                  # 机器学习建模
├── Visualization.py        # 静态可视化分析
├── start.py               # 应用启动脚本
├── requirements.txt       # Python依赖
├── README.md             # 项目说明
├── codeforces_problems_with_solved.csv  # 数据文件
├── models/               # 机器学习模型目录
├── templates/            # HTML模板
│   ├── index.html        # 主页面
│   ├── result.html       # 标签分析结果
│   └── percentage_result.html  # 百分比分析结果
└── static/               # 静态资源
    └── style.css         # 样式文件
```

## 使用说明

### 标签分布分析
1. 在主页选择要分析的标签
2. 设置分数区间范围
3. 点击"分析标签分布"查看结果
4. 系统将显示该标签在所选区间的分布图表

### 标签占比分析
1. 选择要分析的标签和分数区间
2. 点击"查看标签占比"
3. 系统将显示该标签在区间内的百分比占比

### 机器学习模型
- 模型使用随机森林算法预测题目难度
- 特征包括：题目索引、标签集合、解决人数
- 训练后的模型保存在 `models/` 目录

## API说明

### 数据采集
- `api.py`: 从Codeforces API获取题目数据
- 支持自动重试和错误处理
- 数据保存为CSV格式

### Web API端点
- `GET /`: 主页面
- `POST /analyze`: 标签分布分析
- `POST /percentage_analyze`: 标签占比分析

## 开发说明

### 添加新功能
1. 在`app.py`中添加新的路由
2. 创建对应的HTML模板
3. 更新CSS样式（如需要）

### 自定义可视化
编辑`Visualization.py`添加新的图表类型

### 模型优化
在`run.py`中调整模型参数或尝试不同算法

## 故障排除

### 常见问题

1. **字体显示问题**
   - 系统会自动回退到可用字体
   - Linux系统建议安装中文字体支持

2. **数据获取失败**
   - 检查网络连接
   - 确认Codeforces API可访问
   - 查看日志获取详细错误信息

3. **模型训练过慢**
   - 可以跳过模型训练直接使用Web功能
   - 使用`--skip-model`参数

### 日志查看
程序运行时会在控制台输出详细日志信息

## 贡献指南

1. Fork本项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

## 许可证

本项目采用MIT许可证开源。

## 联系我们

如有问题或建议，请提交Issue或联系开发团队。