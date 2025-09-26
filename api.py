#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import csv
import sys
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "https://codeforces.com/api/problemset.problems"
OUTPUT_CSV = "codeforces_problems_with_solved.csv"
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒


def fetch_all_problems_and_stats():
    """
    调用 Codeforces API 获取所有题目及统计信息
    实现重试机制处理网络错误
    返回：
        problems (list of dict)：题目列表
        stats (list of dict)：对应的统计列表，每项含 contestId, index, solvedCount
    """
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"正在获取数据... (尝试 {attempt + 1}/{MAX_RETRIES})")
            resp = requests.get(API_URL, timeout=30)
            resp.raise_for_status()
            
            data = resp.json()
            if data.get("status") != "OK":
                logger.error(f"API 返回状态非 OK: {data.get('status')}")
                if attempt < MAX_RETRIES - 1:
                    logger.info(f"等待 {RETRY_DELAY} 秒后重试...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    sys.exit(1)
            
            result = data["result"]
            logger.info(f"成功获取 {len(result['problems'])} 道题目数据")
            return result["problems"], result["problemStatistics"]
            
        except requests.RequestException as e:
            logger.error(f"请求 Codeforces API 出错：{e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("所有重试尝试失败，退出程序")
                sys.exit(1)
        except Exception as e:
            logger.error(f"未知错误：{e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("所有重试尝试失败，退出程序")
                sys.exit(1)


def write_to_csv(problems, stats, filename):
    """
    将题目及统计数据写入 CSV
    参数：
        problems (list of dict)
        stats (list of dict)
        filename (str)
    """
    try:
        # 构造 (contestId, index) -> solvedCount 映射
        solved_map = {
            (s["contestId"], s["index"]): s.get("solvedCount", 0)
            for s in stats
        }
        
        logger.info(f"开始写入 {len(problems)} 道题目到 {filename}")
        
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            # 表头，增加 solvedCount 列
            writer.writerow(["contestId", "index", "name", "rating", "solvedCount", "tags"])
            
            for i, p in enumerate(problems):
                contest_id = p.get("contestId", "")
                index = p.get("index", "")
                name = p.get("name", "").replace("\n", " ")
                rating = p.get("rating", "")
                solved = solved_map.get((contest_id, index), "")
                tags_str = ";".join(p.get("tags", []))
                writer.writerow([contest_id, index, name, rating, solved, tags_str])
                
                # 每处理 1000 道题显示进度
                if (i + 1) % 1000 == 0:
                    logger.info(f"已处理 {i + 1}/{len(problems)} 道题")
        
        logger.info(f"成功写入数据到 {filename}")
        
    except Exception as e:
        logger.error(f"写入 CSV 文件失败：{e}")
        sys.exit(1)


def main():
    logger.info("开始获取题目及通过人数数据...")
    try:
        problems, stats = fetch_all_problems_and_stats()
        logger.info(f"共获取 {len(problems)} 道题，开始写入 CSV 文件…")
        write_to_csv(problems, stats, OUTPUT_CSV)
        logger.info(f"完成，文件已生成：{OUTPUT_CSV}")
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序执行出错：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
