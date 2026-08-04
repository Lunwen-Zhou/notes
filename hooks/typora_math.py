"""Make Typora-style Markdown compatible with Python Markdown.

Typora accepts a ``$$`` block immediately after or before prose, while
Python Markdown requires a blank line around the block. This hook adds those
blank lines in memory before pymdownx.arithmatex runs. Typora also accepts two
spaces per nested-list level, while Python Markdown requires four. The hook
expands only list-related indentation during the build. Source files are left
unchanged.
"""

from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import subprocess


_MATH_DELIMITER = re.compile(r"^(?P<prefix>\s*(?:>\s*)*)\$\$\s*$")
_FENCE = re.compile(r"^(?P<marker>`{3,}|~{3,})")
_CONTAINER_PREFIX = re.compile(r"^\s*(?:>\s*)*")
_BLANK_OR_QUOTE_SEPARATOR = re.compile(r"^\s*(?:>\s*)*$")
_LEVEL_ONE_HEADING = re.compile(r"^#(?:[ \t]+|$)")
_LIST_ITEM = re.compile(r"^(?P<indent> *)(?:[-+*]|\d+[.)])[ \t]+")
_LEADING_SPACES = re.compile(r"^ *")
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_MODIFIED_TIMES_PATH = _PROJECT_ROOT / ".note-modified-times.json"
_LOCAL_HTML_IMAGE = re.compile(
    r'(?P<prefix><img\b[^>]*?\bsrc\s*=\s*["\'])(?P<src>[^"\']+)(?P<suffix>["\'])',
    re.IGNORECASE,
)


