# -*- coding: utf-8 -*-

"""Python module that contains the entrypoints for kiara_plugin.jupyter.

This plugin package is different, because we don't want to import kiara in our top-level package module, since we might want to do some plugin-installation before anything else.
"""

from kiara.utils.class_loading import (
    KiaraEntryPointItem,
    find_data_types_under,
    find_kiara_model_classes_under,
    find_kiara_modules_under,
    find_kiara_renderers_under,
    find_pipeline_base_path_for_module,
)

from kiara_plugin.jupyter import KIARA_METADATA

find_modules: KiaraEntryPointItem = (
    find_kiara_modules_under,
    "kiara_plugin.jupyter.modules",
)
find_model_classes: KiaraEntryPointItem = (
    find_kiara_model_classes_under,
    "kiara_plugin.jupyter.models",
)
find_data_types: KiaraEntryPointItem = (
    find_data_types_under,
    "kiara_plugin.jupyter.data_types",
)
find_pipelines: KiaraEntryPointItem = (
    find_pipeline_base_path_for_module,
    "kiara_plugin.jupyter.pipelines",
    KIARA_METADATA,
)
find_renderer_classes: KiaraEntryPointItem = (
    find_kiara_renderers_under,
    "kiara_plugin.jupyter.renderers",
)
