# -*- coding: utf-8 -*-
from typing import Literal, Union

from kiara.models.module.pipeline import PipelineConfig, PipelineStructure
from kiara.models.module.pipeline.pipeline import Pipeline


def graph_widget(
    pipeline: Union[PipelineStructure, PipelineConfig, Pipeline],
    graph_type: Literal["data-flow", "data-flow-simple", "execution"] = "execution",
):

    if hasattr(pipeline, "structure"):
        pipeline = pipeline.structure  # type: ignore

    try:
        import ipydagred3 as ipydagred3
    except Exception:
        raise Exception(
            "ipydagred3 not available, please install it manually into the current virtualenv"
        )

    g = ipydagred3.Graph()
    if graph_type == "execution":
        graph = pipeline.execution_graph  # type: ignore
    elif graph_type == "data-flow":
        graph = pipeline.data_flow_graph  # type: ignore
    elif graph_type == "data-flow-simple":
        graph = pipeline.data_flow_graph_simple  # type: ignore
    else:
        raise Exception(f"Invalid graph type requested: '{graph_type}'")

    nodes_set = set()
    for node in graph.nodes:
        nodes_set.add(str(node))
        g.setNode(str(node))

    for edge in graph.edges:
        e = str(edge[0])
        if e not in nodes_set:
            print("MISSING")
            print(e)
        e2 = str(edge[1])
        if e2 not in nodes_set:
            print("MISSING 2")
            print(e2)
        g.setEdge(e, e2)

    widget = ipydagred3.DagreD3Widget(graph=g)
    return widget
