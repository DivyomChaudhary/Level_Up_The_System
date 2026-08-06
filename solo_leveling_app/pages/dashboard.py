"""
pages/dashboard.py — Final.

Layout:
  Top row  : [Level/XP card] [Streak] [STR] [INT] [PER]
  Quest row : Three equal-width contained columns, each with
              its own bordered card header + scrollable quest list.
              Monthly column also hosts the rift mini widget.
"""
import reflex as rx
from solo_leveling_app.state import AppState, QuestItem
from solo_leveling_app.components.system_ui import (
    system_nav, xp_bar, streak_counter,
    quest_type_badge, penalty_dialog, quest_verify_overlay, key_popup,
)


# ──────────────────────────────────────────────────────────────────────
# QUEST ROW COMPONENTS
# ──────────────────────────────────────────────────────────────────────

def _quest_row_daily(quest: QuestItem) -> rx.Component:
    return rx.box(
        rx.hstack(
            # Checkbox
            rx.box(
                rx.cond(
                    quest["done"],
                    rx.text("✓", class_name="text-[11px] font-black text-system-black"),
                    rx.fragment(),
                ),
                on_click=AppState.quest_click(quest["id"]),
                class_name=rx.cond(
                    quest["done"],
                    "w-5 h-5 rounded-sm bg-neon-blue flex items-center justify-center "
                    "cursor-pointer flex-shrink-0",
                    "w-5 h-5 rounded-sm border border-slate-700 flex items-center "
                    "justify-center cursor-pointer flex-shrink-0 hover:border-neon-blue/50 "
                    "transition-colors",
                ),
            ),
            # Title + badge
            rx.hstack(
                rx.text(
                    quest["title"],
                    class_name=rx.cond(
                        quest["done"],
                        "text-xs text-slate-600 line-through flex-1",
                        "text-xs text-slate-200 flex-1",
                    ),
                ),
                quest_type_badge(quest["type"]),
                gap="2", align="center", flex="1",
            ),
            gap="3", align="center", width="100%",
        ),
        class_name=rx.cond(
            quest["done"],
            "p-3 rounded border border-system-border/30 bg-system-card/40 "
            "opacity-50 transition-all duration-300",
            "p-3 rounded border border-system-border/60 bg-system-card/60 "
            "hover:border-neon-blue/25 cursor-pointer transition-all duration-200",
        ),
    )


def _quest_row_toggle(quest: QuestItem, on_toggle, accent: str = "purple") -> rx.Component:
    col_class = "bg-neon-blue" if accent == "blue" else "bg-neon-purple"
    hover_class = "hover:border-neon-blue/25" if accent == "blue" else "hover:border-neon-purple/25"
    return rx.box(
        rx.hstack(
            rx.box(
                rx.cond(
                    quest["done"],
                    rx.text("✓", class_name="text-[11px] font-black text-system-black"),
                    rx.fragment(),
                ),
                on_click=on_toggle(quest["id"]),
                class_name=rx.cond(
                    quest["done"],
                    f"w-5 h-5 rounded-sm {col_class} flex items-center justify-center "
                    "cursor-pointer flex-shrink-0",
                    "w-5 h-5 rounded-sm border border-slate-700 flex items-center "
                    f"justify-center cursor-pointer flex-shrink-0 {hover_class.replace('hover:','hover:')} "
                    "transition-colors",
                ),
            ),
            rx.hstack(
                rx.text(
                    quest["title"],
                    class_name=rx.cond(
                        quest["done"],
                        "text-xs text-slate-600 line-through flex-1",
                        "text-xs text-slate-300 flex-1",
                    ),
                ),
                quest_type_badge(quest["type"]),
                gap="2", align="center", flex="1",
            ),
            gap="3", align="center", width="100%",
        ),
        class_name=rx.cond(
            quest["done"],
            "p-3 rounded border border-system-border/30 bg-system-card/40 "
            "opacity-50 transition-all duration-300",
            f"p-3 rounded border border-system-border/60 bg-system-card/60 "
            f"{hover_class} cursor-pointer transition-all duration-200",
        ),
    )


# ──────────────────────────────────────────────────────────────────────
# ADD QUEST FORM (inline, per-section)
# ──────────────────────────────────────────────────────────────────────

