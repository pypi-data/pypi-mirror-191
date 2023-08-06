import functools
from pathlib import Path
from typing import Any, Dict, Optional

from iolanta.iolanta import Iolanta
from iolanta_jinja2.macros import template_render
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page


class IolantaPlugin(BasePlugin):
    """Integrate MkDocs + iolanta."""

    iolanta: Iolanta

    def on_files(
        self,
        files: Files,
        *,
        config: MkDocsConfig,
    ) -> Optional[Files]:
        """Construct the local iolanta instance and load files."""
        self.iolanta.add(source=Path(config.docs_dir))

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        config.extra['iolanta'] = self.iolanta = Iolanta()
        return config

    def on_page_context(
        self,
        context: Dict[str, Any],
        *,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ) -> Optional[Dict[str, Any]]:
        """Make render() macro available to pages."""
        return {
            'render': functools.partial(
                template_render,
                iolanta=self.iolanta,
            ),
            **context,
        }
