from cliriculum.resume import resume, SideBarHTML, MainHTML, ResumeHTML, Resume
import pytest
import os
import warnings


ARGS = ["location_path", "location_none"]


class TestResume:
    @pytest.mark.parametrize("location", ARGS)
    def test___init__and__call__(self, location, tmp_path, fixtures_path, request):
        s = str(fixtures_path / "sidebar.md")
        m = str(fixtures_path / "main.md")
        d = str(fixtures_path / "dates.json")
        c = str(fixtures_path / "contact.json")
        add_css = str(fixtures_path / "custom.css")
        resume = Resume(rsrc_dst=None, stylesheet=None)
        html = resume(
            sidebar_md=s,
            main_md=m,
            dates=d,
            contact=c,
            location=request.getfixturevalue(location),
        )
        assert len(html) > 0


def test_sidebar_html(fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    c = str(fixtures_path / "contact.json")

    sidebar = SideBarHTML(path=s, contact=c)


@pytest.mark.parametrize("location", ARGS)
def test_main_html(location, fixtures_path, request):
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    main = MainHTML(m, dates=d, location=request.getfixturevalue(location))


# This test tests deprecated function (depr from 0.1.6)
# -----------------------------------
@pytest.mark.parametrize("location", ARGS)
def test_resume(location, tmp_path, fixtures_path, request):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    add_css = str(fixtures_path / "custom.css")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        html = resume(sidebar_md=s, main_md=m, dates=d, contact=c)
    with pytest.deprecated_call():
        resume(sidebar_md=s, main_md=m, dates=d, contact=c)


@pytest.mark.parametrize("location", ARGS)
def test_resume_html(location, tmp_path, fixtures_path, request):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    sidebar = SideBarHTML(path=s, contact=c, rsrc_dst=tmp_path)
    main = MainHTML(path=m, dates=d, location=request.getfixturevalue(location))
    resume = ResumeHTML(
        main=main,
        sidebar=sidebar,
        stylesheet=fixtures_path / "custom.css",
        rsrc_dst=tmp_path,
    )
    assert resume.additionalcss != ""

    files = os.listdir(tmp_path)
    assert set(files).symmetric_difference(["custom.css", "image.png"]) == set()

    with pytest.raises(ValueError):
        ResumeHTML(
            main=main,
            sidebar=sidebar,
            stylesheet=fixtures_path / "custom.css",
            rsrc_dst=None,
        )