def _add_quest_form(mode: str) -> rx.Component:
    return rx.cond(
        AppState.add_quest_mode == mode,
        rx.box(
            rx.vstack(
                rx.input(
                    placeholder="Quest title...",
                    value=AppState.new_add_quest_title,
                    on_change=AppState.set_new_add_quest_title,
                    style={
                        "background": "rgba(8,8,15,0.8)",
                        "border": "1px solid rgba(0,212,255,0.2)",
                        "borderRadius": "3px",
                        "color": "#e2e8f0",
                        "fontFamily": "'Rajdhani', sans-serif",
                        "fontWeight": "600",
                        "fontSize": "0.82rem",
                        "padding": "8px 12px",
                        "outline": "none",
                        "width": "100%",
                    },
                ),
                rx.hstack(
                    rx.select(
                        ["DSA", "DEV", "FITNESS", "CUSTOM"],
                        value=AppState.new_add_quest_type,
                        on_change=AppState.set_new_add_quest_type,
                        style={
                            "background": "rgba(8,8,15,0.8)",
                            "border": "1px solid rgba(26,26,51,0.8)",
                            "color": "#94a3b8",
                            "fontFamily": "'Rajdhani',sans-serif",
                            "fontWeight": "600",
                            "fontSize": "0.8rem",
                            "padding": "7px 10px",
                            "borderRadius": "3px",
                            "flex": "1",
                            "outline": "none",
                        },
                    ),
                    rx.button(
                        "ADD",
                        on_click=AppState.submit_add_quest,
                        style={
                            "fontFamily": "'Orbitron',monospace",
                            "fontWeight": "700",
                            "fontSize": "0.55rem",
                            "letterSpacing": "0.15em",
                            "color": "#00d4ff",
                            "border": "1px solid rgba(0,212,255,0.35)",
                            "background": "rgba(0,212,255,0.05)",
                            "padding": "7px 16px",
                            "cursor": "pointer",
                            "borderRadius": "3px",
                            "flexShrink": "0",
                        },
                    ),
                    rx.button(
                        "✕",
                        on_click=AppState.close_add_quest_form,
                        variant="ghost",
                        style={"color": "rgba(100,116,139,0.4)", "cursor": "pointer",
                               "fontSize": "0.9rem", "padding": "0 4px", "flexShrink": "0"},
                    ),
                    gap="2", align="center", width="100%",
                ),
                gap="2", width="100%",
            ),
            style={
                "background": "rgba(0,212,255,0.03)",
                "border": "1px dashed rgba(0,212,255,0.15)",
                "borderRadius": "4px",
                "padding": "10px",
                "marginBottom": "4px",
            },
        ),
        rx.fragment(),
    )


# ──────────────────────────────────────────────────────────────────────
# QUEST CONTAINER — header + quest list inside one bordered card
# ──────────────────────────────────────────────────────────────────────

def _quest_container_header(
    title: str,
    done_count,
    total_count,
    pct,
    mode: str,
    accent_color: str = "rgba(0,212,255,0.5)",
) -> rx.Component:
    return rx.hstack(
        # Left: title + count
        rx.vstack(
            rx.text(
                title,
                style={
                    "fontFamily": "'Orbitron', monospace",
                    "fontWeight": "700",
                    "fontSize": "0.55rem",
                    "letterSpacing": "0.25em",
                    "color": accent_color,
                },
            ),
            rx.hstack(
                rx.text(done_count,
                        style={"fontFamily": "monospace", "fontWeight": "700",
                               "fontSize": "0.75rem", "color": "#00d4ff"}),
                rx.text("/", style={"color": "#1e293b", "fontSize": "0.75rem"}),
                rx.text(total_count,
                        style={"fontFamily": "monospace", "fontSize": "0.75rem",
                               "color": "rgba(100,116,139,0.4)"}),
                rx.text("done", style={"fontFamily": "'Rajdhani',sans-serif",
                                       "fontWeight": "600", "fontSize": "0.6rem",
                                       "color": "rgba(100,116,139,0.3)"}),
                gap="1", align="center",
            ),
            gap="1",
        ),
        rx.spacer(),
        # Progress bar
        rx.box(
            rx.box(
                style={
                    "width": pct.to_string() + "%",
                    "height": "100%",
                    "background": accent_color,
                    "transition": "width 0.4s ease",
                    "borderRadius": "9999px",
                },
            ),
            style={
                "width": "40px",
                "height": "3px",
                "background": "rgba(26,26,51,0.8)",
                "borderRadius": "9999px",
                "overflow": "hidden",
            },
        ),
        # Add button
        rx.button(
            "+ ADD",
            on_click=AppState.open_add_quest_form(mode),
            variant="ghost",
            style={
                "fontFamily": "'Orbitron',monospace",
                "fontWeight": "700",
                "fontSize": "0.48rem",
                "letterSpacing": "0.15em",
                "color": accent_color,
                "border": f"1px solid {accent_color}",
                "background": "transparent",
                "padding": "3px 8px",
                "cursor": "pointer",
                "borderRadius": "2px",
                "opacity": "0.75",
                "flexShrink": "0",
                "transition": "opacity 0.2s",
            },
        ),
        width="100%", gap="2", align="center",
    )


