"""Серверная оптимизация маршрута (fallback, если Mini App не справился).

Основная логика оптимизации живёт в Mini App (OSRM Trip API + nearest neighbor),
но здесь реализован тот же алгоритм на Python на случай серверного использования.
"""
from math import atan2, cos, radians, sin, sqrt


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Расстояние между двумя точками по большому кругу, км."""
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def nearest_neighbor(
    start: tuple[float, float],
    stops: list[dict],
) -> list[dict]:
    """Жадный алгоритм коммивояжёра.

    stops: [{"lat": .., "lon": ..., ...}, ...]
    Возвращает список в оптимальном порядке.
    """
    remaining = list(stops)
    ordered: list[dict] = []
    cur_lat, cur_lon = start
    while remaining:
        nearest = min(
            remaining,
            key=lambda s: haversine(cur_lat, cur_lon, s["lat"], s["lon"]),
        )
        ordered.append(nearest)
        cur_lat, cur_lon = nearest["lat"], nearest["lon"]
        remaining.remove(nearest)
    return ordered
