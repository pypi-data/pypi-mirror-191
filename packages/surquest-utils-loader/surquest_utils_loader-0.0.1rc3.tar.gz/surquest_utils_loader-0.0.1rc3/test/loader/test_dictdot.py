import pytest
from surquest.utils.loader import Loader


class TestDictDot:
    ERROR_MSG = "Wrong value: Expected: `{}`, Actual: `{}`"

    @pytest.mark.parametrize(
        "file,expected",
        [
            ("../data/sample.json",
             {"name": "Smith", "members": 2, "firstMember": "John"}),
            ("../data/sample.yaml",
             {"name": "Smith", "members": 2, "firstMember": "John"})
        ]
    )
    def test__success(self, file, expected):
        """Method tests the load method of the Loader class"""

        data = Loader.load(file)
        assert expected.get("name") == data.family.name, \
            self.ERROR_MSG.format(
                expected.get("name"), data.get("family")
            )

        assert expected.get("members") == len(data.family.members), \
            self.ERROR_MSG.format(
                expected.get("members"), len(data.family.members)
            )

        assert expected.get("firstMember") == data.family.members[0].name, \
            self.ERROR_MSG.format(
                expected.get("firstMember"), data.family.members[0].name
            )
