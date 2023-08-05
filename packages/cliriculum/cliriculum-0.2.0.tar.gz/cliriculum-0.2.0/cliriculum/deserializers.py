from datetime import date
from typing import Union, List, Dict
from collections import UserDict


class Dates(UserDict):
    """
    Deserializer of date metadata

    Examples
    --------
    >>> d = load_json("dates.json")
    >>> dates = Dates(d)

    Attributes
    ----------
    periods: List[Periods]
    """

    def __setitem__(self, key, item):
        new_value = Period(id=key, **item)
        self.data[key] = new_value


class Period:
    """

    Attributes
    ----------
    start: str
    end: Union[str, None]
    idx: str
    logo: Union[str, None]
    width: Union[str, None]
    height: Union[str, None]
    classes: Union[str, None] classes has priority over logo in :py:mod:`cliriculum.renderers`
    """

    def __init__(
        self,
        id: str,
        start: date,
        end: Union[date, None] = None,
        logo: Union[str, None] = None,
        width: Union[str, None] = None,
        height: Union[str, None] = None,
        classes: Union[str, None] = None,
    ):
        """

        Parameters
        ----------
        id : str
        start : str
            The start of the period
        end : Union[str, None]
            The end of the period
        logo: Union[str, None]
            A path towards a logo
        width: Union[str, None]
            Width of logo
        height:  Union[str, None]
            Height of logo
        classes: Union[str, None]
            css classnames
            `classes="class1 class2"`
        """
        if start is None:
            raise ValueError(
                "`start` of {classname} can not be set to None".format(
                    classname=self.__class__.__name__
                )
            )
        start = date.fromisoformat(start)
        if end is not None:
            end = date.fromisoformat(end)

        self.start = start
        self.end = end
        self.idx = id
        self.logo = logo
        self.width = width
        self.height = height
        self.classes = classes

    def __str__(self):
        return f"Index: {self.idx} with start:{self.start} and end: {self.end}"


class URL:
    """
    Attributes
    ----------
    logo: str
    url: Union[str, None]
    classes: str
        See :py:class:`Period`
    text: str
    """

    def __init__(
        self,
        url: Union[str, None],
        logo: Union[str, None] = None,
        classes: Union[str, None] = None,
        text: Union[str, None] = None,
        width: Union[str, None] = None,
        height: Union[str, None] = None,
    ):
        self.logo = logo
        self.url = url
        self.classes = classes
        self.text = text
        self.width = width
        self.height = height


class Website(URL):
    pass


class Social(URL):
    pass


class Number(URL):
    pass


class Email(URL):
    pass


class Socials:
    """
    Attributes
    ----------
    children: List[Social]
    """

    def __init__(self, socials_list: List[Dict]):
        """
        Parameters
        ----------
        socials_dict : List[Dict]
            A list of dictionaries
            Passed to :py:class:`Social` as named arguments
        """

        self.children = [Social(**dict_) for dict_ in socials_list]


class Profile(URL):
    """
    Profile fields.

    Attributes:
    -----------
    ...: Attributes from: :py:class:`URL`
    """

    def __init__(
        self,
        picture: Union[str, None],
        width: Union[str, None] = "200px",
        height: Union[str, None] = "200px",
    ):
        """
        Parameters
        ----------
        picture : Union[str, None], optional
            Picture path, by default None
            passed as super(URL).__init__(logo=picture)
        width : Union[str, None], optional
            Width height, by default "200px"
        height : Union[str, None], optional
            Picture height, by default "200px"
        """
        super().__init__(url=None, width=width, height=height, logo=picture)


class Contact:
    """
    Contact deserializer.

    Attributes
    ----------
    name: str
    profession: str
    email: Email
    website: Website
    socials: Socials
    number: Number
    """

    def __init__(
        self,
        name,
        profession: Union[str, None] = None,
        email: Union[str, None] = None,
        website: Union[str, None] = None,
        socials: Union[str, None] = None,
        number: Union[str, None] = None,
        profile: Union[str, None] = None,
    ):
        """
        name:
            Required
            Single string (first name last name)
        profession: Union[str, None]
            Defaults to None.
        email: Union[str, None]
            Defaults to None.
        website: Union[str, None]
            Defaults to None.
        socials: Union[str, None]
            Defaults to None.
        number: Union[str, None]
            Defaults to None

        Examples
        --------
        >>> from cliriculum.parsers import load_json
        >>> c = load_json("contact.json")
        >>> Contact(**c)
        """
        self.name = name
        self.profession = profession
        # all classes subclassing URL require url parameter at least
        # i.e:
        # - Email
        # - Website
        # - Number
        if email is None:
            email = {"url": None}  # bypassing restriction
        if website is None:
            website = {"url": None}
        if socials is None:
            socials = []
        if profile is None:
            profile = {"picture": None}
        if number is None:
            number = {"url": None}

        self.email = Email(**email)
        self.website = Website(**website)
        self.socials = Socials(socials)

        self.number = Number(**number)
        self.profile = Profile(**profile)


class Location:
    def __init__(self, id: str, location: str, classes: Union[str, None] = None):
        """

        Parameters
        ----------
        id : str
            An id to match with content
        location : str
            _description_
        classes : Union[str, None], optional
            _description_, by default None
        """
        self.classes = classes
        self.location = location
        self.idx = id


class Locations(UserDict):
    """

    Parameters
    ----------
    UserDict : _type_

    Example
    -------
    >>> from cliriculum.parsers import load_json
    >>> from cliriculum.deserializers import Locations
    >>> l = load_json("location.json")
    >>> Locations(l)
    """

    def __setitem__(self, key, item):
        new_value = Location(id=key, **item)
        self.data[key] = new_value


class Job:
    def __init__(
        self, title: Union[str, None] = None, company: Union[str, None] = None
    ):
        self.title = title
        self.company = company
