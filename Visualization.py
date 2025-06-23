# visualize_codeforces.py
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 全局中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Read the dataset
df = pd.read_csv('codeforces_problems_with_solved.csv')

# Ensure data types
# Some ratings may be NaN; drop these for analyses requiring rating
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 1. Rating Distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['rating'].dropna(), bins=20, kde=True)
plt.xlabel('Rating')
plt.ylabel('Number of Problems')
plt.title('Codeforces题目难度分布')
plt.tight_layout()
plt.show()

# 2. Solved Count vs Rating
# 2a. Scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df['rating'], df['solvedCount'], alpha=0.6)
plt.xlabel('Rating')
plt.ylabel('Solved Count')
plt.title('题目被解决次数与难度的关系')
plt.tight_layout()
plt.show()

# 2b. Averaged solvedCount by rating bins
df_bins = df.dropna(subset=['rating', 'solvedCount']).copy()
bins = list(range(800, 3001, 200))
labels = [f"{b}-{b+200}" for b in bins[:-1]]
df_bins['rating_bin'] = pd.cut(df_bins['rating'], bins=bins, labels=labels, include_lowest=True)
avg_solved = df_bins.groupby('rating_bin', observed=False)['solvedCount'].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(avg_solved['rating_bin'], avg_solved['solvedCount'], marker='o')
plt.xlabel('Rating Bin')
plt.ylabel('Average Solved Count')
plt.title('不同难度区间的平均解决次数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Top 10 Tags by Frequency
# Explode tags into individual rows (split by semicolon)
exploded = df.dropna(subset=['tags']).copy()
exploded['tag_list'] = exploded['tags'].astype(str).str.split(';')
exploded = exploded.explode('tag_list')
exploded['tag_list'] = exploded['tag_list'].str.strip()
tag_counts = exploded['tag_list'].value_counts().nlargest(10)

plt.figure(figsize=(6, 4))
tag_counts.sort_values().plot(kind='barh')
plt.xlabel('Number of Problems')
plt.title('Codeforces最常见的前10个标签')
plt.tight_layout()
plt.show()

# 4. Stacked Bar Chart: Top 5 Tags Across Rating Bins
# Determine top 5 tags overall
top5_tags = exploded['tag_list'].value_counts().nlargest(5).index.tolist()
# Filter exploded to top 5
filtered = exploded[exploded['tag_list'].isin(top5_tags)].copy()
filtered['rating_bin'] = pd.cut(filtered['rating'], bins=bins, labels=labels, include_lowest=True)
# Count per bin and tag
tag_bin_counts = filtered.groupby(['rating_bin', 'tag_list'], observed=False).size().unstack(fill_value=0)
# Plot stacked bar

tag_bin_counts[top5_tags].plot(kind='bar', stacked=True)
plt.xlabel('Rating Bin')
plt.ylabel('Count of Problems')
plt.title('热门标签在各个难度区间的分布')
plt.xticks(rotation=45)
plt.legend(title='Tag')
plt.tight_layout()
plt.show()


# 重新计算比例：使用各 rating_bin 的所有标签总数作为分母
total_tag_counts_per_bin = exploded.copy()
total_tag_counts_per_bin['rating_bin'] = pd.cut(total_tag_counts_per_bin['rating'], bins=bins, labels=labels, include_lowest=True)
total_counts = total_tag_counts_per_bin.groupby('rating_bin', observed=False).size()
tag_bin_props_corrected = tag_bin_counts[top5_tags].div(total_counts, axis=0)

# Plot stacked bar - corrected percentage
tag_bin_props_corrected.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
plt.xlabel('Rating Bin')
plt.ylabel('占比')
plt.title('热门标签在各个难度区间的分布（占所有标签的占比）')
plt.xticks(rotation=45)
plt.legend(title='Tag', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()