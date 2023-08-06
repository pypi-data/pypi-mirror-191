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

from typing import Callable, Iterable, Tuple

import numpy as nmpy

from skl_graph.task.plot.base import axes_t
from skl_graph.type.edge import array_t, edge_t
from skl_graph.type.plot import direction_style_t, edge_styles_h, label_style_t


def Plot(
    edges: Iterable[Tuple[str, str, edge_t]],
    transformation: Callable[[array_t], array_t],
    vector_transf: Callable[[array_t], array_t],
    axes: axes_t,
    edge_styles: edge_styles_h,
    direction_style: direction_style_t,
    label_style: label_style_t,
    mode: str = "site",  # "site", "polyline", "curve"
    max_distance: float = 1.0,
) -> None:
    #
    # space_dim = edges[0][2].dim  # Does not work since 'MultiEdgeDataView' object is not subscriptable
    space_dim = 2
    for _, _, edge in edges:
        space_dim = edge.dim
        break

    plot_fct = axes.plot if space_dim == 2 else axes.plot3D

    for origin, destination, edge in edges:
        if mode == "curve":
            as_curve = edge.AsCurve()
            if as_curve is None:
                sites = list(edge.sites)
            else:
                max_arc_length = as_curve[0].x.item(-1)
                step = 0.125
                arc_lengths = nmpy.arange(0.0, max_arc_length + 0.5 * step, step)
                sites = [as_curve[idx_](arc_lengths) for idx_ in range(space_dim)]
        elif mode == "polyline":
            polyline_idc = edge.AsPolyline(max_distance=max_distance)[1]
            sites = [edge.sites[idx_][polyline_idc] for idx_ in range(space_dim)]
        elif mode == "site":
            sites = list(edge.sites)
        else:
            raise ValueError(
                f"{mode}: Invalid plotting mode; Valid modes: 'site', 'polyline', 'curve'"
            )
        sites[0], sites[1] = sites[1], transformation(sites[0])

        if origin == destination:
            edge_style = edge_styles[1]
        else:
            edge_style = edge_styles[0]
        plot_style = f"{edge_style.color}." if mode == "site" else edge_style.color
        plot_fct(
            *sites,
            plot_style + edge_style.type,
            linewidth=edge_style.size,
            markersize=edge_style.size,
        )

        if direction_style.show:
            origin_direction = edge.OriginDirection()
            if origin_direction is not None:
                dir_sites = tuple(
                    nmpy.hstack((sites[idx_][0], sites[idx_][-1]))
                    for idx_ in range(space_dim)
                )
                directions = list(zip(origin_direction, edge.FinalDirection()))
                directions[0], directions[1] = (
                    directions[1],
                    vector_transf(directions[0]),
                )
                axes.quiver(
                    *dir_sites,
                    *directions,
                    color=direction_style.color,
                    linewidth=direction_style.size,
                )

        # TODO: plot edge labels
