"""fetch_report.py 的离线测试：用假会话模拟知识库接口，不访问网络。"""
import sys
import tempfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, sys.argv[1])
import fetch_report as fr  # noqa: E402

PNG = b"\x89PNG" + b"0" * 1000


class Resp:
    def __init__(self, payload=None, content=b""):
        self._p, self.content = payload, content

    def raise_for_status(self):
        pass

    def json(self):
        return self._p


class FakeSession:
    """pages：可下载的总页数；expire_at：从第几页起令牌失效（0 表示不失效）。"""

    def __init__(self, pages=3, expire_at=0):
        self.pages, self.expire_at, self.posts = pages, expire_at, []

    def post(self, url, data, timeout):
        self.posts.append(dict(data))
        i = int(data["index"])
        assert data["reportToken"] == "TOKEN", "未携带令牌"
        if self.expire_at and i >= self.expire_at:
            return Resp({"code": 460, "message": "请完成滑块验证后查看报告", "data": None})
        if i > self.pages:
            return Resp({"code": 200, "data": None})
        return Resp({"code": 200, "data": {"url": f"/img/{i}.png?e=9999999999"}})

    def get(self, url, timeout):
        return Resp(content=PNG)


def run(session, out, *extra):
    with mock.patch.object(fr, "build_session", return_value=session), mock.patch.object(fr.time, "sleep"):
        return fr.main(["--url", "https://kd.nsfc.cn/finalDetails?id=abc123", "--token", "TOKEN", "--out", str(out), *extra])


with tempfile.TemporaryDirectory() as d:
    out = Path(d) / "pages"
    # 正常下载 3 页后遇到空页结束
    s = FakeSession(pages=3)
    assert run(s, out) == fr.EXIT_OK
    assert sorted(p.name for p in out.iterdir()) == ["1.png", "2.png", "3.png"]
    assert s.posts[0]["id"] == "abc123"
    # 重跑：已有页面跳过，不再请求前 3 页
    s2 = FakeSession(pages=3)
    assert run(s2, out) == fr.EXIT_OK
    assert [p["index"] for p in s2.posts] == [4]

with tempfile.TemporaryDirectory() as d:
    out = Path(d) / "pages"
    # 第 3 页起令牌失效：保存前 2 页，返回令牌失效码，不留临时文件
    s = FakeSession(pages=5, expire_at=3)
    assert run(s, out) == fr.EXIT_TOKEN
    assert sorted(p.name for p in out.iterdir()) == ["1.png", "2.png"]
    # 换新令牌续传（假会话不再失效），从第 3 页接着下
    s2 = FakeSession(pages=5)
    assert run(s2, out) == fr.EXIT_OK
    assert [p["index"] for p in s2.posts][:1] == [3]
    assert len(list(out.glob("*.png"))) == 5 and not list(out.glob("*.part"))

with tempfile.TemporaryDirectory() as d:
    # --end 限定页码；--delay 低于 1 时按 1 处理（不报错）
    out = Path(d) / "pages"
    s = FakeSession(pages=10)
    assert run(s, out, "--end", "2", "--delay", "0.1") == fr.EXIT_OK
    assert len(list(out.glob("*.png"))) == 2

# 缺少项目 ID
assert fr.main(["--token", "T", "--out", "/tmp/x-not-used"]) == fr.EXIT_ARGS
print("fetch_report 离线测试通过")
