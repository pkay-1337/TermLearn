"""`?` help-key tests with a scripted fake console. (SRS VR-007, IF-CLI-006)"""
from lib import keys


class FakeConsole:
    def __init__(self, inputs):
        self.inputs = list(inputs)
        self.printed = []

    def input(self, prompt):
        self.printed.append(("prompt", prompt))
        return self.inputs.pop(0)

    def print(self, *args, **kwargs):
        self.printed.append(("print", " ".join(str(a) for a in args)))


def test_passthrough():
    c = FakeConsole(["2"])
    assert keys.ask(c, "answer: ", "quiz") == "2"
    assert not any(p[0] == "print" for p in c.printed)


def test_question_mark_shows_help_then_reprompts():
    c = FakeConsole(["?", "3"])
    assert keys.ask(c, "answer: ", "quiz") == "3"
    helps = [p[1] for p in c.printed if p[0] == "print"]
    assert any("1-N" in h for h in helps), helps


def test_help_word_and_mode_specific_text():
    c = FakeConsole(["help", "q"])
    assert keys.ask(c, "> ", "lab") == "q"
    helps = [p[1] for p in c.printed if p[0] == "print"]
    assert any("hidden tests" in h for h in helps), helps


def test_unknown_mode_falls_back():
    c = FakeConsole(["?", "x"])
    assert keys.ask(c, "> ", "nope") == "x"


def test_reserved_set_documents_pack_constraint():
    assert keys.RESERVED == {"?", "help"}
