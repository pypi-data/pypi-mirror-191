from cliriculum.utils import copy_resources, copy_files
from cliriculum.main import make_resume
from cliriculum.deserializers import Contact
from cliriculum.loaders import load_json
from pathlib import Path
import os
import pytest

BASE_DIR = Path(__file__).parent.parent


def _isnot_pycache_or_init(path: Path):
    if "__pycache__" in path.parts or "__init__.py" in path.parts:
        return False
    else:
        return True


def test_copy_resources(tmp_path):
    copy_resources(directory=tmp_path)
    lev1 = tmp_path.glob("*")
    lev2 = tmp_path.glob("*/*")
    lev3 = tmp_path.glob("*/*/*")
    expected_path = BASE_DIR / "cliriculum/data"

    rsrcs1 = list(filter(_isnot_pycache_or_init, expected_path.glob("*")))
    rsrcs2 = list(filter(_isnot_pycache_or_init, expected_path.glob("*/*")))
    rsrcs3 = list(filter(_isnot_pycache_or_init, expected_path.glob("*/*/*")))

    t1 = set([path.name for path in lev1]).symmetric_difference(
        [path.name for path in rsrcs1]
    )
    t2 = set([path.name for path in lev2]).symmetric_difference(
        [path.name for path in rsrcs2]
    )
    t3 = set([path.name for path in lev3]).symmetric_difference(
        [path.name for path in rsrcs3]
    )

    assert t1 == set()
    assert t2 == set()
    assert t3 == set()


def test_copy_files(tmp_path, fixtures_path):
    c = str(fixtures_path / "contact.json")
    contact = Contact(**load_json(c))
    copy_files(srcs=[contact.profile.logo], dst=tmp_path)
    img = "image.png"
    t1 = set(os.listdir(tmp_path)).symmetric_difference([img])
    assert t1 == set()


def test_make_resume(tmp_path, fixtures_path):
    s = str(fixtures_path / "sidebar.md")
    m = str(fixtures_path / "main.md")
    d = str(fixtures_path / "dates.json")
    c = str(fixtures_path / "contact.json")
    j = str(fixtures_path / "job.json")
    with pytest.raises(FileExistsError):
        make_resume(
            tmp_path,
            sidebar_md=s,
            main_md=m,
            dates=d,
            contact=c,
            overwrite=False,
            stylesheet=None,
        )

    make_resume(
        tmp_path,
        sidebar_md=s,
        main_md=m,
        dates=d,
        contact=c,
        overwrite=True,
        stylesheet=None,
    )
    assert "index.html" in os.listdir(str(tmp_path))

    make_resume(
        tmp_path,
        sidebar_md=s,
        main_md=m,
        dates=d,
        contact=c,
        overwrite=True,
        stylesheet=None,
        job_metadata=j,
        pdf_auto=True,
    )
