"""
This module contains the Regex base class.

In last releases, in this module are spawned many regexes classes that extends
the base one. Each class has his own doc-test cases inside that run in
continuous integration.
"""

from re import Match, Pattern
import re
from typing import Callable


class Regex:
    """My regex class."""

    def __init__(
        self,
        pattern: str | Pattern[str],
        repl: str | Callable[[Match[str]], str],
        flags,
    ) -> None:
        """
        Initialize a new Regex for the plugin.

        :param pattern: str or Pattern of str
        :type pattern: str | Pattern[str]
        :param repl: str to substitute to matched groups
        :type repl: str
        :param flags: Flags to use for regex
        """
        self.exp = re.compile(pattern, flags=flags)
        self.repl = repl
        self.flags = flags

    def search(self, testString: str):
        """Wrap the regex search method."""
        return self.exp.search(testString)

    def sub(self, string: str):
        """Wrap the regex sub method."""
        return self.exp.sub(self.repl, string)


class TitleRegex(Regex):
    """
    Define the regex that produce Bulma Title and Subtitle.

    Look at for unit tests.
    """

    def __init__(
        self,
    ):
        """Instance the regex."""
        super().__init__(
            r"(.*)\n(=+)(\n+)(.*)\n(-+)",
            r'<h1 class="title is-1 has-text-light" id="\g<1>">\g<1></h1><h3 class="subtitle is-3 has-text-light" id="\g<4>">\g<4></h3>',
            re.MULTILINE,
        )


class HeadingRegex(Regex):
    """
    Define the regex that produce the Bulma First Level Title.

    The regex looks for an id (produced from mkdocs due to markdown
    conversion) and any class produced from this plugin in a previous event
    hook other than title or is-X.

    Look at https://regex101.com/r/bxQBvm/3 for unit tests.

    Headings set title class
    >>> HeadingRegex(1).search('<h1 id="title">Title</h1>') is not None
    True

    Headings with title class doesn't match
    >>> HeadingRegex(1).search('<h1 id="title" class="title">') is not None
    False

    Headings with other class than title will match
    >>> HeadingRegex(1).search('<h1 id="title" class="has-text-light">') is not None
    True

    In tests package you will find a property based testing through every
    supported heading size.
    """

    def __init__(self, level: int = 1):
        """Instance the regex."""
        pre_pattern = (
            r"<h{0} id=\"([\w-]*)\"( class=\"(?![(title)|(is\-{0})])([\w-]*)\")?>"
        )
        pre_repl = r'<h{0} id="\g<1>" class="title is-{0} has-text-light">'
        super().__init__(
            pre_pattern.format(level),
            pre_repl.format(level),
            re.MULTILINE | re.DOTALL,
        )


class UnorderedListRegex(Regex):
    r"""
    Define the regex that produce the Bulma Unordered List.

    Look at https://regex101.com/r/X0PSlS/3 for unit tests.

    Unordered List
    >>> UnorderedListRegex().search('<ul><li>Something</li></ul>') is None
    False

    Unordered List with content
    >>> UnorderedListRegex().search('<div class=\"content\"><ul><li>Something</li></ul></div>') is None
    False
    """

    def __init__(self) -> None:
        """Instance the regex."""
        super().__init__(
            r"\n?<ul>.*</ul>\n?",
            r'<div class="content">\g<0></div>',
            re.MULTILINE | re.DOTALL,
        )


class TableRegex(Regex):
    r"""
    Define the regex that produce the Bulma Table.

    Look at https://regex101.com/r/eHOik3/3 for unit tests.

    Match with a simple table tag
    >>> TableRegex().search('<table>') is None
    False

    Match with a table tag with id attr
    >>> TableRegex().search('<table id="table">') is None
    False

    Match with a table tag with class attr without table class inside
    >>> TableRegex().search('<table class="striped">') is None
    False

    Don't match with a table tag with class attr with table class inside
    >>> TableRegex().search('<table class="table">') is None
    True
    """

    def __init__(self) -> None:
        """Instance the regex."""
        super().__init__(
            r"<table(\sid=\"\w*\")?(\s?class=\"((?!table).*)\")?>",
            r'<table\g<1> class="table \g<3>">',
            re.MULTILINE | re.DOTALL,
        )


class LinkRegex(Regex):
    r"""
    Define the regex that produce the Bulma Link.

    Look at https://regex101.com/r/4jBnav/1 for unit tests.

    A simple link
    >>> LinkRegex().search('<a href=\"https://www.example.com\">Link</a>') is None
    False
    """

    def __init__(self) -> None:
        """Instance the regex."""
        super().__init__(
            r"<a href=\"(.*)\">",
            r'<a href="\g<1>" class="is-clickable has-text-link-light">',
            re.MULTILINE | re.DOTALL,
        )


class TagRegex(Regex):
    r"""
    Define the regex that produce the Bulma tag.

    A simple tag
    >>> TagRegex().search(':tag content: :other:') is None
    False
    """

    def __init__(self) -> None:
        """Instance the regex."""
        super().__init__(
            r":([\w\s]*):",
            r'<span class="tag">\g<1></span>',
            re.MULTILINE | re.DOTALL,
        )
