"""Pager tests with a scripted fake console. (IF-CLI-005, D-16)"""
from lib import pager


class FakeConsole:
    def __init__(self, inputs):
        self.inputs = list(inputs)
        self.printed = []

    def input(self, prompt):
        self.printed.append(("prompt", prompt))
        return self.inputs.pop(0)

    def print(self, *args, **kwargs):
        self.printed.append(("print", " ".join(str(a) for a in args)))


def test_short_text_no_prompt():
    c = FakeConsole([])
    assert pager.show(c, "hello\nworld") is True
    assert not any(p[0] == "prompt" for p in c.printed)


def test_long_text_pages_and_quits():
    text = "\n".join(f"line {i}" for i in range(50))
    assert pager.show(FakeConsole([""]), text) is True
    c = FakeConsole(["q"])
    assert pager.show(c, text) is False
    assert any("—more—" in p[1] for p in c.printed if p[0] == "prompt")


def test_question_mark_in_pager():
    text = "\n".join(f"line {i}" for i in range(45))
    c = FakeConsole(["?", ""])
    assert pager.show(c, text) is True
    assert any("pager keys" in p[1] for p in c.printed if p[0] == "print")


def test_fence_never_torn():
    head = "\n".join(f"p{i}" for i in range(36))
    fence = "```c\n" + "\n".join(f"code {i}" for i in range(4)) + "\n```"
    pages = pager._pages(head + "\n\n" + fence + "\n\ntail\n", 40)
    assert len(pages) == 2
    assert pages[1].count("```") == 2  # fence intact on page 2
