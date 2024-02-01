import json

import structlog

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from pathlib import Path

log: structlog.BoundLogger = structlog.get_logger()


def make_callback(static_dir: str):
    def webpack_bundle(_, name: str):
        manifest_file = Path(static_dir) / "js/manifest.json"
        webpack_bundles = json.load(open(manifest_file))
        return webpack_bundles[name]

    def callback(engine: JinjaTemplateEngine) -> None:
        engine.register_template_callable(
            key="webpack_bundle",
            template_callable=webpack_bundle,
        )

    return callback


def create_template_config(template_dir: str, static_dir: str):
    return TemplateConfig(
        directory=template_dir,
        engine=JinjaTemplateEngine,
        engine_callback=make_callback(static_dir),
    )
