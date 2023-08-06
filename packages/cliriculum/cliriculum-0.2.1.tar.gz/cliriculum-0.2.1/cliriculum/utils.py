from typing import Union, List, Iterable
from pathlib import PosixPath, Path
from shutil import copy2
from importlib import resources
import os


def _check_dir(directory, overwrite):
    if os.path.isdir(directory):
        os.makedirs(directory, exist_ok=overwrite)
    elif os.path.isfile(directory) is False:
        os.mkdir(directory)
    else:
        raise ValueError("The specified file is not a directory and exists")


def get_resources_nodes(
    root, tree, resrcs: List, skip_dirs: Iterable = {"__pycache__"}
) -> List[PosixPath]:
    """
    Get resources nodes recursively.

    Parameters
    ----------
    root: root Traversable
        Directory containing the module
        Generally obtained with:
        `root=resources.files(package_name).parent`
        package_name, being the package installed on your system
    tree : Traversable
        _description_
    resrcs:
        Resources should be empty list for first call.
        Expands on each recursive call.
    skip_dirs: Iterable
        Directories in which resources should not be fetched.
        Default = {'__pycache__'}

    Returns
    -------
    List[PosixPath]
        List of nodes which are resources

    Examples
    --------
    >>> a = resources.files("cliriculum.data")
    >>> get_resources_nodes(a.parent.parent, a)

    """
    package = ".".join(tree.relative_to(root).parts)  # init
    for node in tree.iterdir():
        if node.is_dir() and node.parts[-1] not in set(skip_dirs):
            get_resources_nodes(root=root, tree=node, resrcs=resrcs)
        else:
            if (
                resources.files(package).joinpath(node).is_file()
                and node.parts[-1] != "__init__.py"
            ):
                resrcs.append(node)
    return resrcs


def copy_resources(directory: str, resource_root: str = "cliriculum.data"):
    """
    Copy resources to specified directory

    Parameters
    ----------
    directory: str Where to store the directory.
        The directory should exist.
    resource_root: str
        The resource_root directory specified in module type
    notation, default "cliriculum.data"
    """
    if os.path.isdir(directory) is False and os.path.isfile(directory) is False:
        raise FileNotFoundError(
            f"Directory: '{directory}' does not exist, it should be created first."
        )
    elif os.path.isdir(directory) is False and os.path.isfile(directory) is True:
        raise FileExistsError("File exists: '{directory}'")
    pkgname = resource_root.split(".")[0]

    tree = resources.files(package=resource_root)  # requires python >=3.9
    root = resources.files(package=pkgname).parent
    rsrcs = get_resources_nodes(root=root, tree=tree, resrcs=[])

    for source in rsrcs:
        relative_to = source.relative_to(tree)
        target_dir = Path(directory)
        target = target_dir / str(relative_to)

        # if source.relative_to is not root
        # and directory does not exist
        # create directory
        if target.parent.exists() is False and target.parent != target_dir:
            os.makedirs(target.parent)
        copy2(src=source, dst=target)
        # assert False == True


def copy_files(srcs: Iterable[Union[str, Path]], dst: Union[Path, str]) -> None:
    """
    Copy files to destination keeping path basename.

    Parameters
    ----------
    srcs : Iterable[Union[str, Path]]
        _description_
    dst : Union[Path, str]
        _description_
    """
    # effectivement peut etre très dangereux.
    # Doit etre corriger.
    if isinstance(srcs, str):
        raise TypeError("srcs should be an Iterable but not a string")
    for src in srcs:
        file_dst = Path(dst) / os.path.basename(src)
        copy2(src, file_dst)


def _case(string, camel_case: bool) -> str:
    if camel_case is True:
        string = string.capitalize()
    else:
        string = string.lower()
    return string


def _replace_space(string, camel_case):
    return "_".join(_case(token, camel_case=camel_case) for token in string.split(" "))


def auto_filename(name: str, job_title: str, company: str, camel_case: bool) -> str:
    """
    Create filename string under the form:

    `<name>-resume-<job title>-<company>.pdf` if camel_case is False.
    Or `<Name>-Resume-<Job title>-<Company>.pdf` if camel_case is True.

    Note that spaces contained in name will be replace by "_"

    Example
    -------
    No space in name:

    >>> from cliriculum.utils import auto_filename
    >>> auto_filename(name="Cliriculum", job_title="Resume Maker", "company"="No Company")
        'cliriculum-resume_maker-company'


    Space in name:

    >>> auto_filename(name="Cliriculum Tool", job_title="Resume Maker", "company"="No Company")
        'cliriculum_tool-resume_maker-company'

    Camel case in name:

    >>> auto_filename(name="Cliriculum Tool", job_title="Resume Maker", "company"="No Company", camel_case=True)
        'Cliriculum_Tool-Resume-Maker-Company'

    """

    return (
        _replace_space(name, camel_case=camel_case)
        + "-"
        + _case("resume", camel_case=camel_case)
        + "-"
        + _replace_space(job_title, camel_case=camel_case)
        + "-"
        + _replace_space(company, camel_case=camel_case)
        + ".pdf"
    )
