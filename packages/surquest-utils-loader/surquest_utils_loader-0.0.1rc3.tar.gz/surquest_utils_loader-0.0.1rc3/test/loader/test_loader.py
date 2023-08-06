import pytest
from surquest.utils.loader import Loader, DictDot


class TestLoader:
    ERROR_MSG = "Wrong value: Expected: `{}`, Actual: `{}`"

    @pytest.mark.parametrize(
        "file,expected",
        [
            ("../data/sample.json", {"type": DictDot, "key": "family"}),
            ("../data/sample.yaml", {"type": DictDot, "key": "family"}),
            ("../data/sample.sql", {"type": str})
        ]
    )
    def test__load__success(self, file, expected):
        "Method tests the load method of the Loader class"

        data = Loader.load(file)
        assert expected.get("type") == type(data), \
            self.ERROR_MSG.format(
                expected.get("type"), type(data)
            )
        if expected.get("key") is not None:
            assert expected.get("key") in data.keys(), \
                self.ERROR_MSG.format(expected.get("key"))
            assert "Smith" == data.family.name, \
                self.ERROR_MSG.format(
                    "Smith", data.get("family")
                )

    @pytest.mark.parametrize(
        "file,expected",
        [
            ("../data/sample.json", {"type": dict, "key": "family"}),
            ("../data/sample.yaml", {"type": dict, "key": "family"})
        ]
    )
    def test__load_as_dict__success(self, file, expected):
        """Method tests the load methods for JSON and YAML of the Loader class"""

        data = Loader.load(file, output_type=dict)
        assert expected.get("type") == type(data), \
            self.ERROR_MSG.format(
                expected.get("type"), type(data)
            )
        assert expected.get("key") in data.keys(), \
            self.ERROR_MSG.format(expected.get("key"))
        assert "Smith" == data.get("family").get("name"), \
            self.ERROR_MSG.format(
                "Smith", data.get("family")
            )
