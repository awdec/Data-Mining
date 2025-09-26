import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 全局中文字体设置
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
except:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 模型和预处理器文件路径
MODEL_PATH = "models/rating_prediction_model.joblib"
PREPROCESSOR_PATH = "models/preprocessors.joblib"
DATA_PATH = "codeforces_problems_with_solved.csv"

# 创建模型目录
if not os.path.exists("models"):
    os.makedirs("models")

def load_and_preprocess_data(data_path):
    """加载和预处理数据"""
    print("正在加载数据...")
    df = pd.read_csv(data_path, encoding="utf-8")
    
    # 提取标签列表
    df["tags_list"] = df["tags"].fillna("").apply(lambda s: s.split(";") if s else [])
    
    # 丢弃任何在 index、tags_list、rating、solvedCount 上有缺失的行
    df = df.dropna(subset=["index", "tags_list", "rating", "solvedCount"])
    
    # 提取 solvedCount 并处理类型
    df["solvedCount"] = df["solvedCount"].astype(float)
    
    print(f"数据加载完成，共 {len(df)} 条记录")
    return df


def create_features(df):
    """创建特征矩阵"""
    print("正在创建特征...")
    
    # 准备目标值
    y = df["rating"].astype(float)
    
    # 对 index 做 One-Hot 编码
    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_index = ohe.fit_transform(df[["index"]])
    
    # 对 tags_list 做多标签二值化
    mlb = MultiLabelBinarizer(sparse_output=False)
    X_tags = mlb.fit_transform(df["tags_list"])
    
    # 将 solvedCount 加入特征矩阵
    X_solved = df["solvedCount"].values.reshape(-1, 1)
    
    # 合并所有特征
    X = np.hstack([X_index, X_tags, X_solved])
    
    print(f"特征矩阵形状：{X.shape}")
    
    return X, y, ohe, mlb


def train_model(X, y):
    """训练模型"""
    print("正在训练模型...")
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 训练随机森林回归模型
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # 在测试集上评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"测试集 MSE: {mse:.2f}")
    print(f"测试集 R²: {r2:.3f}")
    
    return model, X_train, X_test, y_train, y_test, y_pred


def save_model_and_preprocessors(model, ohe, mlb):
    """保存模型和预处理器"""
    print("正在保存模型...")
    
    # 保存模型
    joblib.dump(model, MODEL_PATH)
    
    # 保存预处理器
    preprocessors = {
        'ohe': ohe,
        'mlb': mlb
    }
    joblib.dump(preprocessors, PREPROCESSOR_PATH)
    
    print(f"模型已保存到: {MODEL_PATH}")
    print(f"预处理器已保存到: {PREPROCESSOR_PATH}")


def load_model_and_preprocessors():
    """加载模型和预处理器"""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
        return None, None, None
    
    model = joblib.load(MODEL_PATH)
    preprocessors = joblib.load(PREPROCESSOR_PATH)
    
    return model, preprocessors['ohe'], preprocessors['mlb']


def predict_rating(model, ohe, mlb, index, tags_list, solved_count):
    """预测单个题目的难度评级"""
    # 准备数据
    sample_df = pd.DataFrame({
        "index": [index],
        "tags_list": [tags_list],
        "solvedCount": [solved_count]
    })
    
    # 特征工程
    X_idx = ohe.transform(sample_df[["index"]])
    X_tags = mlb.transform(sample_df["tags_list"])
    X_solved = sample_df["solvedCount"].values.reshape(-1, 1)
    
    X_sample = np.hstack([X_idx, X_tags, X_solved])
    
    # 预测
    prediction = model.predict(X_sample)[0]
    
    return prediction

def main():
    """主函数"""
    print("="*50)
    print("Codeforces 题目难度预测模型训练")
    print("="*50)
    
    # 检查是否已有训练好的模型
    model, ohe, mlb = load_model_and_preprocessors()
    
    if model is not None:
        print("发现已训练的模型，是否重新训练？(y/n): ", end="")
        choice = input().lower().strip()
        if choice != 'y':
            print("使用已有模型进行示例预测...")
            # 示例预测
            sample_predictions = [
                ("A", ["greedy", "implementation"], 1500),
                ("C", ["dp", "graphs"], 500),
                ("D", ["math", "number theory"], 300)
            ]
            
            for idx, tags, solved in sample_predictions:
                pred = predict_rating(model, ohe, mlb, idx, tags, solved)
                print(f"Index={idx}, Tags={tags}, Solved={solved} -> 预测 rating={pred:.1f}")
            return
    
    # 加载和预处理数据
    df = load_and_preprocess_data(DATA_PATH)
    
    # 创建特征
    X, y, ohe, mlb = create_features(df)
    
    # 训练模型
    model, X_train, X_test, y_train, y_test, y_pred = train_model(X, y)
    
    # 保存模型
    save_model_and_preprocessors(model, ohe, mlb)
    
    print("\n模型训练完成！")
