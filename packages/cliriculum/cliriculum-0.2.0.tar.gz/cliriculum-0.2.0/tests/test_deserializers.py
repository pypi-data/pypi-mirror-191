from cliriculum.deserializers import Contact, Profile, Socials, URL
from cliriculum.deserializers import Dates, Period
from datetime import date, timedelta
import pytest


WEBSITE_1 = {
    "url": "https://github.com/sondalex/cliriculum",
    "logo": "github.com/sondalex/cliriculum",
    "classes": None,
    "text": None,
    "width": None,
    "height": None,
}
# fa-brands fa-linkedin"
WEBSITE_2 = {
    "url": "https://github.com/sondalex/cliriculum",
    "classes": "fa-brands fa-linkedin",
    "text": "github.com/sondalex/cliriculum",
    "width": "300px",
    "height": "300px",
}

KWARGS = [
    (
        {
            "profession": None,
            "email": None,
            "website": None,
            "socials": None,
            "number": None,
            "profile": None,
        },
        {
            "profession": "Data Scientist",
            "email": {"url": "test@email.com", "text": "test@email.com"},
            "website": WEBSITE_1,
            "socials": [WEBSITE_1],
            "number": WEBSITE_1,
            "profile": {"picture": "tests/fixtures/image.png"},
        },
        {
            "profession": "Data Scientist",
            "email": {"url": "test@email.com", "text": "test@email.com"},
            "website": WEBSITE_2,
            "socials": [WEBSITE_2],
            "number": WEBSITE_2,
        },
        {"profession": "Data Scientist"},
    )
]

PERIOD_KWARGS = [
    (
        {
            "start": date.today().isoformat(),
            "end": (date.today() + timedelta(1)).isoformat(),
            "logo": "github.com/sondalex/cliriculum",
            "width": "200px",
            "height": "200px",
            "classes": "fa-solid fa-location-pin",
        },
        {
            "start": date.today().isoformat(),
            "end": None,
            "logo": None,
            "width": None,
            "height": None,
            "classes": None,
        },
    )
]


class TestContact:
    @pytest.mark.parametrize("tuple", KWARGS)
    def test___init__(self, tuple):
        for dict_ in tuple:
            Contact("cliriculum", **dict_)
        with pytest.raises(TypeError):
            Contact()
        with pytest.raises(TypeError):
            Contact(**{})


class TestDates:
    @pytest.mark.parametrize("tuple", PERIOD_KWARGS)
    def test___init__(self, tuple):
        with pytest.raises(TypeError):
            Period(id="an-id")
        for dict_ in tuple:
            Period(id="an-id", **dict_)


class TestDates:
    @pytest.mark.parametrize("tuple", PERIOD_KWARGS)
    def test___init__(self, tuple):
        Dates({})  # not raise Error
        d = {f"an-id_{i}": item for i, item in enumerate(tuple)}
        Dates(d)
