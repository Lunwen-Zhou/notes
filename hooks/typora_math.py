"""Make Typora-style display math compatible with Python Markdown.

Typora accepts a ``$$`` block immediately after or before prose, while
Python Markdown requires a blank line around the block. This hook adds those
blank lines in memory before pymdownx.arithmatex runs. Source files are left
unchanged.
"""

from __future__ import annotations

import re


_MATH_DELIMITER = re.compile(r"^(?P<prefix>\s*(?:>\s*)*)\$\$\s*$")
_FENCE = re.compile(r"^(?P<marker>`{3,}|~{3,})")
_CONTAINER_PREFIX = re.compile(r"^\s*(?:>\s*)*")
_BLANK_OR_QUOTE_SEPARATOR = re.compile(r"^\s*(?:>\s*)*$")


def _content_without_container_prefix(line: str) -> str:
    """Return content after indentation and blockquote markers."""

    return line[_CONTAINER_PREFIX.match(line).end() :]


def _separator_for(prefix: str) -> str:
    """Keep an inserted blank line inside a blockquote when needed."""

    return prefix.rstrip()


def _is_separator(line: str) -> bool:
    return _BLANK_OR_QUOTE_SEPARATOR.fullmatch(line) is not None


def _dedent_math_line(line: str, width: int) -> str:
    """Dedent Typora's two-space list continuation for block parsing."""

    indentation = len(line) - len(line.lstrip(" "))
    return line[min(indentation, width) :]


def normalize_typora_math(markdown: str) -> str:
    """Add missing blank lines around standalone ``$$`` math blocks."""

    lines = markdown.splitlines()
    normalized: list[str] = []
    in_math = False
    math_dedent = 0
    fence_character: str | None = None
    fence_length = 0

    for index, line in enumerate(lines):
        content = _content_without_container_prefix(line)
        fence_match = _FENCE.match(content)

        if fence_match:
            marker = fence_match.group("marker")
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0

            normalized.append(line)
            continue

        delimiter_match = None if fence_character else _MATH_DELIMITER.fullmatch(line)
        if delimiter_match is None:
            normalized.append(_dedent_math_line(line, math_dedent) if in_math else line)
            continue

        prefix = delimiter_match.group("prefix")
        if not in_math and ">" not in prefix and 0 < len(prefix) < 4:
            # Typora indents list continuations by two spaces. Python Markdown
            # requires four, so render the equation as a top-level block.
            math_dedent = len(prefix)

        rendered_line = _dedent_math_line(line, math_dedent)
        rendered_prefix = _dedent_math_line(prefix, math_dedent)
        separator = _separator_for(rendered_prefix)

        if not in_math and normalized and not _is_separator(normalized[-1]):
            normalized.append(separator)

        normalized.append(rendered_line)
        in_math = not in_math

        if not in_math and index + 1 < len(lines) and not _is_separator(lines[index + 1]):
            normalized.append(separator)
        if not in_math:
            math_dedent = 0

    result = "\n".join(normalized)
    if markdown.endswith("\n"):
        result += "\n"
    return result


def on_page_markdown(markdown: str, **kwargs) -> str:
    """MkDocs hook entry point."""

    return normalize_typora_math(markdown)
