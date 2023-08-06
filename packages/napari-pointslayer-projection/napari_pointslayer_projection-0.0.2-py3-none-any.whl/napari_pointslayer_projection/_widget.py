"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from napari.layers import Points

if TYPE_CHECKING:
    import napari


def project_points(
    points_data: "napari.types.PointsData",
    face_color: str = "red",
    edge_color: str = "red",
) -> "napari.layers.Points":
    return Points(
        points_data[:, -2:],
        name="projected points",
        ndim=2,
        face_color=face_color,
        edge_color=edge_color,
    )