# ── RIFT MINI ─────────────────────────────────────────────────────────

def _rift_mini() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.box(class_name="rift-outer"),
            rx.box(class_name="rift-inner"),
            rx.box(class_name="rift-core"),
            class_name="rift-container",
            style={"width": "52px", "height": "52px", "position": "relative"},
        ),
        rx.hstack(
            rx.text(
                "🗝",
                style={
                    "fontSize": "0.7rem",
                    "filter": rx.cond(
                        AppState.instance_dungeon_key_count > 0,
                        "drop-shadow(0 0 4px rgba(255,215,0,0.8))",
                        "grayscale(1) opacity(0.3)",
                    ),
                },
            ),
            rx.text(
                AppState.instance_dungeon_key_count,
                style={
                    "fontFamily": "monospace",
                    "fontWeight": "700",
                    "fontSize": "0.82rem",
                    "color": rx.cond(
                        AppState.instance_dungeon_key_count > 0,
                        "#f5d17a",
                        "rgba(100,116,139,0.3)",
                    ),
                },
            ),
            gap="1", align="center",
        ),
        rx.text(
            "INSTANCE RIFT",
            style={
                "fontFamily": "'Rajdhani',sans-serif",
                "fontWeight": "600",
                "fontSize": "0.5rem",
                "letterSpacing": "0.12em",
                "color": rx.cond(
                    AppState.instance_dungeon_key_count > 0,
                    "rgba(255,255,255,0.35)",
                    "rgba(100,116,139,0.2)",
                ),
            },
        ),
        gap="2",
        align="center",
        style={
            "padding": "14px 10px",
            "border": "1px solid rgba(255,255,255,0.05)",
            "borderRadius": "6px",
            "background": "rgba(8,8,15,0.4)",
            "minWidth": "80px",
        },
    )


# ──────────────────────────────────────────────────────────────────────
# THREE QUEST CONTAINERS
# ──────────────────────────────────────────────────────────────────────

def _daily_container() -> rx.Component:
    """Daily quests — full-height bordered container."""
    sinful_border = rx.cond(
        AppState.perception_is_sinful,
        "1px solid rgba(239,68,68,0.3)",
        "1px solid rgba(26,26,51,0.7)",
    )
    sinful_bg = rx.cond(
        AppState.perception_is_sinful,
        "rgba(100,0,0,0.12)",
        "rgba(8,8,15,0.5)",
    )
    return rx.vstack(
        # Container header
        rx.box(
            rx.hstack(
                _quest_container_header(
                    "DAILY QUESTS",
                    AppState.completed_daily_count,
                    AppState.total_daily_count,
                    AppState.daily_progress_pct,
                    "daily",
                    "rgba(0,212,255,0.6)",
                ),
                rx.cond(
                    AppState.perception_is_sinful,
                    rx.text(
                        "SINFUL",
                        style={
                            "fontFamily": "'Orbitron',monospace",
                            "fontWeight": "900",
                            "fontSize": "0.45rem",
                            "letterSpacing": "0.2em",
                            "color": "#ef4444",
                            "border": "1px solid rgba(239,68,68,0.35)",
                            "background": "rgba(127,0,0,0.2)",
                            "padding": "2px 6px",
                            "borderRadius": "2px",
                            "animation": "intro-reveal 0.4s ease both",
                            "flexShrink": "0",
                        },
                    ),
                    rx.fragment(),
                ),
                width="100%", gap="2", align="center",
            ),
            style={
                "padding": "12px 14px",
                "borderBottom": "1px solid rgba(26,26,51,0.7)",
                "background": "rgba(0,0,0,0.3)",
            },
        ),
        # Quest list body
        rx.box(
            _add_quest_form("daily"),
            rx.cond(
                AppState.daily_quests.length() > 0,
                rx.vstack(
                    rx.foreach(AppState.daily_quests, _quest_row_daily),
                    gap="2", width="100%",
                ),
                rx.box(
                    rx.text(
                        "No daily quests yet. Complete awakening.",
                        style={
                            "fontFamily": "'Rajdhani',sans-serif",
                            "fontWeight": "500",
                            "fontSize": "0.72rem",
                            "color": "rgba(100,116,139,0.3)",
                            "textAlign": "center",
                        },
                    ),
                    style={"padding": "20px 0"},
                ),
            ),
            style={"padding": "12px 14px"},
            width="100%",
        ),
        gap="0",
        width="100%",
        style={
            "border": sinful_border,
            "borderRadius": "6px",
            "background": sinful_bg,
            "overflow": "hidden",
            "height": "100%",
        },
    )


