from cliriculum.renderers import Renderer
from cliriculum.markdown import ParseMd, LogoEntry
from cliriculum.deserializers import Dates, Contact
from cliriculum.loaders import load_json


def test_parse_md(fixtures_path):
    parsed = ParseMd(str(fixtures_path / "main.md"))
    dates_d = load_json(str(fixtures_path / "dates.json"))
    dates = Dates(dates_d)
    contact_d = load_json(str(fixtures_path / "contact.json"))
    contact = Contact(**contact_d)
    parsed.add_dates(dates=dates)
    parsed.add_contact(contact=contact)


def test_renderer(fixtures_path):
    """_summary_
    Test calling only.
    No result control
    Parameters
    ----------
    fixtures_path : _type_
        _description_
    """
    md_path = str(fixtures_path / "main.md")
    parsed = ParseMd(md_path)
    dates_d = load_json(str(fixtures_path / "dates.json"))
    dates = Dates(dates_d)
    doc = parsed.add_dates(dates=dates).doc
    with Renderer() as r:
        html = r.render(doc)
    contact_d = load_json(str(fixtures_path / "contact.json"))
    contact = Contact(**contact_d)
    doc = parsed.add_contact(contact=contact).doc
    with Renderer() as r:
        html = r.render(doc)
