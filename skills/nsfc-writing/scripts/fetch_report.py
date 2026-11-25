#!/usr/bin/env python3
"""用浏览器里已通过验证的报告令牌，逐页下载国家自然科学基金基础研究知识库的结题报告页面。

前提：用户本人已在浏览器中打开该项目的结题报告并完成滑块验证。本脚本不处理验证，
只使用用户提供的报告令牌（reportToken，可选附带 cookies）按页请求，令牌过期即停止。

如何拿到令牌：在浏览器开发者工具的“网络”面板中，找到发往
/api/baseQuery/completeProjectReport 的请求，复制请求参数里的 reportToken；
网页前端设定的有效期约 29 分钟，请在拿到后尽快运行。

用法：
  python3 fetch_report.py --id 项目ID --token 报告令牌 --out 报告图片目录
  python3 fetch_report.py --url "https://kd.nsfc.cn/finalDetails?id=..." --token ... --out ...
可选：--cookie "浏览器中复制的 Cookie 字符串" 或 --cookie-file 文件；--user-agent 与浏览器一致；
      --start/--end 限定页码；--delay 每页间隔秒数（默认 1.5，不低于 1）。

页面保存为 <out>/<页码>.png；已存在的页面会跳过，可中断后重跑续传。
下载完成后用 merge_pages.py 合并为 PDF。依赖：requests。
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_URL = "https://kd.nsfc.cn"
REPORT_API = f"{BASE_URL}/api/baseQuery/completeProjectReport"
DEFAULT_UA = "Mozilla/5.0 (compatible; nsfc-writing report fetcher)"
MIN_IMAGE_BYTES = 500
EXIT_OK, EXIT_ARGS, EXIT_TOKEN, EXIT_NET = 0, 1, 3, 4


def project_id_from(args: argparse.Namespace) -> str:
    if args.id:
        return args.id.strip()
    if args.url:
        q = parse_qs(urlparse(args.url).query)
        if q.get("id"):
            return q["id"][0].strip()
    return ""


def build_session(args: argparse.Namespace):
    import requests

    s = requests.Session()
    s.headers.update({
        "User-Agent": args.user_agent or DEFAULT_UA,
        "Accept": "application/json, text/plain, */*",
        "Referer": BASE_URL,
    })
    cookie = args.cookie
    if args.cookie_file:
        cookie = Path(args.cookie_file).read_text(encoding="utf-8").strip()
    if cookie:
        s.headers["Cookie"] = cookie
    return s


def fetch_page(session, project_id: str, index: int, token: str, timeout: float = 15.0):
    """返回 (状态, 内容)。状态：ok / end / token / error。"""
    r = session.post(REPORT_API, data={"id": project_id, "index": index, "reportToken": token}, timeout=timeout)
    r.raise_for_status()
    result = r.json()
    code = result.get("code")
    if code == 460:
        return "token", result.get("message", "")
    if code != 200 or not result.get("data") or not result["data"].get("url"):
        return "end", ""
    url = result["data"]["url"]
    img = session.get(url if url.startswith("http") else BASE_URL + url, timeout=timeout)
    img.raise_for_status()
    if len(img.content) < MIN_IMAGE_BYTES:
        return "end", ""
    return "ok", img.content


def save_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="用已验证的报告令牌逐页下载结题报告页面")
    p.add_argument("--id", help="项目 ID（finalDetails?id= 后面的值）")
    p.add_argument("--url", help="项目详情页地址，含 id 参数")
    p.add_argument("--token", required=True, help="浏览器中通过验证后得到的 reportToken")
    p.add_argument("--cookie", help="浏览器中复制的 Cookie 字符串")
    p.add_argument("--cookie-file", help="保存 Cookie 字符串的文件")
    p.add_argument("--user-agent", help="与浏览器一致的 User-Agent")
    p.add_argument("--out", required=True, type=Path, help="保存页面图片的目录")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=0, help="最后一页（默认直到没有下一页）")
    p.add_argument("--delay", type=float, default=1.5, help="每页间隔秒数，不低于 1")
    args = p.parse_args(argv)

    project_id = project_id_from(args)
    if not project_id:
        print("需要 --id 或带 id 参数的 --url", file=sys.stderr)
        return EXIT_ARGS
    delay = max(1.0, args.delay)
    try:
        session = build_session(args)
    except ImportError:
        print("缺少 requests：pip install requests", file=sys.stderr)
        return EXIT_ARGS
    args.out.mkdir(parents=True, exist_ok=True)

    index, saved, skipped = args.start, 0, 0
    while not args.end or index <= args.end:
        target = args.out / f"{index}.png"
        if target.exists() and target.stat().st_size >= MIN_IMAGE_BYTES:
            skipped += 1
            index += 1
            continue
        try:
            status, content = fetch_page(session, project_id, index, args.token)
        except Exception as e:  # 网络或解析错误：停止，保留已下载页面
            print(f"第 {index} 页请求失败：{e}；已保存 {saved} 页，重跑同一命令可续传", file=sys.stderr)
            return EXIT_NET
        if status == "token":
            print(f"第 {index} 页：令牌已失效或未通过验证（{content}）。请回浏览器重新完成验证、复制新令牌后重跑；已保存的页面会跳过。", file=sys.stderr)
            return EXIT_TOKEN
        if status == "end":
            break
        save_atomic(target, content)
        saved += 1
        print(f"第 {index} 页已保存（本次 {saved} 页）", flush=True)
        index += 1
        time.sleep(delay)

    print(f"完成：本次保存 {saved} 页，跳过已有 {skipped} 页，目录 {args.out}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
