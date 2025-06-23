import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 全局中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取包含 solvedCount 的数据
df = pd.read_csv("codeforces_problems_with_solved.csv", encoding="utf-8")

# 2. 提取标签列表
df["tags_list"] = df["tags"].fillna("").apply(lambda s: s.split(";") if s else [])

# 3. 丢弃任何在 index、tags_list、rating、solvedCount 上有缺失的行
df = df.dropna(subset=["index", "tags_list", "rating", "solvedCount"])

# 4. 提取 solvedCount 并处理类型
df["solvedCount"] = df["solvedCount"].astype(float)

# 5. 准备目标值
y = df["rating"].astype(float)

# 6. 对 index 做 One-Hot 编码
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_index = ohe.fit_transform(df[["index"]])

# 7. 对 tags_list 做多标签二值化
mlb = MultiLabelBinarizer(sparse_output=False)
X_tags = mlb.fit_transform(df["tags_list"])

# 8. 将 solvedCount 加入特征矩阵
X_solved = df["solvedCount"].values.reshape(-1, 1)

# 9. 合并所有特征
X = np.hstack([X_index, X_tags, X_solved])

# 10. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 11. 训练随机森林回归模型
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 12. 在测试集上评估
y_pred = model.predict(X_test)
print(f"测试集 MSE: {mean_squared_error(y_test, y_pred):.2f}")
print(f"测试集 R²: {r2_score(y_test, y_pred):.3f}")

# 13. 可视化

# 13.1 实际值 vs 预测值 散点图
plt.figure()
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         linestyle='--', linewidth=2)
plt.xlabel("真实 rating")
plt.ylabel("预测 rating")
plt.title("实际值 vs 预测值")
plt.show()

# 13.2 特征重要性条形图（前20）
importances = model.feature_importances_
feature_names = list(ohe.get_feature_names_out(["index"])) + list(mlb.classes_) + ["solvedCount"]
indices = np.argsort(importances)[-20:]

plt.figure(figsize=(8, 6))
plt.barh(np.array(feature_names)[indices], importances[indices])
plt.xlabel("重要性得分")
plt.title("前 20 个特征重要性")
plt.tight_layout()
plt.show()

# 13.3 学习曲线
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, scoring='neg_mean_squared_error',
    train_sizes=np.linspace(0.1, 1.0, 10), n_jobs=-1
)
train_error = -train_scores.mean(axis=1)
val_error   = -val_scores.mean(axis=1)

plt.figure()
plt.plot(train_sizes, train_error, 'o-', label="训练集 MSE")
plt.plot(train_sizes, val_error,   'o--', label="验证集 MSE")
plt.xlabel("训练样本数")
plt.ylabel("均方误差")
plt.title("学习曲线")
plt.legend()
plt.show()

# 13.4 残差分布图
residuals = y_test - y_pred
plt.figure()
plt.hist(residuals, bins=50)
plt.xlabel("残差 (真实 - 预测)")
plt.ylabel("频次")
plt.title("残差分布")
plt.show()

# 14. 示例：对新样本预测
sample = pd.DataFrame({
    "index": ["A", "C"],
    "tags_list": [["greedy", "implementation"], ["dp", "graphs"]],
    "solvedCount": [1500, 500]
})
X_idx_s = ohe.transform(sample[["index"]])
X_tgs_s = mlb.transform(sample["tags_list"])
X_solved_s = sample["solvedCount"].values.reshape(-1, 1)
pred = model.predict(np.hstack([X_idx_s, X_tgs_s, X_solved_s]))
for inp, p in zip(sample.values, pred):
    print(f"Index={inp[0]}, Tags={inp[1]}, Solved={inp[2]} -> 预测 rating={p:.1f}")
