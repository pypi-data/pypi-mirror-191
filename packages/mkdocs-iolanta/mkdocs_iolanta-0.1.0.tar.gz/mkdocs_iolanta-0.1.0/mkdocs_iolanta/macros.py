import functools
import json
from functools import partial

from iolanta_jinja2.macros import template_render
from mkdocs_macros.plugin import MacrosPlugin

from mkdocs_iolanta.types import LOCAL


def define_env(env: MacrosPlugin) -> MacrosPlugin:  # noqa: WPS213
    """Create mkdocs-macros Jinja environment."""
    iolanta = env.variables.extra['iolanta']

    render = functools.partial(
        template_render,
        iolanta=iolanta,
    )

    env.macro(
        render,
        name='render',
    )

    return env
