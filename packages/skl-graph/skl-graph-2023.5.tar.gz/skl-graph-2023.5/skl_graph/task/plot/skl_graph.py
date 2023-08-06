# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Callable, Dict, Optional, Tuple, Union

import networkx as nwkx
import numpy as nmpy

from skl_graph.graph import skl_graph_t
from skl_graph.task.plot.base import axes_t, figure_t, axes_3d_t, NewFigure,TriggerMatplotlibEventLoop
from skl_graph.task.plot.edge import Plot as PlotEdges
from skl_graph.task.plot.node import (
    Plot2DBranchNodes,
    Plot3DBranchNodes,
    Plot3DNodeLabels,
    PlotEndNodes,
)
from skl_graph.type.plot import plot_mode_e


array_t = nmpy.ndarray


def Plot(
    skl_graph: skl_graph_t,
    /,
    *,
    figure: figure_t = None,
    axes: axes_t = None,
    mode: plot_mode_e = plot_mode_e.SKL,
    max_distance: float = 1.0,
    colormap: Dict[int, str] = None,
    should_block: bool = True,
    should_return_figure: bool = False,
    should_return_axes: bool = False,
) -> Optional[Union[figure_t, axes_t, Tuple[figure_t, axes_t]]]:
    #
    if skl_graph.number_of_nodes() < 1:
        print("Empty graph")
        return None

    if axes is None:
        if figure is None:
            figure = NewFigure()
        if skl_graph.dim == 2:
            axes = figure.gca()
        else:
            axes = figure.add_subplot(1, 1, 1, projection=axes_3d_t.name)
        axes.invert_yaxis()
    else:
        figure = axes.get_figure()

    if axes.yaxis_inverted():
        transformation = lambda y: y
        vector_transf = lambda y: y
    else:
        max_0 = skl_graph.domain_lengths[0] - 1
        transformation = lambda y: max_0 - nmpy.asarray(y)
        vector_transf = lambda y: -nmpy.asarray(y)

    transform_coords = lambda pos: (pos[1], transformation(pos[0]), *pos[2:])
    positions_as_dict = dict(
        (uid, transform_coords(node.position))
        for uid, node in skl_graph.nodes.data("as_node_t")
    )

    if skl_graph.dim == 2:
        if mode is plot_mode_e.Networkx:
            _PlotWithNetworkX(skl_graph, positions_as_dict, axes, colormap)
        #
        elif mode in (
            plot_mode_e.SKL,
            plot_mode_e.SKL_Polyline,
            plot_mode_e.SKL_Curve,
        ):
            _PlotExplicitly(
                skl_graph,
                positions_as_dict,
                transformation,
                vector_transf,
                axes,
                mode,
                max_distance,
            )
        #
        elif mode is plot_mode_e.Graphviz:
            _PlotWithGraphviz(skl_graph, axes)
        #
        else:
            raise ValueError(f"{mode}: Invalid plotting mode")
        #
    else:
        _PlotExplicitly(
            skl_graph,
            positions_as_dict,
            transformation,
            vector_transf,
            axes,
            mode,
            max_distance,
        )

    if skl_graph.dim == 2:
        # Matplotlib says: NotImplementedError: It is not currently possible to manually set the aspect on 3D axes
        axes.axis("equal")

    if should_block:
        TriggerMatplotlibEventLoop()
        return None
    elif should_return_figure:
        if should_return_axes:
            return figure, axes
        else:
            return figure
    elif should_return_axes:
        return axes

    return None


