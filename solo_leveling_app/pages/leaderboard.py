"""
pages/leaderboard.py — S-Rank to D-Rank Hunter Registry.
Phase 4 changes:
  • Top 3 border animations: #1 purple-fire, #2 orange-sun, #3 blue-pulse
  • Table width: 58.575% of page
  • Wider rows, aligned columns
  • No rank-badge border on hunter rows (removed)
  • Position numbers #1/2/3 styled with gradient text
"""
import reflex as rx
from solo_leveling_app.state import AppState, HunterEntry
from solo_leveling_app.components.system_ui import system_nav


def _rank_color(rank) -> str:
    return rx.match(
        rank,
        ("S", "#ffd700"),
        ("A", "#c084fc"),
        ("B", "#60a5fa"),
        ("C", "#4ade80"),
        ("D", "#94a3b8"),
        "#6b7280",
    )


def _row_class(hunter: HunterEntry) -> str:
    """Pick the CSS class for a leaderboard row."""
    return rx.cond(
        hunter["is_user"],
        "lb-row-user",
        rx.cond(
            hunter["pos"] == 1,
            "lb-row-top1",
            rx.cond(
                hunter["pos"] == 2,
                "lb-row-top2",
                rx.cond(
                    hunter["pos"] == 3,
                    "lb-row-top3",
                    "lb-row",
                ),
            ),
        ),
    )


def _pos_cell(pos) -> rx.Component:
    """Position number with top-3 gradient effects."""
    return rx.cond(
        pos == 1,
        rx.text(pos, class_name="lb-pos-1"),
        rx.cond(
            pos == 2,
            rx.text(pos, class_name="lb-pos-2"),
            rx.cond(
                pos == 3,
                rx.text(pos, class_name="lb-pos-3"),
                rx.text(pos,
                        style={"fontSize": "0.7rem", "color": "#374151",
                               "fontFamily": "monospace", "fontWeight": "600"}),
            ),
        ),
    )


def hunter_row(hunter: HunterEntry) -> rx.Component:
    rank     = hunter["rank"]
    pos      = hunter["pos"]
    lv       = hunter["level"]
    rank_col = _rank_color(rank)

    # Rank badge — text only, no border on the row itself
    rank_cell = rx.text(
        rank,
        style={
            "color": rank_col,
            "fontFamily": "'Orbitron', monospace",
            "fontSize": "0.72rem",
            "fontWeight": "800",
        },
    )

    level_cell = rx.text(
        "Lv." + lv.to_string(),
        style={"color": "rgba(100,116,139,0.6)", "fontFamily": "monospace",
               "fontSize": "0.68rem", "fontWeight": "600"},
    )

    name_cell = rx.text(
        hunter["name"],
        style=rx.cond(
            rank == "S",
            {"color": "#f1f5f9", "fontSize": "0.85rem", "fontWeight": "500",
             "fontFamily": "'Rajdhani', sans-serif"},
            {"color": "#94a3b8", "fontSize": "0.82rem",
             "fontFamily": "'Rajdhani', sans-serif"},
        ),
    )

    region_cell = rx.text(
        hunter["region"],
        style={"color": "#374151", "fontSize": "0.68rem",
               "fontFamily": "'Rajdhani', sans-serif", "fontWeight": "600"},
    )

    # Info preview — full width, truncated
    info_preview = rx.text(
        hunter["info"],
        style={"color": "rgba(75,85,99,0.9)", "fontSize": "0.68rem",
               "fontFamily": "'Rajdhani', sans-serif", "fontWeight": "500",
               "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"},
    )

    return rx.hover_card.root(
        rx.hover_card.trigger(
            rx.box(
                _pos_cell(pos),
                rank_cell,
                level_cell,
                rx.cond(
                    hunter["is_user"],
                    rx.hstack(
                        name_cell,
                        rx.text("YOU",
                                style={"fontSize": "0.52rem", "letterSpacing": "0.2em",
                                       "color": "rgba(0,212,255,0.7)",
                                       "border": "1px solid rgba(0,212,255,0.3)",
                                       "background": "rgba(0,212,255,0.06)",
                                       "padding": "1px 7px", "borderRadius": "2px",
                                       "fontFamily": "'Orbitron',monospace"}),
                        gap="2", align="center",
                    ),
                    name_cell,
                ),
                region_cell,
                info_preview,
                class_name=_row_class(hunter),
            ),
        ),
        rx.hover_card.content(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        rank,
                        style={"color": rank_col,
                               "fontFamily": "'Orbitron', monospace",
                               "fontSize": "1rem", "fontWeight": "900",
                               "padding": "4px 10px",
                               "background": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                               "borderRadius": "2px"},
                    ),
                    rx.vstack(
                        rx.text(hunter["name"],
                                style={"color": "#f1f5f9", "fontSize": "0.92rem",
                                       "fontWeight": "600", "fontFamily": "'Rajdhani',sans-serif"}),
                        rx.hstack(
                            rx.text("Level", style={"color": "rgba(100,116,139,0.5)",
                                                     "fontSize": "0.62rem", "letterSpacing": "0.15em",
                                                     "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600"}),
                            rx.text(lv.to_string(),
                                    style={"color": "rgba(0,212,255,0.7)",
                                           "fontFamily": "monospace", "fontSize": "0.68rem"}),
                            gap="2",
                        ),
                        gap="0.5",
                    ),
                    gap="3", align="center",
                ),
                rx.box(class_name="w-full h-px bg-system-border"),
                rx.text(hunter["info"],
                        style={"color": "#94a3b8", "fontSize": "0.8rem",
                               "lineHeight": "1.6", "fontFamily": "'Rajdhani',sans-serif",
                               "fontWeight": "500"}),
                rx.hstack(
                    rx.text("REGION", style={"color": "#374151", "fontSize": "0.6rem",
                                             "letterSpacing": "0.15em",
                                             "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700"}),
                    rx.text(hunter["region"],
                            style={"color": "#6b7280", "fontSize": "0.72rem",
                                   "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600"}),
                    gap="2",
                ),
                gap="3", align="start",
            ),
            class_name="system-card p-4",
            style={"background": "rgba(8,8,15,0.99)",
                   "border": "1px solid rgba(155,89,255,0.3)",
                   "boxShadow": "0 0 24px rgba(155,89,255,0.15)",
                   "minWidth": "300px", "maxWidth": "380px"},
        ),
    )


