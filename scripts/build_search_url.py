#!/usr/bin/env python3
"""Build Patsnap/Zhihuiya Analytics result URLs for simple search queries.

Usage:
  python scripts/build_search_url.py "关键词A 关键词B" "CN117964767B"
  python scripts/build_search_url.py --init-output-dir outputs/case "CN117964767B"
"""

import argparse
from pathlib import Path
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


def init_output_dir(path: str) -> None:
    output_dir = Path(path).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    search_log = output_dir / "search_log.md"
    if not search_log.exists():
        search_log.write_text(
            "# Prior-Art Search Log\n\n"
            "Status: initialized before browser search\n",
            encoding="utf-8",
        )

    run_report = output_dir / "run_report.md"
    if not run_report.exists():
        run_report.write_text(
            "# Run Report\n\n"
            "Status: initialized; final report pending\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Patsnap/Zhihuiya Analytics result URLs."
    )
    parser.add_argument(
        "--init-output-dir",
        metavar="DIR",
        help="create disclosure sidecar placeholders before printing URLs",
    )
    parser.add_argument("queries", nargs="+")
    args = parser.parse_args()

    if args.init_output_dir:
        init_output_dir(args.init_output_dir)

    queries = args.queries
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