def _PlotExplicitly(
    skl_graph: skl_graph_t,
    positions_as_dict: Dict[str, Tuple[int, ...]],
    transformation: Callable[[array_t], array_t],
    vector_transf: Callable[[array_t], array_t],
    axes: axes_t,
    mode: plot_mode_e,
    max_distance: float,
) -> None:
    #
    if mode == plot_mode_e.SKL:
        mode = "site"
    elif mode == plot_mode_e.SKL_Polyline:
        mode = "polyline"
    else:
        mode = "curve"
    PlotEdges(
        skl_graph.edges.data("as_edge_t"),
        transformation,
        vector_transf,
        axes,
        skl_graph.edge_styles,
        skl_graph.direction_style,
        skl_graph.label_styles[1],
        mode=mode,
        max_distance=max_distance,
    )
    # TODO: there is no distinction between end nodes and isolated nodes
    PlotEndNodes(
        skl_graph.nodes.data("as_node_t"),
        transformation,
        axes,
        skl_graph.node_styles.get(1, skl_graph.node_styles[None]),
    )

    if skl_graph.dim == 2:
        Plot2DBranchNodes(
            skl_graph.nodes.data("as_node_t"),
            skl_graph.degree,
            transformation,
            axes,
            skl_graph.node_styles,
        )
        if skl_graph.label_styles[0].show:
            nwkx.draw_networkx_labels(
                skl_graph,
                ax=axes,
                pos=positions_as_dict,
                font_size=int(round(skl_graph.label_styles[0].size)),
                font_color=skl_graph.label_styles[0].color,
            )
    else:
        Plot3DBranchNodes(
            skl_graph.nodes.data("as_node_t"),
            skl_graph.degree,
            transformation,
            axes,
            skl_graph.node_styles,
        )
        if skl_graph.label_styles[0].show:
            Plot3DNodeLabels(
                skl_graph, positions_as_dict, axes, skl_graph.label_styles[0]
            )


def _PlotWithNetworkX(
    skl_graph: skl_graph_t,
    positions_as_dict: Dict[str, Tuple[int, ...]],
    axes: axes_t,
    colormap: Optional[Dict[int, str]],
) -> None:
    #
    if colormap is None:
        colormap = skl_graph.__class__.colormap

    node_degrees = (elm[1] for elm in skl_graph.degree)
    node_colors = tuple(
        colormap[degree] if degree < 3 else colormap[2] for degree in node_degrees
    )

    nwkx.draw_networkx(
        skl_graph,
        ax=axes,
        pos=positions_as_dict,
        node_color=node_colors,
        with_labels=skl_graph.label_styles[0].show,
        font_size=int(round(skl_graph.label_styles[0].size)),
        width=skl_graph.edge_styles[0].size,
    )
    if skl_graph.label_styles[1].show:
        nwkx.draw_networkx_edge_labels(
            skl_graph,
            ax=axes,
            pos=positions_as_dict,
            edge_labels=_EdgeIDsForPlot(skl_graph),
            font_size=int(round(skl_graph.label_styles[1].size)),
        )


def _PlotWithGraphviz(skl_graph: skl_graph_t, axes: axes_t) -> None:
    #
    try:
        import tempfile as tp_

        import imageio as io_
        import pygraphviz as gp_

        graph = nwkx.nx_agraph.to_agraph(skl_graph)
        with tp_.NamedTemporaryFile() as tmp_accessor:
            img_name = tmp_accessor.name
            graph.layout()
            graph.draw(img_name, format="png")
            axes.imshow(io_.v3.imread(img_name))
    except Exception as exc:
        axes.text(
            0,
            0,
            f"Unable to plot graph using pygraphviz/imageio.\nPlease check installed modules.\n[{exc}]",
            horizontalalignment="center",
        )


def _EdgeIDsForPlot(skl_graph) -> Dict[str, str]:
    #
    lengths_as_dict = nwkx.get_edge_attributes(skl_graph, "length")
    w_lengths_as_dict = (
        nwkx.get_edge_attributes(skl_graph, "w_length")
        if skl_graph.has_widths
        else None
    )

    w_length_str = ""
    edge_ids = {}
    for key, value in lengths_as_dict.items():
        if w_lengths_as_dict is not None:
            w_length_str = "/" + str(round(w_lengths_as_dict[key]))
        edge_ids[key[0:2]] = key[2] + "\n" + str(round(value)) + w_length_str

    return edge_ids