def leaderboard_page() -> rx.Component:
    return rx.box(
        system_nav(),
        rx.box(
            rx.vstack(

                # Page header
                rx.vstack(
                    rx.text("[ WORLDWIDE HUNTER REGISTRY ]",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                   "fontSize": "0.62rem", "letterSpacing": "0.3em",
                                   "color": "#374151"}),
                    rx.text("Leaderboard",
                            class_name="app-name-cinzel",
                            style={"fontSize": "2.2rem", "fontWeight": "900"}),
                    rx.text("Registered hunters, ranked by classification.",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                                   "fontSize": "0.8rem", "color": "rgba(100,116,139,0.5)"}),
                    gap="2", class_name="mb-8", align="center",
                ),

                # Your status compact bar
                rx.box(
                    rx.hstack(
                        rx.text("YOUR POSITION",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "rgba(100,116,139,0.4)"}),
                        rx.spacer(),
                        rx.hstack(
                            rx.text(AppState.user_name,
                                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                           "fontSize": "0.9rem", "color": "#f1f5f9"}),
                            rx.text("·", style={"color": "#1e293b"}),
                            rx.text("LVL",
                                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                           "fontSize": "0.6rem", "color": "rgba(100,116,139,0.4)",
                                           "letterSpacing": "0.15em"}),
                            rx.text(AppState.level,
                                    style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                                           "fontSize": "0.85rem", "color": "#00d4ff"}),
                            rx.text("·", style={"color": "#1e293b"}),
                            rx.text("RANK",
                                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                           "fontSize": "0.6rem", "color": "rgba(100,116,139,0.4)",
                                           "letterSpacing": "0.15em"}),
                            rx.text(AppState.hunter_rank,
                                    class_name=AppState.rank_color_class,
                                    style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                           "fontSize": "0.85rem"}),
                            gap="2", align="center",
                        ),
                        width="100%", align="center",
                    ),
                    style={"padding": "14px 24px",
                           "background": "rgba(0,212,255,0.04)",
                           "border": "1px solid rgba(0,212,255,0.15)",
                           "borderRadius": "4px",
                           "marginBottom": "24px"},
                ),

                # Leaderboard table (58.575% width)
                rx.box(
                    # Header row
                    rx.box(
                        rx.text("#",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        rx.text("RANK",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        rx.text("LEVEL",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        rx.text("HUNTER",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        rx.text("REGION",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        rx.text("INTEL",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.62rem", "letterSpacing": "0.2em", "color": "#374151"}),
                        class_name="lb-header",
                    ),
                    # Hunter rows
                    rx.vstack(
                        rx.foreach(AppState.leaderboard_with_user, hunter_row),
                        gap="0", width="100%",
                    ),
                    class_name="lb-table-container system-card overflow-hidden",
                ),

                gap="0", width="100%", align="center",
            ),
            class_name="pt-20 px-4 pb-16",
        ),
        class_name="min-h-screen portal-bg",
    )
