"""In-memory хранилище последних маршрутов + форматирование."""
from bot.middlewares.i18n import t

_last_routes: dict[int, dict] = {}


def save_last_route(user_id: int, data: dict) -> None:
    _last_routes[user_id] = data


def get_last_route(user_id: int) -> dict | None:
    return _last_routes.get(user_id)


def format_route(user_id: int, data: dict) -> str:
    """Форматирует сообщение о построенном маршруте."""
    lines = [t(user_id, "route_built"), ""]
    for i, stop in enumerate(data.get("stops", []), 1):
        name = stop.get("name") or f"#{i}"
        lines.append(f"{i}️⃣ <b>{name}</b>")
        if stop.get("address"):
            lines.append(f"   📍 {stop['address']}")
        if stop.get("comment"):
            lines.append(f"   💬 {stop['comment']}")
        lines.append("")
    if data.get("total_distance"):
        lines.append(f"{t(user_id, 'total_distance')}: <b>{data['total_distance']}</b>")
    if data.get("total_time"):
        lines.append(f"{t(user_id, 'total_time')}: <b>{data['total_time']}</b>")
    return "\n".join(lines)


def format_completion(user_id: int, data: dict) -> str:
    """Форматирует отчёт о завершении маршрута."""
    lines = [t(user_id, "route_complete"), ""]
    done = data.get("done", 0)
    total = data.get("total", 0)
    lines.append(f"{t(user_id, 'deliveries_done')}: <b>{done}/{total}</b>")
    if data.get("total_distance"):
        lines.append(f"{t(user_id, 'distance_traveled')}: <b>{data['total_distance']}</b>")
    if data.get("total_time"):
        lines.append(f"{t(user_id, 'time_spent')}: <b>{data['total_time']}</b>")
    return "\n".join(lines)


def format_last_route(user_id: int, data: dict) -> str:
    return format_route(user_id, data)
