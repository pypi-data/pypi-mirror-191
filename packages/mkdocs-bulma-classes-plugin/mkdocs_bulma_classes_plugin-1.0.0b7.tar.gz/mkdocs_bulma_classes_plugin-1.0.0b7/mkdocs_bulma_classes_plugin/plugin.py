"""Plugin module for MkDocs. Use in tandem with mkdocs-bulma-theme."""

import re
from typing import List, Optional
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from mkdocs_bulma_classes_plugin.regexs.regex import (
    HeadingRegex,
    LinkRegex,
    Regex,
    TableRegex,
    TitleRegex,
    UnorderedListRegex,
    TagRegex,
)


class BulmaClassesPlugin(BasePlugin):
    """Discoverable class for MkDocs."""

    markdown_regexes: List[Regex] = [
        TitleRegex(),
        TagRegex(),
    ]

    regex_dict: List[Regex] = [
        TableRegex(),
        HeadingRegex(1),
        HeadingRegex(2),
        HeadingRegex(3),
        HeadingRegex(4),
        HeadingRegex(5),
        HeadingRegex(6),
        LinkRegex(),
        UnorderedListRegex(),
    ]

    config_scheme = {
        ("param", config_options.Type(str, default="")),
    }

    def __init__(self):
        """Create the plugin instance."""
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(
        self, markdown: str, page: Page, config, files
    ) -> Optional[str]:
        """Substitute any element that need Markdown to be mapped."""
        for obj in self.markdown_regexes:
            # TODO: This substitution not leave any chance to process any
            # markdown inside a captured content of the regex (.*), like the
            # issue with Titles and Subtitles. There's a possibility to make it
            # with the least possible complexity?
            markdown = obj.sub(markdown)

        return markdown

    def on_post_page(self, output: str, *, page: Page, config) -> Optional[str]:
        """Substitute any element that need HTML to be mapped."""
        # Substitute any element that need HTML to be mapped.
        # Here we take all other simple Markdown elements with easy mapping to Bulma classes
        for obj in self.regex_dict:
            if m := re.findall(obj.exp, output):
                utils.log.debug(f"Found {obj.exp} in {page.title}: {m}")

            output = obj.sub(output)

        return output
