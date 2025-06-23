import os

import matplotlib
import pandas as pd

matplotlib.use('Agg')  # 设置非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request
import io
import base64

# 全局中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

# 数据预处理
data_path = os.path.join('data', 'codeforces_problems_with_solved.csv')
df = pd.read_csv(data_path)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 处理标签列，分割标签并进行统计
exploded = df.dropna(subset=['tags']).copy()
exploded['tag_list'] = exploded['tags'].astype(str).str.split(';')
exploded = exploded.explode('tag_list')
exploded['tag_list'] = exploded['tag_list'].str.strip()

# 定义分数区间
bins = list(range(800, 3501, 100))
labels = [f"{b}-{b + 100}" for b in bins[:-1]]

# 预计算所有标签的分布
exploded['rating_bin'] = pd.cut(exploded['rating'], bins=bins, labels=labels, include_lowest=True)
tag_bin_counts = exploded.groupby(['rating_bin', 'tag_list'], observed=False).size().unstack(fill_value=0)
total_counts = exploded.groupby('rating_bin', observed=False).size()


@app.route('/')
def index():
    # 获取所有唯一标签供前端选择
    unique_tags = exploded['tag_list'].unique().tolist()
    return render_template('index.html', tags=unique_tags)


@app.route('/analyze', methods=['POST'])
def analyze():
    selected_tag = request.form.get('tag')
    selected_min_rating = int(request.form.get('min_rating'))
    selected_max_rating = int(request.form.get('max_rating'))

    if not selected_tag:
        return render_template('index.html', error="请选择一个标签")

    # 直接使用用户选择的区间作为 selected_bin
    selected_bin = f"{selected_min_rating}-{selected_max_rating}"

    # 过滤所选标签和所选分数区间的数据
    filtered_data = exploded[(exploded['tag_list'] == selected_tag) &
                             (exploded['rating'] >= selected_min_rating) &
                             (exploded['rating'] <= selected_max_rating)]

    # 计算所选标签在所选分数区间的数量
    tag_count = len(filtered_data)

    # 计算所选分数区间的总问题数量（基于原始数据框）
    total_bin_count = len(df[(df['rating'] >= selected_min_rating) &
                             (df['rating'] <= selected_max_rating)])

    print(total_bin_count)

    if total_bin_count == 0:
        percentage = 0
    else:
        percentage = (tag_count / total_bin_count) * 100

    # 绘制柱状图
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制所有标签在所选分数区间的分布
    filtered_bin_data = exploded[(exploded['rating'] >= selected_min_rating) &
                                 (exploded['rating'] < selected_max_rating)]
    tag_distribution = filtered_bin_data['tag_list'].value_counts().head(10)

    tag_distribution.plot(kind='bar', ax=ax, color=sns.color_palette('viridis', len(tag_distribution)))

    # 高亮显示所选标签
    if selected_tag in tag_distribution.index:
        ax.patches[list(tag_distribution.index).index(selected_tag)].set_color('red')

    ax.set_title(f'标签在 {selected_bin} 分数区间的分布')
    ax.set_xlabel('')
    ax.set_ylabel('问题数量')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    # 将图表转换为 base64 编码的图像
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # 关闭图表以释放资源
    plt.close(fig)

    return render_template('result.html',
                           tag=selected_tag,
                           rating_bin=selected_bin,
                           percentage=f"{percentage:.2f}",
                           plot_url=plot_url)


@app.route('/percentage_analyze', methods=['POST'])
def percentage_analyze():
    selected_tag = request.form.get('tag')
    selected_min_rating = int(request.form.get('min_rating'))
    selected_max_rating = int(request.form.get('max_rating'))

    if not selected_tag:
        return render_template('index.html', error="请选择一个标签")

    selected_bin = f"{selected_min_rating}-{selected_max_rating}"

    # 使用 exploded 数据框进行过滤
    filtered_tag_data = exploded[(exploded['tag_list'] == selected_tag) &
                                 (exploded['rating'] >= selected_min_rating) &
                                 (exploded['rating'] <= selected_max_rating)]

    tag_count = len(filtered_tag_data)

    # 使用原始数据框 df 计算总问题数
    total_bin_count = len(df[(df['rating'] >= selected_min_rating) &
                             (df['rating'] <= selected_max_rating)])

    if total_bin_count == 0:
        percentage = 0
    else:
        percentage = (tag_count / total_bin_count) * 100

    # 使用原始数据框 df 获取所有标签在当前分数区间内的数量和占比
    filtered_total_data = df[(df['rating'] >= selected_min_rating) &
                             (df['rating'] <= selected_max_rating)]

    # 提取标签并计算每个标签的数量
    tag_list = []
    for tags in filtered_total_data['tags']:
        if pd.notna(tags):
            tag_list.extend(tags.split(';'))

    # 统计每个标签的数量
    tag_distribution = pd.Series(tag_list).value_counts().head(10)
    tag_percentages = (tag_distribution / total_bin_count) * 100

    # 绘制柱状图，显示每个标签的百分比
    fig, ax = plt.subplots(figsize=(10, 6))
    tag_percentages.plot(kind='bar', ax=ax, color=sns.color_palette('viridis', len(tag_percentages)))

    # 高亮显示所选标签
    if selected_tag in tag_percentages.index:
        ax.patches[list(tag_percentages.index).index(selected_tag)].set_color('red')

    ax.set_title(f'标签在 {selected_bin} 分数区间的占比')
    ax.set_xlabel('')
    ax.set_ylabel('占比 (%)')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close(fig)

    return render_template('percentage_result.html',
                           tag=selected_tag,
                           rating_bin=selected_bin,
                           percentage=f"{percentage:.2f}",
                           plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)
