from __future__ import annotations
from typing import Callable


def n_backticks_to_wrap_codespan(character: str, text: str) -> int:
    in_a_rows, current_in_a_row = ([], 0)
    for ch in text:
        if ch == character:
            current_in_a_row += 1
        elif current_in_a_row > 0:
            if current_in_a_row not in in_a_rows:
                in_a_rows.append(current_in_a_row)
            current_in_a_row = 0
    if current_in_a_row > 0 and current_in_a_row not in in_a_rows:
        in_a_rows.append(current_in_a_row)

    result = 0
    if in_a_rows:
        for n in range(1, max(in_a_rows) + 2):
            if n not in in_a_rows:
                result = n
                break
    return result


def parse_link_references(content: str) -> list[tuple[str, str, str]]:
    import re

    link_reference_re = re.compile(
        r'^\[([^\]]+)\]:\s+<?([^\s>]+)>?\s*["\'\(]?([^"\'\)]+)?'
    )

    response = []
    for line in content.splitlines():
        if line[0] == "[":
            match = re.search(link_reference_re, line)
            if match:
                response.append(list(match.groups()))
    return response


def transform_line_by_line_skipping_codeblocks(
    markdown: str,
    func: Callable[[str], str],
) -> str:
    """Apply a transformation line by line in a Markdown text using a function.
    Skip fenced codeblock lines, where the transformation never is applied.
    Indented codeblocks are not taken into account because in the practice
    this function is never used for transformations on indented lines. See
    the PR https://github.com/mondeja/mkdocs-include-markdown-plugin/pull/95
    to recover the implementation handling indented codeblocks.
    """
    import io

    # current fenced codeblock delimiter
    _current_fcodeblock_delimiter = ""

    lines = []
    for line in io.StringIO(markdown):
        if not _current_fcodeblock_delimiter:
            lstripped_line = line.lstrip()
            if lstripped_line.startswith("```") or lstripped_line.startswith("~~~"):
                _current_fcodeblock_delimiter = lstripped_line[:3]
            elif not line.startswith("    ") or line.startswith("     "):
                line = func(line)
        elif line.lstrip().startswith(_current_fcodeblock_delimiter):
            _current_fcodeblock_delimiter = ""
        lines.append(line)

    return "".join(lines).rstrip()


def transform_negative_offset_func_factory(
    offset: int,
) -> Callable[[str], str]:
    def func(line: str) -> str:
        if not line.startswith("#"):
            return line
        curr_offset = 0
        new_line = ""
        for c in line:
            if c != "#":
                break
            curr_offset += 1
        if curr_offset > offset:
            new_line = "#" * (curr_offset - offset)
        else:
            new_line = "#"
        new_line += line.lstrip("#")
        return new_line

    return func


def transform_positive_offset_func_factory(
    offset: int,
) -> Callable[[str], str]:
    heading_prefix = "#" * offset
    return lambda line: (heading_prefix + line if line.startswith("#") else line)


def modify_headings_offset(markdown: str, offset: int) -> str:
    return transform_line_by_line_skipping_codeblocks(
        markdown,
        transform_positive_offset_func_factory(offset)
        if offset > 0
        else transform_negative_offset_func_factory(abs(offset)),
    )
