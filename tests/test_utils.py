from bot.telegram_bot import escape_markdown_v2_strict

def test_escape_strict_handles_underscores():
    """
    Tests that the strict escaper correctly escapes underscores in command names.
    This is the test that would have caught our previous bug.
    """
    raw_text = "Use /my_subject to check."
    expected_text = r"Use /my\_subject to check\."
    assert escape_markdown_v2_strict(raw_text) == expected_text

def test_escape_strict_handles_all_chars():
    """
    Tests that the strict escaper handles a variety of special characters.
    """
    raw_text = "Hello! This is a test for *bold* and _italic_ text (with symbols +-=)."
    expected_text = r"Hello\! This is a test for \*bold\* and \_italic\_ text \(with symbols \+\-\=\)\."
    assert escape_markdown_v2_strict(raw_text) == expected_text

def test_escape_strict_handles_clean_text():
    """
    Tests that text with no special characters remains unchanged.
    """
    raw_text = "This is a clean sentence"
    assert escape_markdown_v2_strict(raw_text) == raw_text