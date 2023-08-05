from cliriculum.markdown import ParseMd
from cliriculum.renderers import SideBarRenderer, MainRenderer
from cliriculum.deserializers import Contact, Dates, Locations
from cliriculum.markdown import DescriptionBlock
from cliriculum.loaders import load_json
from warnings import warn
from typing import Union
from cliriculum.utils import copy_files
from os.path import basename


HEAD = """
<!doctype html>
<head>
  <meta charset="UTF-8">
  <title>HTML Resume</title>
  <link rel="stylesheet" href="style.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/all.css" type="text/css">
  <link rel="stylesheet" href="fontawesome/css/v4-shims.css" type="text/css">
  {additionalcss}
  <script src="paged.polyfill.js"></script>
  <script src="style.js"></script>
</head>
"""


class SideBarHTML:
    def __init__(self, path, contact, rsrc_dst: Union[str, None] = None):
        """_summary_

        Parameters
        ----------
        path : _type_
            _description_
        contact : _type_
            _description_
        rsrc_dst : Union[str, None], optional
            If not None resources mentionned in JSON files are copied to destination directory `rsrc_dst`. By default, None.
        """
        parsed = ParseMd(path)
        contact_d = load_json(contact)
        contact_o = Contact(**contact_d)
        parsed.add_contact(contact_o)
        doc = parsed.doc
        # find ...
        if parsed.top is True:
            contact = doc.children[0]
            description = doc.children[1:]
        else:
            contact = doc.children[-1]
            description = doc.children[:-1]
        # all except this element
        # either at beginning either at the end
        children = [contact, DescriptionBlock(children=description)]
        doc.children = children
        with SideBarRenderer() as r:
            self.html = r.render(doc)
        if rsrc_dst is not None and contact_o.profile.logo is not None:
            warn("Currently, specifying rsrc_dst copies only contact profile picture")
            copy_files([contact_o.profile.logo], rsrc_dst)
        self._contact = contact_o


class MainHTML:
    def __init__(
        self, path, dates: Union[str, None] = None, location: Union[str, None] = None
    ):
        self.parsed = ParseMd(path)
        if dates is not None:
            dates_d = load_json(dates)
            dates_o = Dates(dates_d)
            self.parsed.add_dates(dates_o)

        if location is not None:
            location_d = load_json(location)
            location_o = Locations(location_d)
            self.parsed.add_location(location_o)

        with MainRenderer() as r:
            self.html = r.render(self.parsed.doc)


class ResumeHTML:
    """
    Render Resume

    Attributes
    ----------
    main: MainHTML
    sidebar: SideBarHTML
    """

    def __init__(
        self,
        sidebar: SideBarHTML,
        main: MainHTML,
        stylesheet: Union[str, None],
        rsrc_dst=Union[str, None],
    ):
        """

        Parameters
        ----------
        sidebar : SideBarHTML
        main : MainHTML
        stylesheet: Path to stylesheet.
        rsrc_dst: See :class:SidebarHTML

        Returns
        -------
        _type_
            _description_
        """
        self.main = main
        self.sidebar = sidebar
        if stylesheet is not None and rsrc_dst is None:
            raise ValueError("stylesheet can not be used when rsrc_dst is set to None")
        if stylesheet is not None:
            copy_files(srcs=[stylesheet], dst=rsrc_dst)
            _ = f'<link rel="stylesheet" href="{basename(stylesheet)}" type="text/css">'
        else:
            _ = ""
        self.additionalcss = _

    def join(self) -> str:
        body = self.sidebar.html + "\n" + self.main.html  # union of sidebar and main
        template = "<html>{head}<body>{body}</body></html>"
        return template.format(
            head=HEAD.format(additionalcss=self.additionalcss), body=body
        )


def resume(
    sidebar_md: str,
    main_md: str,
    dates: str,
    contact: str,
    rsrc_dst: Union[str, None] = None,
    stylesheet: Union[str, None] = None,
    location: Union[str, None] = None,
) -> str:
    """

    Parameters
    ----------
    sidebar_md : str
        Path to sidebar markdown
    main_md : str
        Path to main markdown
    dates : str
        path to dates JSON
    contact : str
        Path to contact JSON
    rsrc_dst: Union[str, None]
        Argument passed to :class:SidebarHTML and :class:ResumeHTML
    stylesheet: Argument passed to :class:ResumeHTML
    location: Union[str, None]
        Path to JSON file containing location metadata

    Returns
    -------
    str
        HTML representation of the resume

    Examples
    --------
    >>> from cliriculum import resume
    >>> html = resume(sidebar_md="sidebar.md", main_md="main.md", contact="contact.json", dates="dates.json")
    """
    warn(
        "Deprecated in 0.1.6, Resume class should be used instead.", DeprecationWarning
    )
    sidebar = SideBarHTML(path=sidebar_md, contact=contact, rsrc_dst=rsrc_dst)
    main = MainHTML(path=main_md, dates=dates, location=location)
    resume = ResumeHTML(
        main=main, sidebar=sidebar, stylesheet=stylesheet, rsrc_dst=rsrc_dst
    )
    html = resume.join()
    return html


class Resume:
    """

    Attributes
    ----------
    stylesheet: str
    rsrc_dst: str
    resume: Union[ResumeHTML, None]
        Is set on __call__ (to ResumeHTML instance)

    Example
    -------
    >>> from cliriculum.resume import Resume
    >>> resume = Resume()  # a callable
    >>> resume(sidebar_md="sidebar.md", main_md="main.md", contact="contact.json", dates="dates.json")
    """

    def __init__(
        self,
        rsrc_dst: Union[str, None] = None,
        stylesheet: Union[str, None] = None,
    ):
        self.rsrc_dst = rsrc_dst
        self.stylesheet = stylesheet
        self.resume = None

    def __call__(
        self,
        sidebar_md: str,
        main_md: str,
        contact: str,
        dates: Union[str, None] = None,
        location: Union[str, None] = None,
    ) -> str:
        sidebar = SideBarHTML(path=sidebar_md, contact=contact, rsrc_dst=self.rsrc_dst)
        main = MainHTML(path=main_md, dates=dates, location=location)
        resume = ResumeHTML(
            main=main,
            sidebar=sidebar,
            stylesheet=self.stylesheet,
            rsrc_dst=self.rsrc_dst,
        )
        self.resume = resume  # wich means a text is generated
        html = resume.join()
        return html
