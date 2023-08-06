import argparse
import os
import sys
from pathlib import Path
from typing import Union
from cliriculum.resume import Resume
from cliriculum.utils import copy_resources, auto_filename, _check_dir
from cliriculum.pdf import chromium_print
from cliriculum.deserializers import Job
from cliriculum.loaders import load_json


def make_resume(
    directory,
    sidebar_md: str,
    main_md: str,
    dates: str,
    contact: str,
    overwrite: bool,
    stylesheet: Union[str, None],
    location: Union[str, None] = None,
    output: Union[str, None] = None,
    job_metadata: Union[str, None] = None,
    pdf_auto: bool = False,
):
    """
    Generates resume


    Parameters
    ----------
    ...:
        See :py:mod:`cliriculum.resume`
    directory: Directory to store the resume and all its file component (css, html, pdf, ...)
    overwrite: bool
        Whether to overwrite the `directory`
    output: Union[str, None]
        If provided a pdf is created in `directory + pdf`.
    pdf_auto:
        Precedence over output. Generates the pdf name automatically based on `job_metadata` if the latter is not None.
        Else defaults to output.pdf. By default False
    job_metadata: Union[str, None]
        JSON file location to job metadata, by default False.
    """
    _check_dir(directory=directory, overwrite=overwrite)
    resume = Resume(rsrc_dst=directory, stylesheet=stylesheet)
    html = resume(
        sidebar_md=sidebar_md,
        main_md=main_md,
        contact=contact,
        dates=dates,
        location=location,
    )

    with open(Path(directory) / "index.html", "w") as f:
        f.write(html)

    # copy dependencies
    print(f"Copying files to {directory}")
    copy_resources(directory)
    if output is not None and pdf_auto is False:
        chromium_print(directory=directory, filename=output)
    elif pdf_auto is True and job_metadata is not None:
        job_meta_dict = load_json(job_metadata)
        jobmeta = Job(**job_meta_dict)

        contact = resume.resume.sidebar._contact
        filename = auto_filename(
            name=contact.name,
            company=jobmeta.company,
            job_title=jobmeta.title,
            camel_case=False,
        )
        chromium_print(directory=directory, filename=filename)
    elif pdf_auto is True and job_metadata is None:
        raise ValueError("If `pdf_auto` is set to True job metadata must be set. ")


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a Resume using JSON and Markdown"
    )
    parser.add_argument(
        "--main",
        dest="main_md",
        type=str,
        action="store",
        required=True,
        help="Path to the markdown file",
    )
    parser.add_argument(
        "--description", dest="descr_md", type=str, action="store", required=True
    )
    parser.add_argument(
        "--dates",
        dest="dates_json",
        type=str,
        action="store",
        required=True,
        help="Path to the dates JSON file",
    )
    parser.add_argument(
        "--contact",
        dest="contact_json",
        type=str,
        action="store",
        required=True,
        help="Path to the contact JSON file",
    )

    parser.add_argument(
        "--destination",
        dest="destination",
        type=str,
        action="store",
        required=False,
        help="Directory where the HTML resume should be created",
        default="resume",
    )

    parser.add_argument(
        "--overwrite",
        type=int,
        action="store",
        required=False,
        help="Overwrite existing directory if set to other value than 0.",
        default=0,
    )
    parser.add_argument(
        "--stylesheet",
        dest="stylesheet",
        type=str,
        action="store",
        required=False,
        help="A supplementary stylesheet to add to the dom.",
        default=None,
    )
    parser.add_argument(
        "--location",
        dest="location",
        type=str,
        action="store",
        required=False,
        help="A file specifying locations to map to 2nd level headers by id",
        default=None,
    )
    parser.add_argument(
        "--pdf-output",
        dest="output",
        action="store",
        type=str,
        default=None,
        required=False,
        help="If filename the pdf will be generated and saved to '--directory + --pdf-output', if path like it will be saved to provided path",
    )
    parser.add_argument(
        "--pdf-auto",
        dest="pdf_auto",
        type=int,
        default=0,
        required=False,
        help="If not 0, the pdf will be named automatically based on job-metadata. If job-metadata is not provided it will default to 'output.pdf'. Precedence over pdf-output",
    )
    parser.add_argument(
        "--job-metadata",
        dest="job_metadata",
        action="store",
        type=str,
        default=None,
        required=False,
        help="Path to json file including metadata about job",
    )
    return parser


def main():
    parser = cli()
    args = parser.parse_args()
    overwrite = bool(args.overwrite)
    make_resume(
        directory=args.destination,
        sidebar_md=args.descr_md,
        contact=args.contact_json,
        dates=args.dates_json,
        main_md=args.main_md,
        overwrite=overwrite,
        stylesheet=args.stylesheet,
        location=args.location,
        output=args.output,
        job_metadata=args.job_metadata,
        pdf_auto=bool(args.job_metadata),
    )


if __name__ == "__main__":
    sys.exit(main())
