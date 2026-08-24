from datetime import datetime
from src.utils.date_helpers import format_date, parse_date, date_diff_days


class TestFormatDate:
    def test_default_format(self):
        dt = datetime(2026, 8, 24)
        assert format_date(dt) == "2026-08-24"

    def test_custom_format(self):
        dt = datetime(2026, 8, 24, 14, 30)
        assert format_date(dt, "%m/%d/%Y %H:%M") == "08/24/2026 14:30"


class TestParseDate:
    def test_default_format(self):
        result = parse_date("2026-08-24")
        assert result == datetime(2026, 8, 24)

    def test_custom_format(self):
        result = parse_date("08/24/2026", "%m/%d/%Y")
        assert result == datetime(2026, 8, 24)

    def test_invalid_raises(self):
        try:
            parse_date("not-a-date")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestDateDiffDays:
    def test_positive_diff(self):
        start = datetime(2026, 8, 1)
        end = datetime(2026, 8, 24)
        assert date_diff_days(start, end) == 23

    def test_negative_diff(self):
        start = datetime(2026, 8, 24)
        end = datetime(2026, 8, 1)
        assert date_diff_days(start, end) == -23

    def test_same_day(self):
        dt = datetime(2026, 8, 24)
        assert date_diff_days(dt, dt) == 0
