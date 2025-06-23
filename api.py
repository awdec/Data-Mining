#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import csv
import sys

API_URL = "https://codeforces.com/api/problemset.problems"
OUTPUT_CSV = "codeforces_problems_with_solved.csv"


def fetch_all_problems_and_stats():
    """
    调用 Codeforces API 获取所有题目及统计信息
    返回：
        problems (list of dict)：题目列表
        stats (list of dict)：对应的统计列表，每项含 contestId, index, solvedCount
    """
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"请求 Codeforces API 出错：{e}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if data.get("status") != "OK":
        print(f"API 返回状态非 OK: {data.get('status')}", file=sys.stderr)
        sys.exit(1)

    result = data["result"]
    return result["problems"], result["problemStatistics"]


def write_to_csv(problems, stats, filename):
    """
    将题目及统计数据写入 CSV
    参数：
        problems (list of dict)
        stats (list of dict)
        filename (str)
    """
    # 构造 (contestId, index) -> solvedCount 映射
    solved_map = {
        (s["contestId"], s["index"]): s.get("solvedCount", 0)
        for s in stats
    }

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # 表头，增加 solvedCount 列
        writer.writerow(["contestId", "index", "name", "rating", "solvedCount", "tags"])
        for p in problems:
            contest_id = p.get("contestId", "")
            index = p.get("index", "")
            name = p.get("name", "").replace("\n", " ")
            rating = p.get("rating", "")
            solved = solved_map.get((contest_id, index), "")
            tags_str = ";".join(p.get("tags", []))
            writer.writerow([contest_id, index, name, rating, solved, tags_str])


def main():
    print("开始获取题目及通过人数数据...")
    problems, stats = fetch_all_problems_and_stats()
    print(f"共获取 {len(problems)} 道题，写入 CSV 文件…")
    write_to_csv(problems, stats, OUTPUT_CSV)
    print("完成，文件已生成：", OUTPUT_CSV)


if __name__ == "__main__":
    main()
