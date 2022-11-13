import random

import typer
from rich import print
from rich.console import Console

from wte.gateways import wolt
from wte.models import Ordering, Sort
from wte.models.config import Profile
from wte.models.wolt import Item
from wte.services import filters
from wte.services.display import build_items_table, build_restaurant_table
from wte.services.utils import build_weights


def items_controller(
    items: list[Item],
    profile: Profile,
    query: str | None,
    tag: str | None,
    sort: Sort,
    ordering: Ordering,
    limit: int | None,
) -> None:
    if query:
        items = filters.filter_by_query(items, query)
    if tag:
        items = filters.filter_by_tag(items, tag)
    if sort:
        items = filters.sort_by(items, sort, ordering)
    if limit:
        items = items[:limit]

    if not items:
        print("[red]No restaurants found")
        raise typer.Exit(0)

    table = build_items_table(items=items)
    table.caption = f":popcorn: Restaurants in [italic bold cyan]{profile.address}[/] via wolt :popcorn:"

    console = Console()
    console.print(table)


def restaurant_controller(items: list[Item], restaurant: str) -> None:
    items = filters.filter_by_name(items, restaurant)

    if len(items) == 0:
        print(f"[red]Restaurant [cyan italic]{restaurant}[/][red] not found[/red]")
        raise typer.Exit()
    if len(items) > 1:
        print(
            f"[red]More than one restaurant found for [cyan italic]{restaurant}[/][red]. "
            f"Try to specify one restaurant[/red]"
        )
        raise typer.Exit()

    restaurant = wolt.restaurant(items[0])  # type: ignore[assignment]
    table = build_restaurant_table(restaurant)  # type: ignore[arg-type]

    console = Console()
    console.print(table)


def random_controller(items: list[Item], tag: str | None,) -> None:
    if tag:
        items = filters.filter_by_tag(items, tag)

    if not items:
        print("[red]No restaurants found")
        raise typer.Exit(0)

    item = random.choices(population=items, weights=build_weights(items), k=1)[0]
    restaurant = wolt.restaurant(item)

    table = build_restaurant_table(restaurant=restaurant)

    console = Console()
    console.print(table)
