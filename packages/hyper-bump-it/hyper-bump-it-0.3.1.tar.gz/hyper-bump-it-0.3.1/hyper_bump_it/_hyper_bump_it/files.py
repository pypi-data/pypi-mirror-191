"""
Operation on files.
"""
from dataclasses import InitVar, dataclass, field
from pathlib import Path

from .config import File
from .error import FileGlobError, VersionNotFound
from .text_formatter import TextFormatter
from .text_formatter.text_formatter import FormatContext


@dataclass
class LineChange:
    line_index: int
    old_line: str
    new_line: str


@dataclass
class PlannedChange:
    file: Path  # absolute resolved path
    project_root: InitVar[Path]  # absolute resolved path
    relative_file: Path = field(init=False)
    line_changes: list[LineChange]

    def __post_init__(self, project_root: Path) -> None:
        self.relative_file = self.file.relative_to(project_root)


def collect_planned_changes(
    project_root: Path, config: File, formatter: TextFormatter
) -> list[PlannedChange]:
    """
    Aggregate a collection of changes that would occur across multiple files.

    :param project_root: Root directory to start looking for files.
    :param config: Configuration of how the changes should operate.
    :param formatter: Object that converts format patterns into text.
    :return: Descriptions of the change that would occur.
    :raises FileGlobError: Glob pattern for selecting files did not find any files.
    :raises VersionNotFound: A file did not contain the produced search text.
    """
    changes = [
        _planned_change_for(
            file,
            config.search_format_pattern,
            config.replace_format_pattern,
            formatter,
            project_root,
        )
        for file in project_root.glob(config.file_glob)
    ]
    if not changes:
        raise FileGlobError(project_root, config.file_glob)
    return changes


def _planned_change_for(
    file: Path,
    search_pattern: str,
    replace_pattern: str,
    formatter: TextFormatter,
    project_root: Path,
) -> PlannedChange:
    search_text = formatter.format(search_pattern, FormatContext.search)
    changes: list[LineChange] = []
    for i, line in enumerate(file.read_text().splitlines()):
        if search_text in line:
            replace_text = formatter.format(replace_pattern, FormatContext.replace)
            changes.append(
                LineChange(
                    line_index=i,
                    old_line=line,
                    new_line=line.replace(search_text, replace_text),
                )
            )

    if changes:
        return PlannedChange(file, project_root, changes)

    raise VersionNotFound(file.relative_to(project_root), search_pattern)


def perform_change(change: PlannedChange) -> None:
    try:
        contents = change.file.read_bytes()
    except FileNotFoundError:
        raise ValueError(
            f"Given file '{change.file}' does not exist. PlannedChange is not valid."
        )
    lines = contents.splitlines(keepends=True)
    for line_change in change.line_changes:
        try:
            old_line = lines[line_change.line_index]
        except IndexError:
            raise ValueError(
                f"Given file '{change.file}' does not contain a line with the index of"
                f" {line_change.line_index}. PlannedChange is not valid."
            )
        lines[line_change.line_index] = line_change.new_line.encode() + _line_ending(
            old_line
        )
    change.file.write_bytes(b"".join(lines))


def _line_ending(line: bytes) -> bytes:
    # match line ending of file instead of assuming os.linesep
    if line.endswith(b"\r\n"):
        return b"\r\n"
    if line.endswith(b"\n"):
        return b"\n"
    # no trailing new line
    return b""
