import json
from pathlib import Path

import requests

def fetch_posts(url: str) -> list:
    """请求公开 API，返回 JSON 数据"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_posts(posts: list, limit: int = 10) -> list:
    """提取前 limit 条文章的关键信息"""
    result = []

    for post in posts[:limit]:
        item = {
            "id": post.get("id"),
            "title": post.get("title"),
            "body": post.get("body")
        }
        result.append(item)

    return result

def save_to_json(data: list, output_path: Path) -> None:
    """保存数据到 JSON 文件"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    current_dir = Path(__file__).parent
    output_file = current_dir / "result.json"

    try:
        posts = fetch_posts(url)
        extracted_data = extract_posts(posts, limit=10)
        save_to_json(extracted_data, output_file)

        print("数据获取成功！")
        print(f"共保存 {len(extracted_data)} 条数据到: {output_file}")

    except requests.RequestException as e:
        print(f"请求出错: {e}")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()