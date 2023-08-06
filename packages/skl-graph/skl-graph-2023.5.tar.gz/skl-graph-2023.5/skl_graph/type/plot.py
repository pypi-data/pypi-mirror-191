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

import dataclasses as dtcl
from enum import Enum as enum_t
from typing import ClassVar, Dict, Tuple, Union


node_style_raw_h = Tuple[str, int, str]  # type, size, color
node_styles_raw_h = Dict[Union[int, None], node_style_raw_h]
node_either_raw_h = Union[node_style_raw_h, node_styles_raw_h]

edge_style_raw_h = node_style_raw_h
edge_styles_raw_h = Tuple[edge_style_raw_h, edge_style_raw_h]

# show, size, color | show (False)
label_style_raw_h = Union[Tuple[bool, float, str], bool]
label_styles_raw_h = Tuple[label_style_raw_h, label_style_raw_h]

# show, size, color | show (False)
direction_style_raw_h = Union[Tuple[bool, int, str], bool]


class plot_mode_e(enum_t):
    Networkx = 0
    SKL = 1
    SKL_Polyline = 2
    SKL_Curve = 3
    Graphviz = 4


@dtcl.dataclass
class node_style_t:
    type: str  # E.g., "."
    size: int  # "markersize"
    color: str  # E.g., "b"

    DEFAULT_TYPE: ClassVar[str] = "."
    DEFAULT_SIZE: ClassVar[int] = 6
    DEFAULT_COLORS: ClassVar[Tuple[Tuple[int | None, str]]] = ((None, "g"), (1, "r"))

    @classmethod
    def Default(cls) -> node_styles_h:
        """"""
        return {
            _key: cls(type=cls.DEFAULT_TYPE, size=cls.DEFAULT_SIZE, color=_vle)
            for _key, _vle in cls.DEFAULT_COLORS
        }

    @classmethod
    def NewFromUnstructured(cls, style: node_either_raw_h, /) -> node_styles_h:
        """"""
        if isinstance(style, tuple):  # node_style_raw_h
            output = {None: cls(type=style[0], size=style[1], color=style[2])}
        else:
            output = {
                _dgr: cls(type=_stl[0], size=_stl[1], color=_stl[2])
                for _dgr, _stl in style.items()
            }

        return output


@dtcl.dataclass
class edge_style_t:
    type: str  # E.g., "-"
    size: int  # "linewidth"
    color: str  # E.g., "b"

    DEFAULT_TYPES: ClassVar[Tuple[str, str]] = ("-", ":")  # Regular, self-loop
    DEFAULT_SIZE: ClassVar[int] = 2
    DEFAULT_COLOR: ClassVar[str] = "k"

    @classmethod
    def Default(cls) -> edge_styles_h:
        """"""
        # noinspection PyTypeChecker
        return tuple(
            cls(type=_typ, size=cls.DEFAULT_SIZE, color=cls.DEFAULT_COLOR)
            for _typ in cls.DEFAULT_TYPES
        )

    @classmethod
    def AllFromUnstructured(
        cls,
        current: edge_styles_h,
        /,
        *,
        edge: edge_style_raw_h = None,
        regular_edge: edge_style_raw_h = None,
        self_loop: edge_style_raw_h = None,
        edges: edge_styles_raw_h = None,
    ) -> edge_styles_h | None:
        """"""
        return _AllFromUnstructured(
            edge_style_t,
            current,
            common=edge,
            first=regular_edge,
            last=self_loop,
            both=edges,
        )

    @classmethod
    def NewFromUnstructured(cls, style: edge_style_raw_h, /) -> edge_style_t:
        """"""
        return cls(type=style[0], size=style[1], color=style[2])


@dtcl.dataclass
class label_style_t:
    show: bool
    size: float  # "fontsize"
    color: str  # "k"

    DEFAULT_SIZE: ClassVar[float] = 6.0
    DEFAULT_COLOR: ClassVar[str] = "k"

    @classmethod
    def Default(cls) -> label_styles_h:
        """"""
        return (
            cls.DefaultForNodes(),
            cls.DefaultForEdges(),
        )

    @classmethod
    def DefaultForNodes(cls) -> label_style_t:
        """"""
        return cls.NewFromUnstructured(True)

    @classmethod
    def DefaultForEdges(cls) -> label_style_t:
        """"""
        return cls.NewFromUnstructured(False)

    @classmethod
    def AllFromUnstructured(
        cls,
        current: label_styles_h,
        /,
        *,
        label: label_style_raw_h = None,
        node: label_style_raw_h = None,
        edge: label_style_raw_h = None,
        labels: label_styles_raw_h = None,
    ) -> label_styles_h | None:
        """"""
        return _AllFromUnstructured(
            label_style_t,
            current,
            common=label,
            first=node,
            last=edge,
            both=labels,
        )

    @classmethod
    def NewFromUnstructured(cls, style: label_style_raw_h, /) -> label_style_t:
        """"""
        if isinstance(style, bool):
            show = style
            size = cls.DEFAULT_SIZE
            color = cls.DEFAULT_COLOR
        else:
            show, size, color = style

        return cls(show=show, size=size, color=color)


@dtcl.dataclass
class direction_style_t:
    show: bool
    size: int  # "linewidth"
    color: str  # "k"

    DEFAULT_SIZE: ClassVar[int] = 2
    DEFAULT_COLOR: ClassVar[str] = "y"

    @classmethod
    def Default(cls) -> direction_style_t:
        """"""
        return cls.NewFromUnstructured(False)

    @classmethod
    def NewFromUnstructured(cls, style: direction_style_raw_h, /) -> direction_style_t:
        """"""
        if isinstance(style, bool):
            show = style
            size = cls.DEFAULT_SIZE
            color = cls.DEFAULT_COLOR
        else:
            show, size, color = style

        return cls(show=show, size=size, color=color)


node_styles_h = Dict[Union[int, None], node_style_t]
edge_styles_h = Tuple[edge_style_t, edge_style_t]  # regular edges, self-loops
label_styles_h = Tuple[label_style_t, label_style_t]  # nodes, edges


def _AllFromUnstructured(
    class_: edge_style_t.__class__ | label_style_t.__class__,
    current: edge_styles_h | label_styles_h,
    /,
    *,
    common: edge_style_raw_h | label_styles_raw_h = None,
    first: edge_style_raw_h | label_styles_raw_h = None,
    last: edge_style_raw_h | label_styles_raw_h = None,
    both: edge_styles_raw_h | label_styles_raw_h = None,
) -> edge_styles_h | label_styles_h | None:
    """"""
    if common is not None:
        style = class_.NewFromUnstructured(common)
        output = (style, style)
    elif first is not None:
        style = class_.NewFromUnstructured(first)
        output = (style, current[1])
    elif last is not None:
        style = class_.NewFromUnstructured(last)
        output = (current[0], style)
    elif both is not None:
        output = tuple(map(class_.NewFromUnstructured, both))
    else:
        output = None

    return output