def _weekly_container() -> rx.Component:
    """Weekly quests — full-height bordered container."""
    return rx.vstack(
        # Header
        rx.box(
            _quest_container_header(
                "WEEKLY QUESTS",
                AppState.completed_weekly_count,
                AppState.total_weekly_count,
                AppState.weekly_progress_pct,
                "weekly",
                "rgba(155,89,255,0.6)",
            ),
            style={
                "padding": "12px 14px",
                "borderBottom": "1px solid rgba(26,26,51,0.7)",
                "background": "rgba(0,0,0,0.3)",
            },
        ),
        # Body
        rx.box(
            _add_quest_form("weekly"),
            rx.vstack(
                rx.foreach(
                    AppState.weekly_quests,
                    lambda q: _quest_row_toggle(q, AppState.toggle_weekly_quest, "purple"),
                ),
                gap="2", width="100%",
            ),
            style={"padding": "12px 14px"},
            width="100%",
        ),
        gap="0",
        width="100%",
        style={
            "border": "1px solid rgba(26,26,51,0.7)",
            "borderRadius": "6px",
            "background": "rgba(8,8,15,0.5)",
            "overflow": "hidden",
            "height": "100%",
        },
    )


def _monthly_container() -> rx.Component:
    """Monthly quests + rift mini widget — full-height bordered container."""
    return rx.vstack(
        # Header
        rx.box(
            _quest_container_header(
                "MONTHLY QUESTS",
                AppState.completed_monthly_count,
                AppState.total_monthly_count,
                AppState.monthly_progress_pct,
                "monthly",
                "rgba(250,204,21,0.55)",
            ),
            style={
                "padding": "12px 14px",
                "borderBottom": "1px solid rgba(26,26,51,0.7)",
                "background": "rgba(0,0,0,0.3)",
            },
        ),
        # Body: quests + rift side by side
        rx.hstack(
            # Quest list
            rx.box(
                _add_quest_form("monthly"),
                rx.vstack(
                    rx.foreach(
                        AppState.monthly_quests,
                        lambda q: _quest_row_toggle(q, AppState.toggle_monthly_quest, "purple"),
                    ),
                    gap="2", width="100%",
                ),
                style={"padding": "12px 14px", "flex": "1"},
            ),
            # Rift widget — vertically centered in the body
            rx.box(
                _rift_mini(),
                style={
                    "padding": "12px 10px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "borderLeft": "1px solid rgba(26,26,51,0.5)",
                    "flexShrink": "0",
                },
            ),
            gap="0", align="stretch", width="100%",
        ),
        gap="0",
        width="100%",
        style={
            "border": "1px solid rgba(26,26,51,0.7)",
            "borderRadius": "6px",
            "background": "rgba(8,8,15,0.5)",
            "overflow": "hidden",
            "height": "100%",
        },
    )


# ──────────────────────────────────────────────────────────────────────
# TOP STAT ROW
# ──────────────────────────────────────────────────────────────────────

