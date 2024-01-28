import json

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from pathlib import Path

from example_app.etc import app_resource


def webpack_bundle(_, name: str):
    manifest_file = app_resource("static/bundles/manifest.json")
    webpack_bundles = json.load(open(manifest_file))
    return webpack_bundles[name]


def register_template_callables(engine: JinjaTemplateEngine) -> None:
    engine.register_template_callable(
        key="webpack_bundle",
        template_callable=webpack_bundle,
    )


template_config = TemplateConfig(
    directory=Path(__file__).parent / "templates",
    engine=JinjaTemplateEngine,
    engine_callback=register_template_callables,
)
