from typing import List

from geopy import distance
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from ..models.municipality import MuncipalityWithDistance, Municipality


def search_close_meeting_points(
    all_points: List[Municipality],
    latitude: float,
    longitude: float,
    radius_km: int,
) -> List[MuncipalityWithDistance]:
    """
    Search the closest meeting points.
    Args:
        all_points (List[Municipality]): list of the municipality.
        latitude (float): latitude of the muncipality.
        longitude (float): longitude of the muncipality.
        radius_km (int): radius_km of the muncipality.
    Raises:
        HTTPException: Raise http-400 when there is bad type of params.
    Returns:
        List[MuncipalityWithDistance]: The list of closest meeting point.
    """
    close_points: List[MuncipalityWithDistance] = []
    try:
        for point in all_points:
            copy_point = point.copy()
            copy_point["distance_km"] = round(
                distance.distance(
                    (latitude, longitude), (point["latitude"], point["longitude"])
                ).km,
                2,
            )
            if copy_point["distance_km"] < radius_km:
                close_points.append(copy_point)
    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Bad type of params"
        )
    return close_points