def _top_stat_row() -> rx.Component:
    return rx.flex(
        # Level + XP card
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "LEVEL",
                        style={
                            "fontFamily": "'Rajdhani',sans-serif",
                            "fontWeight": "700",
                            "fontSize": "0.6rem",
                            "letterSpacing": "0.2em",
                            "color": "rgba(0,212,255,0.5)",
                        },
                    ),
                    rx.spacer(),
                    rx.text(
                        AppState.hunter_rank,
                        class_name=AppState.rank_color_class,
                        style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                               "fontSize": "0.9rem"},
                    ),
                    width="100%",
                ),
                rx.text(
                    AppState.level,
                    style={
                        "fontFamily": "'Orbitron',monospace",
                        "fontWeight": "900",
                        "fontSize": "2.8rem",
                        "color": "#00d4ff",
                        "textShadow": "0 0 20px rgba(0,212,255,0.4)",
                        "lineHeight": "1",
                    },
                ),
                rx.box(class_name="h-2"),
                xp_bar(),
                gap="1",
            ),
            class_name="system-card p-4",
            style={"flex": "2", "minWidth": "180px"},
        ),
        # Streak
        streak_counter(),
        # Unified STATS card
        rx.box(
            rx.vstack(
                rx.text("STATS",
                        style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                               "fontSize": "0.55rem", "letterSpacing": "0.25em",
                               "color": "rgba(100,116,139,0.5)", "marginBottom": "6px"}),
                # STR — red
                rx.box(
                    rx.hstack(
                        rx.text("STR",
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "800",
                                       "fontSize": "0.55rem", "letterSpacing": "0.12em",
                                       "color": "#fff", "width": "32px"}),
                        rx.text(AppState.strength_display,
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "1rem", "color": "#fff", "flex": "1",
                                       "textAlign": "right"}),
                        gap="2", align="center", width="100%",
                    ),
                    style={"background": "rgba(239,68,68,0.18)",
                           "border": "1px solid rgba(239,68,68,0.35)",
                           "borderRadius": "4px", "padding": "6px 10px"},
                ),
                # INT — green
                rx.box(
                    rx.hstack(
                        rx.text("INT",
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "800",
                                       "fontSize": "0.55rem", "letterSpacing": "0.12em",
                                       "color": "#fff", "width": "32px"}),
                        rx.text(AppState.intelligence_display,
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "1rem", "color": "#fff", "flex": "1",
                                       "textAlign": "right"}),
                        gap="2", align="center", width="100%",
                    ),
                    style={"background": "rgba(34,197,94,0.15)",
                           "border": "1px solid rgba(34,197,94,0.3)",
                           "borderRadius": "4px", "padding": "6px 10px"},
                ),
                # PER — blue
                rx.box(
                    rx.hstack(
                        rx.text("PER",
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "800",
                                       "fontSize": "0.55rem", "letterSpacing": "0.12em",
                                       "color": "#fff", "width": "32px"}),
                        rx.text(AppState.perception_display,
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "1rem", "color": "#fff", "flex": "1",
                                       "textAlign": "right"}),
                        gap="2", align="center", width="100%",
                    ),
                    style={"background": "rgba(0,212,255,0.12)",
                           "border": "1px solid rgba(0,212,255,0.25)",
                           "borderRadius": "4px", "padding": "6px 10px"},
                ),
                gap="2", width="100%",
            ),
            class_name="system-card p-4",
            style={"flex": "1", "minWidth": "140px"},
        ),
        gap="3",
        wrap="wrap",
        width="100%",
    )


# ──────────────────────────────────────────────────────────────────────
# DEBUG PANEL
# ──────────────────────────────────────────────────────────────────────

def _debug_panel() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(
                "DEBUG",
                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                       "fontSize": "0.55rem", "letterSpacing": "0.2em",
                       "color": "rgba(100,116,139,0.25)"},
            ),
            rx.spacer(),
            rx.button(
                "RESET DAY",
                on_click=AppState.reset_daily_quests,
                variant="ghost",
                style={
                    "fontFamily": "'Orbitron',monospace",
                    "fontWeight": "700",
                    "fontSize": "0.48rem",
                    "letterSpacing": "0.15em",
                    "color": "rgba(239,68,68,0.4)",
                    "border": "1px solid rgba(239,68,68,0.15)",
                    "background": "transparent",
                    "padding": "4px 12px",
                    "cursor": "pointer",
                    "borderRadius": "2px",
                },
            ),
            width="100%", align="center",
        ),
        style={
            "padding": "8px 14px",
            "border": "1px dashed rgba(26,26,51,0.4)",
            "borderRadius": "4px",
        },
    )


# ──────────────────────────────────────────────────────────────────────
# MAIN PAGE
# ──────────────────────────────────────────────────────────────────────

def dashboard_page() -> rx.Component:
    return rx.box(
        system_nav(),
        quest_verify_overlay(),
        penalty_dialog(),
        key_popup(),

        rx.box(
            rx.vstack(
                # Stat cards row
                _top_stat_row(),

                # Quest containers grid — equal-width, contained columns
                rx.grid(
                    _daily_container(),
                    _weekly_container(),
                    _monthly_container(),
                    columns=rx.breakpoints(initial="1", md="3"),
                    gap="4",
                    width="100%",
                    style={"alignItems": "start"},
                ),

                _debug_panel(),

                gap="4",
                width="100%",
            ),
            class_name="pt-20 px-4 md:px-8 pb-12 max-w-7xl mx-auto",
        ),

        class_name="min-h-screen",
        style={
            "background": (
                "radial-gradient(ellipse at 30% 20%, rgba(0,212,255,0.04) 0%, transparent 50%),"
                "radial-gradient(ellipse at 80% 70%, rgba(155,89,255,0.03) 0%, transparent 50%),"
                "#020205"
            )
        },
    )
