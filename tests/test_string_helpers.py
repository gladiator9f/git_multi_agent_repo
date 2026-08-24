from src.utils.string_helpers import slugify, truncate, sanitize_html


class TestSlugify:
    def test_spaces_to_hyphens(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars_removed(self):
        assert slugify("Hello, World! #2026") == "hello-world-2026"

    def test_unicode_normalized(self):
        assert slugify("café résumé") == "cafe-resume"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_already_slug(self):
        assert slugify("hello-world") == "hello-world"


class TestTruncate:
    def test_short_text_unchanged(self):
        assert truncate("hello", 10) == "hello"

    def test_exact_length_unchanged(self):
        assert truncate("hello", 5) == "hello"

    def test_long_text_truncated(self):
        assert truncate("hello world", 8) == "hello..."

    def test_custom_suffix(self):
        assert truncate("hello world", 9, suffix=">>") == "hello w>>"

    def test_default_max_length(self):
        short = "a" * 50
        assert truncate(short) == short


class TestSanitizeHtml:
    def test_strips_tags(self):
        assert sanitize_html("<b>bold</b>") == "bold"

    def test_nested_tags(self):
        assert sanitize_html("<div><p>text</p></div>") == "text"

    def test_no_tags(self):
        assert sanitize_html("plain text") == "plain text"

    def test_self_closing_tags(self):
        assert sanitize_html("line<br/>break") == "linebreak"

    def test_empty_string(self):
        assert sanitize_html("") == ""
