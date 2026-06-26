#!/usr/bin/env python3
"""Build Patsnap/Zhihuiya Analytics result URLs for simple search queries.

Usage:
  python scripts/build_search_url.py "关键词A 关键词B" "CN117964767B"
"""

import sys
from urllib.parse import urlencode

BASE_URL = "https://analytics.zhihuiya.com/search/result/tablelist/1"


def build_url(query: str) -> str:
    params = {
        "sort": "sdesc",
        "limit": "100",
        "q": query,
        "_type": "query",
        "search_mode": "publication",
    }
    return f"{BASE_URL}?{urlencode(params)}"


def main() -> int:
    queries = sys.argv[1:]
    if not queries:
        print('Usage: python scripts/build_search_url.py "query" ["query"...]', file=sys.stderr)
        return 2

    for query in queries:
        if not query.strip():
            print("Error: query must not be empty", file=sys.stderr)
            return 2
        print(build_url(query))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