@lru_cache(maxsize=1)
def _stored_modified_times() -> dict[str, dict[str, str]]:
    """Read portable file times captured from the author's filesystem."""

    try:
        data = json.loads(_MODIFIED_TIMES_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return data.get("files", {})


def _git_modified_time(relative_path: str) -> datetime | None:
    """Return the last commit time for a clean file, when available."""

    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--", relative_path],
            cwd=_PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        if status.stdout:
            return None
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", relative_path],
            cwd=_PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    timestamp = result.stdout.strip()
    return datetime.fromisoformat(timestamp) if timestamp else None


def get_modified_time(source_path: str) -> datetime:
    """Resolve a Markdown file's real modification time automatically.

    A content hash lets CI reuse the file time captured on the author's
    computer instead of the checkout time. For new clean content, Git's last
    commit time is the portable fallback; uncommitted local edits use mtime.
    """

    path = Path(source_path).resolve()
    filesystem_time = datetime.fromtimestamp(path.stat().st_mtime).astimezone()

    try:
        relative_path = path.relative_to(_PROJECT_ROOT).as_posix()
    except ValueError:
        return filesystem_time

    stored = _stored_modified_times().get(relative_path)
    content_hash = sha256(path.read_bytes()).hexdigest()
    if stored and stored.get("content_sha256") == content_hash:
        try:
            return datetime.fromisoformat(stored["modified_at"])
        except (KeyError, ValueError):
            pass

    return _git_modified_time(relative_path) or filesystem_time


def normalize_typora_lists(markdown: str) -> str:
    """Expand Typora's two-space list indentation for Python Markdown.

    The transformation is limited to indented lines belonging to a list. A
    fenced code block inside a list receives only the container's additional
    indentation, so indentation inside the code itself is preserved.
    """

    lines = markdown.splitlines()
    normalized: list[str] = []
    in_list = False
    fence_character: str | None = None
    fence_length = 0
    fence_indent = 0
    fence_delta = 0

    for line in lines:
        leading_spaces = len(_LEADING_SPACES.match(line).group())
        content = line[leading_spaces:]

        if fence_character is not None:
            adjusted_line = f"{' ' * fence_delta}{line}" if line else line
            normalized.append(adjusted_line)
            fence_match = _FENCE.match(content)
            if (
                fence_match
                and fence_match.group("marker")[0] == fence_character
                and len(fence_match.group("marker")) >= fence_length
                and leading_spaces == fence_indent
            ):
                fence_character = None
                fence_length = 0
                fence_indent = 0
                fence_delta = 0
            continue

        list_match = _LIST_ITEM.match(line)
        if leading_spaces == 0 and line.strip() and list_match is None:
            in_list = False

        if list_match is not None:
            in_list = True

        if in_list and leading_spaces >= 2:
            # Typora uses two spaces for each list level. Doubling the
            # structural indentation gives Python Markdown its required four.
            adjusted_indent = leading_spaces * 2
            adjusted_line = f"{' ' * adjusted_indent}{content}"
        else:
            adjusted_indent = leading_spaces
            adjusted_line = line

        fence_match = _FENCE.match(content)
        if in_list and fence_match:
            marker = fence_match.group("marker")
            fence_character = marker[0]
            fence_length = len(marker)
            fence_indent = leading_spaces
            fence_delta = adjusted_indent - leading_spaces

        normalized.append(adjusted_line)

    result = "\n".join(normalized)
    if markdown.endswith("\n"):
        result += "\n"
    return result


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
    math_quote_prefix: str | None = None
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
            if in_math and math_quote_prefix is not None:
                content = _content_without_container_prefix(line)
                # A blank quoted line splits a display-math paragraph in
                # Python Markdown. Typora ignores it, so omit it here too.
                if content.strip():
                    normalized.append(f"{math_quote_prefix}{content}")
            else:
                normalized.append(_dedent_math_line(line, math_dedent) if in_math else line)
            continue

        prefix = delimiter_match.group("prefix")
        if not in_math and ">" in prefix:
            # Typora permits display math indented beneath a list inside a
            # blockquote (for example ``>   $$``). Flatten only the math block
            # back to its quote level so pymdownx.arithmatex can recognize it.
            math_quote_prefix = "> " * prefix.count(">")
        if not in_math and ">" not in prefix and 0 < len(prefix) < 4:
            # Typora indents list continuations by two spaces. Python Markdown
            # requires four, so render the equation as a top-level block.
            math_dedent = len(prefix)
        elif (
            not in_math
            and ">" not in prefix
            and len(prefix) >= 4
            and len(prefix) % 4 == 2
        ):
            # ``normalize_typora_lists`` doubles a three-space continuation to
            # six spaces. Display math needs four spaces at that list level;
            # remove only the two-space excess and keep it inside the item.
            math_dedent = 2

        if math_quote_prefix is not None:
            rendered_line = f"{math_quote_prefix}$$"
            rendered_prefix = math_quote_prefix
        else:
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
            math_quote_prefix = None

    result = "\n".join(normalized)
    if markdown.endswith("\n"):
        result += "\n"
    return result


def add_modified_time(markdown: str, source_path: str) -> str:
    """Render the source file's modification time below its first H1."""

    modified_at = get_modified_time(source_path)
    display_time = modified_at.strftime("%Y年%m月%d日 %H:%M")
    timestamp = modified_at.astimezone().isoformat(timespec="minutes")
    modified_markup = (
        '<p class="document-modified-time">'
        '更新时间：<time datetime="'
        f'{escape(timestamp, quote=True)}">{escape(display_time)}</time></p>'
    )

    lines = markdown.splitlines()
    fence_character: str | None = None
    fence_length = 0

    for index, line in enumerate(lines):
        fence_match = _FENCE.match(line)
        if fence_match:
            marker = fence_match.group("marker")
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            continue

        if fence_character is None and _LEVEL_ONE_HEADING.match(line):
            lines[index + 1:index + 1] = ["", modified_markup]
            result = "\n".join(lines)
            if markdown.endswith("\n"):
                result += "\n"
            return result

    return markdown


def on_page_markdown(markdown: str, page, **kwargs) -> str:
    """MkDocs hook entry point."""

    source_path = Path(page.file.abs_src_path)
    if source_path.name.lower() != "index.md":
        markdown = add_modified_time(markdown, str(source_path))
    markdown = normalize_typora_lists(markdown)
    return normalize_typora_math(markdown)


def on_page_content(html: str, page, config, **kwargs) -> str:
    """Keep same-folder Typora image paths working with directory URLs.

    A regular MkDocs page is emitted as ``page/index.html``, one directory
    deeper than its Markdown source. MkDocs adjusts Markdown image syntax but
    leaves raw ``<img>`` tags unchanged, so add that one directory traversal
    to local raw-HTML image sources at build time only.
    """

    is_index = Path(page.file.abs_src_path).name.lower() == "index.md"
    if not config.get("use_directory_urls", True) or is_index:
        return html

    def rewrite(match: re.Match[str]) -> str:
        src = match.group("src")
        if (
            src.startswith(("/", "../", "#", "//"))
            or re.match(r"^[a-z][a-z0-9+.-]*:", src, re.IGNORECASE)
        ):
            return match.group(0)
        return f'{match.group("prefix")}../{src}{match.group("suffix")}'

    return _LOCAL_HTML_IMAGE.sub(rewrite, html)
