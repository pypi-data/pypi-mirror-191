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

from typing import Callable, Dict, Iterable, Tuple

import numpy as nmpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as polygons_3d_t
from scipy import spatial as sptl

from skl_graph.task.plot.base import axes_t
from skl_graph.type.node import array_t, branch_node_t, end_node_t, node_t
from skl_graph.type.plot import label_style_t, node_style_t, node_styles_h


def PlotEndNodes(
    nodes: Iterable[Tuple[str, node_t]],
    transformation: Callable[[array_t], array_t],
    axes: axes_t,
    node_style: node_style_t,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    positions = nmpy.array(
        tuple(node.position for _, node in nodes if isinstance(node, end_node_t))
    )
    if positions.size == 0:
        return

    plot_style = node_style.color + node_style.type

    if positions.shape[1] == 2:
        axes.plot(
            positions[:, 1],
            transformation(positions[:, 0]),
            plot_style,
            markersize=node_style.size,
        )
    else:
        axes.plot3D(
            positions[:, 1],
            transformation(positions[:, 0]),
            positions[:, 2],
            plot_style,
            markersize=node_style.size,
        )


def Plot2DBranchNodes(
    nodes: Iterable[Tuple[str, node_t]],
    degrees: Iterable[Dict[str, int]],
    transformation: Callable[[array_t], array_t],
    axes: axes_t,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    positions_0, positions_1, types, sizes, colors = [], [], [], [], []
    for label, node in nodes:
        if isinstance(node, branch_node_t):
            node_style = node_styles.get(degrees[label], default_style)

            coords_0 = node.sites[1]
            coords_1 = transformation(node.sites[0])
            if coords_0.size > 2:
                try:
                    hull = sptl.ConvexHull(nmpy.transpose((coords_0, coords_1)))
                except sptl.QhullError:
                    # TODO: check when this happens, in particular flat convex hull
                    axes.plot(
                        coords_0,
                        coords_1,
                        node_style.color + "-",
                        linewidth=0.3 * node_style.size,
                    )
                else:
                    vertices = hull.vertices
                    axes.fill(coords_0[vertices], coords_1[vertices], node_style.color)
            elif coords_0.size > 1:
                axes.plot(
                    coords_0,
                    coords_1,
                    node_style.color + "-",
                    linewidth=0.3 * node_style.size,
                )

            # Grouping for "better performances"
            positions_0.extend(coords_0)
            positions_1.extend(coords_1)
            types.extend(coords_0.size * (node_style.type,))
            sizes.extend(coords_0.size * (node_style.size,))
            colors.extend(coords_0.size * (node_style.color,))

    if positions_0.__len__() > 0:
        positions_0 = nmpy.array(positions_0)
        positions_1 = nmpy.array(positions_1)
        types = nmpy.array(types)
        sizes = nmpy.array(sizes)
        colors = nmpy.array(colors)
        for type_ in nmpy.unique(types):
            which = types == type_
            axes.scatter(positions_0[which], positions_1[which], marker=type_, s=sizes[which], c=colors[which])


def Plot3DBranchNodes(
    nodes: Iterable[Tuple[str, node_t]],
    degrees: Iterable[Dict[str, int]],
    transformation: Callable[[array_t], array_t],
    axes: axes_t,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    default_style = node_styles[None]
    positions_0, positions_1, positions_2, types, sizes, colors = [], [], [], [], [], []
    for label, node in nodes:
        if isinstance(node, branch_node_t):
            node_style = node_styles.get(degrees[label], default_style)

            coords_0 = node.sites[1]
            coords_1 = transformation(node.sites[0])
            coords_2 = node.sites[2]
            if coords_0.size > 3:
                try:
                    coords = nmpy.transpose((coords_0, coords_1, coords_2))
                    hull = sptl.ConvexHull(coords)
                    triangle_lst = []
                    for face in hull.simplices:
                        triangle_lst.append(
                            [coords[v_idx, :].tolist() for v_idx in face]
                        )
                    triangle_lst = polygons_3d_t(
                        triangle_lst,
                        facecolors=node_style.color,
                        edgecolors="b",
                        linewidth=0.6 * node_style.size,
                    )
                    axes.add_collection3d(triangle_lst)
                except:
                    # TODO: better space-filling drawing: to be done
                    axes.plot3D(
                        coords_0,
                        coords_1,
                        coords_2,
                        node_style.color + ".",
                        markersize=node_style.size,
                    )
            elif coords_0.size > 2:
                triangle = list(zip(coords_0, coords_1, coords_2))
                triangle_lst = polygons_3d_t([triangle], facecolors=node_style.color)
                axes.add_collection3d(triangle_lst)
            elif coords_0.size > 1:
                axes.plot3D(
                    coords_0,
                    coords_1,
                    coords_2,
                    node_style.color + "-",
                    linewidth=0.3 * node_style.size,
                )

            # Grouping for "better performances"
            positions_0.extend(coords_0)
            positions_1.extend(coords_1)
            positions_2.extend(coords_2)
            types.extend(coords_0.size * (node_style.type,))
            sizes.extend(coords_0.size * (node_style.size,))
            colors.extend(coords_0.size * (node_style.color,))

    if positions_0.__len__() > 0:
        positions_0 = nmpy.array(positions_0)
        positions_1 = nmpy.array(positions_1)
        positions_2 = nmpy.array(positions_2)
        types = nmpy.array(types)
        sizes = nmpy.array(sizes)
        colors = nmpy.array(colors)
        for type_ in nmpy.unique(types):
            which = types == type_
            axes.scatter3D(
                positions_0[which], positions_1[which], positions_2[which], marker=type_, s=sizes[which], c=colors[which]
            )


def Plot3DNodeLabels(
    nodes: Iterable[str],
    positions_as_dict: Dict[str, Tuple[int, ...]],
    axes: axes_t,
    style: label_style_t,
) -> None:
    #
    for node in nodes:
        axes.text(
            *positions_as_dict[node], node, fontsize=style.size, color=style.color
        )
