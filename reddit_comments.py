import requests

def fetch_reddit_comments(permalink, limit=10):
    """
    从 Reddit 的某条帖子抓取评论内容。
    :param permalink: 例如 "/r/canada/comments/abc123/example_post_title/"
    :param limit: 要抓取的评论条数
    :return: 评论列表，每条是一个 dict：author, body, created_utc
    """
    headers = {'User-agent': 'EchoWatch-CommentScanner'}
    url = f"https://www.reddit.com{permalink}.json?limit={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[-] Failed to fetch comments: {response.status_code}")
        return []

    try:
        data = response.json()
        comments_raw = data[1]["data"]["children"]
        comments = []
        for c in comments_raw:
            if c["kind"] != "t1":
                continue  # 跳过非评论内容（如广告或加载器）
            info = c["data"]
            comments.append({
                "author": info.get("author", "[deleted]"),
                "body": info.get("body", ""),
                "created_utc": info.get("created_utc", 0)
            })
            if len(comments) >= limit:
                break
        return comments
    except Exception as e:
        print(f"[-] Error parsing comments: {e}")
        return []
