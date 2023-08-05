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

from __future__ import annotations

from typing import List, Tuple

import numpy as nmpy
import skimage.measure as ms_

import skl_graph.brick.elm_id as id_
import skl_graph.type.topology_map as bymp
from skl_graph.brick.constants import UNTESTED_VALIDITY


array_t = nmpy.ndarray


class node_t:
    #
    __slots__ = ("uid", "position", "invalidities")

    uid: str
    position: array_t
    invalidities: List[str]  # Use brick.constants.UNTESTED_VALIDITY as initial value

    def __init__(self):
        #
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)
        self.invalidities = UNTESTED_VALIDITY

    def _SetUID(self) -> None:
        #
        self.uid = id_.COORDINATE_SEPARATOR.join(
            coord.__str__() for coord in self.position
        )

    @property
    def is_valid(self) -> bool:
        """"""
        output = True
        self.invalidities = []

        if self.uid is None:
            output = False
            self.invalidities.append("Has no UID")

        return output

    def __str__(self) -> str:
        """"""
        return f"{self.__class__.__name__}[{self.uid}]: Pos={self.position}"


class end_node_t(node_t):
    #
    __slots__ = ("diameter",)

    diameter: float

    def __init__(self):
        #
        super().__init__()
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)

    @classmethod
    def WithPosition(cls, position: array_t, width_map: array_t = None) -> end_node_t:
        #
        instance = cls()

        instance.position = position
        if width_map is not None:
            instance.diameter = width_map.item(tuple(position))
        instance._SetUID()

        return instance


class branch_node_t(node_t):
    #
    __slots__ = ("sites", "diameters")

    sites: Tuple[array_t, ...]
    diameters: array_t

    def __init__(self):
        #
        super().__init__()
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)

    @classmethod
    def WithCentroidAndSites(
        cls, centroid: array_t, sites: Tuple[array_t, ...], width_map: array_t = None
    ) -> branch_node_t:
        #
        # TODO: why passing the centroid instead of computing it here from sites?
        # TODO: sites is not optional but seems to be considered as such from at least a calling function (do a search to find out which)
        instance = cls()

        sites_as_array = nmpy.array(sites)
        centroid = nmpy.around(centroid).reshape((-1, 1))
        segments = sites_as_array - centroid
        medoid_idx = (segments**2).sum(axis=0).argmin()
        # nmpy.array(): fresh array instead of a view of sites_as_array
        position = nmpy.array(sites_as_array[:, medoid_idx].squeeze())

        instance.position = position
        instance.sites = sites
        if width_map is not None:
            instance.diameters = width_map[sites]
        instance._SetUID()

        return instance


def EndNodes(
    part_map: array_t, width_map: array_t = None
) -> Tuple[List[end_node_t], array_t]:
    #
    # Note: End nodes are necessarily single-pixel nodes. Hence, they have no coordinate list.
    #
    # Not uint to allow for subtraction
    e_node_lmap = (part_map == 1).astype(nmpy.int64)  # Not really an lmsk here
    e_node_coords = nmpy.where(e_node_lmap)

    e_nodes = e_node_coords[0].__len__() * [end_node_t()]
    for n_idx, position in enumerate(zip(*e_node_coords)):
        end_node = end_node_t.WithPosition(
            nmpy.array(position, dtype=nmpy.int64), width_map=width_map
        )
        e_nodes[n_idx] = end_node
        e_node_lmap[position] = n_idx + 1  # Now that's becoming an lmsk

    return e_nodes, e_node_lmap


def BranchNodes(
    part_map: array_t, width_map: array_t = None
) -> Tuple[List[branch_node_t], array_t]:
    #
    # Note: Branch nodes always have a coordinate list (i.e., even if they are single-pixeled)
    #
    b_node_map = nmpy.logical_and(
        part_map > 2, part_map != bymp.TMapBackgroundLabel(part_map)
    )
    b_node_lmap, n_b_nodes = bymp.LABELING_FCT_FOR_DIM[part_map.ndim](b_node_map)

    b_node_props = ms_.regionprops(b_node_lmap)

    b_nodes = n_b_nodes * [branch_node_t()]
    for n_idx, props in enumerate(b_node_props):
        sites = props.image.nonzero()
        for d_idx in range(part_map.ndim):
            sites[d_idx].__iadd__(props.bbox[d_idx])
        branch_node = branch_node_t.WithCentroidAndSites(
            props.centroid, sites=sites, width_map=width_map
        )
        b_nodes[n_idx] = branch_node

    return b_nodes, b_node_lmap


