"""
pages/leaderboard.py — Column-container layout.

Instead of a CSS grid per row, we use a flexbox where each COLUMN is its own
container. All hunters' values for that column are stacked vertically inside
that container, guaranteeing perfect alignment regardless of text width.

Top 3 use wrapper divs (.lb-wrapper-top1/2/3) for animated borders.
The inner content row (.lb-row-inner) has NO animation.
"""
import reflex as rx
from solo_leveling_app.state import AppState, HunterEntry
from solo_leveling_app.components.system_ui import system_nav


# ─── Color helpers ────────────────────────────────────────────────────

def _rank_color(rank) -> str:
    return rx.match(
        rank,
        ("S", "#ffd700"), ("A", "#c084fc"), ("B", "#60a5fa"),
        ("C", "#4ade80"), ("D", "#94a3b8"), "#6b7280",
    )


# ─── ROW WRAPPER — animated border for top 3, plain for others ────────

def _row_wrapper_class(hunter: HunterEntry) -> str:
    return rx.cond(
        hunter["is_user"], "lb-row-user",
        rx.cond(
            hunter["pos"] == 1, "lb-wrapper-top1",
            rx.cond(
                hunter["pos"] == 2, "lb-wrapper-top2",
                rx.cond(
                    hunter["pos"] == 3, "lb-wrapper-top3",
                    "lb-row",
                ),
            ),
        ),
    )

def _inner_class(hunter: HunterEntry) -> str:
    """Inner grid row — no animation."""
    return rx.cond(
        hunter["pos"] <= 3,
        "lb-row-inner",
        "lb-row-inner",
    )


# ─── CELL HELPERS ─────────────────────────────────────────────────────

def _pos_cell(pos) -> rx.Component:
    return rx.cond(
        pos == 1, rx.text(pos, class_name="lb-pos-1"),
        rx.cond(
            pos == 2, rx.text(pos, class_name="lb-pos-2"),
            rx.cond(
                pos == 3, rx.text(pos, class_name="lb-pos-3"),
                rx.text(pos, style={"fontFamily": "monospace", "fontWeight": "600",
                                    "fontSize": "0.72rem", "color": "#374151"}),
            ),
        ),
    )


# ─── SINGLE HUNTER ROW ────────────────────────────────────────────────

def hunter_row(hunter: HunterEntry) -> rx.Component:
    rank     = hunter["rank"]
    pos      = hunter["pos"]
    lv       = hunter["level"]
    rank_col = _rank_color(rank)

    name_cell = rx.cond(
        hunter["is_user"],
        rx.hstack(
            rx.text(hunter["name"],
                    style={"color": "#f1f5f9", "fontSize": "0.84rem",
                           "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600"}),
            rx.text("YOU",
                    style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                           "fontSize": "0.45rem", "letterSpacing": "0.2em",
                           "color": "rgba(0,212,255,0.7)",
                           "border": "1px solid rgba(0,212,255,0.3)",
                           "background": "rgba(0,212,255,0.06)",
                           "padding": "1px 6px", "borderRadius": "2px"}),
            gap="2", align="center",
        ),
        rx.text(hunter["name"],
                style=rx.cond(
                    rank == "S",
                    {"color": "#f1f5f9", "fontSize": "0.84rem",
                     "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600"},
                    {"color": "#94a3b8", "fontSize": "0.82rem",
                     "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500"},
                )),
    )

    inner_row = rx.box(
        # The inner row uses the SAME grid as lb-row-inner (no animation)
        _pos_cell(pos),
        # Rank — text only
        rx.text(rank,
                style={"color": rank_col, "fontFamily": "'Orbitron',monospace",
                       "fontWeight": "800", "fontSize": "0.72rem"}),
        # Level
        rx.text("Lv." + lv.to_string(),
                style={"color": "rgba(100,116,139,0.6)", "fontFamily": "monospace",
                       "fontSize": "0.68rem", "fontWeight": "600"}),
        # Hunter name
        name_cell,
        # Region
        rx.text(hunter["region"],
                style={"color": "#374151", "fontSize": "0.68rem",
                       "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                       "overflow": "hidden", "textOverflow": "ellipsis",
                       "whiteSpace": "nowrap"}),
        # Intel preview
        rx.text(hunter["info"],
                style={"color": "rgba(75,85,99,0.9)", "fontSize": "0.68rem",
                       "fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                       "overflow": "hidden", "textOverflow": "ellipsis",
                       "whiteSpace": "nowrap"}),
        class_name="lb-row-inner",
    )

    # Hover card for detail
    return rx.hover_card.root(
        rx.hover_card.trigger(
            rx.box(
                inner_row,
                class_name=_row_wrapper_class(hunter),
            ),
        ),
        rx.hover_card.content(
            rx.vstack(
                rx.hstack(
                    rx.text(rank,
                            style={"color": rank_col,
                                   "fontFamily": "'Orbitron',monospace",
                                   "fontWeight": "900", "fontSize": "1rem",
                                   "padding": "4px 10px",
                                   "background": "rgba(155,89,255,0.06)",
                                   "borderRadius": "2px"}),
                    rx.vstack(
                        rx.text(hunter["name"],
                                style={"color": "#f1f5f9", "fontSize": "0.92rem",
                                       "fontWeight": "600", "fontFamily": "'Rajdhani',sans-serif"}),
                        rx.hstack(
                            rx.text("Level", style={"color": "rgba(100,116,139,0.5)",
                                                     "fontSize": "0.62rem",
                                                     "fontFamily": "'Rajdhani',sans-serif",
                                                     "fontWeight": "600",
                                                     "letterSpacing": "0.1em"}),
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
                                             "fontFamily": "'Rajdhani',sans-serif",
                                             "fontWeight": "700"}),
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


# ─── PAGE ─────────────────────────────────────────────────────────────

def leaderboard_page() -> rx.Component:
    return rx.box(
        system_nav(),
        rx.box(
            rx.vstack(

                # Page header
                rx.vstack(
                    rx.text("[ WORLDWIDE HUNTER REGISTRY ]",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
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

                # Your status bar
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
                    style={"padding": "14px 24px", "background": "rgba(0,212,255,0.04)",
                           "border": "1px solid rgba(0,212,255,0.15)", "borderRadius": "4px",
                           "marginBottom": "24px"},
                ),

                # Table
                rx.box(
                    # Header row
                    rx.box(
                        rx.text("#",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        rx.text("RANK",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        rx.text("LEVEL",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        rx.text("HUNTER",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        rx.text("REGION",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        rx.text("INTEL",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                       "fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "#374151"}),
                        class_name="lb-header",
                    ),
                    # Rows
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
