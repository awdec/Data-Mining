# visualize_codeforces.py
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# 全局中文字体设置
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
except:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 设置全局样式
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# 创建输出目录
output_dir = 'visualization_output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def save_plot(filename, dpi=300, bbox_inches='tight'):
    """统一保存图表的函数"""
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"图表已保存: {filepath}")

def generate_all_visualizations():
    """生成所有可视化图表的主函数"""
    print("\n" + "="*50)
    print("Codeforces 数据可视化分析")
    print("="*50)
    
    # Read the dataset
    print("正在加载数据...")
    df = pd.read_csv('codeforces_problems_with_solved.csv')
    
    # Ensure data types
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    print(f"数据加载完成，共 {len(df)} 条记录")
    
    # 1. Rating Distribution
    print("\n正在生成雾度分布图...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rating'].dropna(), bins=20, kde=True, alpha=0.7)
    plt.xlabel('Rating')
    plt.ylabel('Number of Problems')
    plt.title('Codeforces题目雾度分布')
    plt.grid(True, alpha=0.3)
    save_plot('rating_distribution.png')
    plt.close()
    
    # 2. Solved Count vs Rating - Scatter plot
    print("正在生成解决数量与雾度关系图...")
    plt.figure(figsize=(12, 6))
    plt.scatter(df['rating'], df['solvedCount'], alpha=0.6, s=20)
    plt.xlabel('Rating')
    plt.ylabel('Solved Count')
    plt.title('题目被解决次数与雾度的关系')
    plt.grid(True, alpha=0.3)
    save_plot('solved_vs_rating_scatter.png')
    plt.close()
    
    # 2b. Averaged solvedCount by rating bins
    print("正在生成平均解决数量分析...")
    df_bins = df.dropna(subset=['rating', 'solvedCount']).copy()
    bins = list(range(800, 3001, 200))
    labels = [f"{b}-{b+200}" for b in bins[:-1]]
    df_bins['rating_bin'] = pd.cut(df_bins['rating'], bins=bins, labels=labels, include_lowest=True)
    avg_solved = df_bins.groupby('rating_bin', observed=False)['solvedCount'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(avg_solved['rating_bin'], avg_solved['solvedCount'], marker='o', linewidth=2, markersize=8)
    plt.xlabel('Rating Bin')
    plt.ylabel('Average Solved Count')
    plt.title('不同雾度区间的平均解决次数')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    save_plot('avg_solved_by_rating.png')
    plt.close()

    # 3. Top 10 Tags by Frequency
    print("正在生成标签频率统计图...")
    exploded = df.dropna(subset=['tags']).copy()
    exploded['tag_list'] = exploded['tags'].astype(str).str.split(';')
    exploded = exploded.explode('tag_list')
    exploded['tag_list'] = exploded['tag_list'].str.strip()
    tag_counts = exploded['tag_list'].value_counts().nlargest(10)
    
    plt.figure(figsize=(10, 6))
    tag_counts.sort_values().plot(kind='barh', color=sns.color_palette('viridis', len(tag_counts)))
    plt.xlabel('Number of Problems')
    plt.title('Codeforces最常见的前10个标签')
    plt.grid(True, alpha=0.3)
    save_plot('top_tags_frequency.png')
    plt.close()
    
    # 4. Stacked Bar Chart: Top 5 Tags Across Rating Bins
    print("正在生成标签分布堆叠图...")
    top5_tags = exploded['tag_list'].value_counts().nlargest(5).index.tolist()
    filtered = exploded[exploded['tag_list'].isin(top5_tags)].copy()
    filtered['rating_bin'] = pd.cut(filtered['rating'], bins=bins, labels=labels, include_lowest=True)
    tag_bin_counts = filtered.groupby(['rating_bin', 'tag_list'], observed=False).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 6))
    tag_bin_counts[top5_tags].plot(kind='bar', stacked=True, colormap='tab10')
    plt.xlabel('Rating Bin')
    plt.ylabel('Count of Problems')
    plt.title('热门标签在各个雾度区间的分布')
    plt.xticks(rotation=45)
    plt.legend(title='Tag', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    save_plot('tags_distribution_stacked.png')
    plt.close()
    
    # 5. Tag Distribution Percentage
    print("正在生成标签占比分布图...")
    total_tag_counts_per_bin = exploded.copy()
    total_tag_counts_per_bin['rating_bin'] = pd.cut(total_tag_counts_per_bin['rating'], bins=bins, labels=labels, include_lowest=True)
    total_counts = total_tag_counts_per_bin.groupby('rating_bin', observed=False).size()
    tag_bin_props = tag_bin_counts[top5_tags].div(total_counts, axis=0)
    
    plt.figure(figsize=(12, 6))
    tag_bin_props.plot(kind='bar', stacked=True, colormap='Set3')
    plt.xlabel('Rating Bin')
    plt.ylabel('占比')
    plt.title('热门标签在各个雾度区间的分布（占所有标签的占比）')
    plt.xticks(rotation=45)
    plt.legend(title='Tag', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    save_plot('tags_percentage_distribution.png')
    plt.close()
    
    print(f"\n✓ 所有图表已生成并保存到 '{output_dir}' 目录")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
if __name__ == "__main__":
    generate_all_visualizations()