from app.database.search import _find_known_value


def test_find_known_value_matches_whole_word() -> None:
    priorities = {
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "critical": "Critical",
    }

    assert _find_known_value("Show low priority tickets", priorities) == "Low"


def test_find_known_value_does_not_match_inside_another_word() -> None:
    priorities = {
        "low": "Low",
    }

    assert _find_known_value(
        "What KB article should support follow?",
        priorities,
    ) is None


def test_find_known_value_is_case_insensitive() -> None:
    categories = {
        "vpn": "VPN",
    }

    assert _find_known_value("Show all VPN tickets", categories) == "VPN"


def test_find_known_value_returns_none_for_unknown_value() -> None:
    categories = {
        "vpn": "VPN",
        "printer": "Printer",
    }

    assert _find_known_value("Show payroll records", categories) is None
