"""Unit tests for ISO/IEC/IEEE 29148:2018 Multi-Lab Workspace and Correctness Engine."""
from pathlib import Path
import pytest
from lib import lab_workspace as lw


@pytest.fixture
def temp_labs_dir(tmp_path, monkeypatch):
    """Overrides labs directory with a temporary path."""
    monkeypatch.setattr(lw, "get_labs_base_dir", lambda: tmp_path / "labs")
    return tmp_path / "labs"


def test_provision_and_preserve_student_work(temp_labs_dir):
    lab_def = {
        "id": "lab1",
        "title": "Modular C Components",
        "files": [
            {"path": "engine.h", "content": "#ifndef ENGINE_H\n#define ENGINE_H\n#endif\n"},
            {"path": "engine.c", "content": "#include \"engine.h\"\nvoid init(void) {}\n"}
        ]
    }

    # 1. First-time provisioning
    wdir = lw.provision_lab_workspace("test-book", "ch01", lab_def)
    assert (wdir / "engine.h").exists()
    assert (wdir / "engine.c").exists()
    assert "init(void)" in (wdir / "engine.c").read_text()

    # 2. Student edits engine.c
    (wdir / "engine.c").write_text("#include \"engine.h\"\n/* student solution */\n")

    # 3. Subsequent provisioning does NOT overwrite student edit (REQ-LAB-DIR-004)
    lw.provision_lab_workspace("test-book", "ch01", lab_def, reset=False)
    assert "student solution" in (wdir / "engine.c").read_text()

    # 4. Explicit reset DOES restore initial file (REQ-LAB-DIR-005)
    lw.provision_lab_workspace("test-book", "ch01", lab_def, reset=True)
    assert "init(void)" in (wdir / "engine.c").read_text()


def test_list_and_read_write_files(temp_labs_dir):
    lab_def = {
        "id": "lab1",
        "files": [
            {"path": "src/module.c", "content": "int x = 10;\n"},
            {"path": "include/module.h", "content": "extern int x;\n"}
        ]
    }
    wdir = lw.provision_lab_workspace("book", "ch01", lab_def)
    files = lw.list_workspace_files(wdir)
    assert files == ["include/module.h", "src/module.c"]

    # Read and write
    content = lw.read_workspace_file(wdir, "src/module.c")
    assert content == "int x = 10;\n"
    lw.write_workspace_file(wdir, "src/module.c", "int x = 20;\n")
    assert lw.read_workspace_file(wdir, "src/module.c") == "int x = 20;\n"


def test_command_execution_in_workspace_cwd(temp_labs_dir):
    lab_def = {
        "id": "lab1",
        "files": [
            {"path": "data.txt", "content": "TermLearn Workspace Verification"}
        ]
    }
    wdir = lw.provision_lab_workspace("book", "ch01", lab_def)
    res = lw.run_command_in_workspace(wdir, "cat data.txt")
    assert res["returncode"] == 0
    assert "TermLearn Workspace Verification" in res["stdout"]


def test_command_denylist_enforcement(temp_labs_dir):
    wdir = temp_labs_dir / "test"
    wdir.mkdir(parents=True)
    res = lw.run_command_in_workspace(wdir, "rm -rf /")
    assert res["denied"] is True
    assert "prohibited pattern" in res["error"]


def test_input_vs_expected_output_verification_pass(temp_labs_dir):
    lab_def = {
        "id": "lab1",
        "files": [
            {"path": "echoer.sh", "content": "#!/bin/sh\nread -r val\necho \"Processed: $val\"\n"}
        ],
        "commands": {
            "run": "sh echoer.sh"
        },
        "test_cases": [
            {
                "name": "Single Line Input Test",
                "stdin": "42\n",
                "expect": "Processed: 42\n",
                "expect_exit": 0
            }
        ]
    }
    wdir = lw.provision_lab_workspace("book", "ch01", lab_def)
    report = lw.run_lab_verification(wdir, lab_def)
    assert report["passed"] is True
    assert report["cases_passed"] == 1
    assert report["cases_run"] == 1
    assert report["diff"] == ""


def test_input_vs_expected_output_verification_diff_on_failure(temp_labs_dir):
    lab_def = {
        "id": "lab1",
        "files": [
            {"path": "echoer.sh", "content": "#!/bin/sh\necho \"Wrong Output\"\n"}
        ],
        "commands": {
            "run": "sh echoer.sh"
        },
        "test_cases": [
            {
                "name": "Failing Case",
                "stdin": "",
                "expect": "Expected Output\n",
                "expect_exit": 0
            }
        ]
    }
    wdir = lw.provision_lab_workspace("book", "ch01", lab_def)
    report = lw.run_lab_verification(wdir, lab_def)
    assert report["passed"] is False
    assert report["cases_passed"] == 0
    assert "-Expected Output" in report["diff"]
    assert "+Wrong Output" in report["diff"]
