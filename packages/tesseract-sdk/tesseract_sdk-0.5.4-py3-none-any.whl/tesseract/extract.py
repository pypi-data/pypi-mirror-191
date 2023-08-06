import numpy as np
from geodesic.utils import DeferredImport
from shapely.geometry import Polygon

measure = DeferredImport("skimage.measure")


def extract_polygons(x: np.ndarray, value=None, threshold_func=None, min_area=1.0, simplify_threshold=1.0):
    if x.ndim != 2:
        raise ValueError(f"extract_polygons only works on 2D arrays, got {x.ndim}")

    y = x
    if threshold_func is not None:
        y = threshold_func(x)
    elif value is not None:
        y = x == value

    contours = measure.find_contours(y, level=0.5)

    rows, cols = x.shape

    shapes = [
        Polygon(shell=zip(contour[:, 1] / (cols - 1), contour[:, 0] / (rows - 1)))
        for contour in contours
        if len(contour) > 2
    ]

    # filter based on area
    shapes = [
        shape
        for shape in shapes
        if (shape.area > (min_area / (cols - 1) / (rows - 1))
            and shape.exterior.coords[0] == shape.exterior.coords[-1])]
    # simplify - use a simplify threshold in pixels, convert to normalized tile coordinate distance
    distance_convert = np.sqrt(rows*rows + cols*cols)
    shapes = [shape.simplify(simplify_threshold / distance_convert) for shape in shapes]
    # filter out invalid polygons
    shapes = [shape for shape in shapes if shape.is_valid]

    return shapes
