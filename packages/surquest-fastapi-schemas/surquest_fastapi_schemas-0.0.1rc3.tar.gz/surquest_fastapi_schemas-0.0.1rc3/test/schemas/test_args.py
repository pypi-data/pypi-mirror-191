import pytest
import datetime as dt

from surquest.fastapi.schemas.args import Args

class TestArgs:

    ERRORS = {
        "value": "Wrong value: Expected: `{}`, Actual: `{}`",
        "type": "Wrong type: Expected: `{}`, Actual: `{}`"
    }

    @pytest.mark.parametrize(
        "arg,expected",
        [
            ("start_date", {"type": dt.date, "alias": "startDate"}),
            ("end_date", {"type": dt.date, "alias": "endDate"}),
            ("offset", {"type": int, "alias": "offset"}),
            ("limit", {"type": int, "alias": "limit"}),
        ]
    )
    def test__start_date__default(self, arg, expected):

        assert expected.get("type") == getattr(Args, arg)().type_, \
            self.ERRORS.get("type").format(
                expected.get("type"),
                getattr(Args, arg)().type_
            )

        # test alias
        assert expected.get("alias") == getattr(Args, arg)().query.alias, \
            self.ERRORS.get("type").format(
                expected.get("alias"),
                getattr(Args, arg)().query.alias
            )

    def test__start_date__custom(self):

        config = {
            "default": ...,
            "alias": "start_date"
        }

        assert dt.date == Args.start_date(**config).type_, \
            self.ERRORS.get("type").format(
                dt.date,
                Args.start_date().type_
            )

        # test alias
        assert config.get("alias") == Args.start_date(**config).query.alias, \
            self.ERRORS.get("value").format(
                config.get("alias"),
                Args.start_date().query.alias
            )