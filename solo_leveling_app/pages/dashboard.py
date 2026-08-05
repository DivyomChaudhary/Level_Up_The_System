"""
pages/dashboard.py — Phase 3 (restored).
Quest layout, stat cards, rift spinner, penalty dialog, verify overlay.
"""
import reflex as rx
from solo_leveling_app.state import AppState, QuestItem
from solo_leveling_app.components.system_ui import (
    system_nav, xp_bar, streak_counter, stat_card,
    quest_type_badge, penalty_dialog, quest_verify_overlay, key_popup,
)


# ─── QUEST ROWS ───────────────────────────────────────────────────────

def _quest_row_daily(quest: QuestItem) -> rx.Component:
    """Daily quest — checkbox opens verify popup or uncompletes."""
    return rx.box(
        rx.hstack(
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
                    "w-5 h-5 rounded-sm border border-slate-700 flex items-center justify-center "
                    "cursor-pointer flex-shrink-0 hover:border-neon-blue/50 transition-colors",
                ),
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        quest["title"],
                        class_name=rx.cond(
                            quest["done"],
                            "text-sm text-slate-600 line-through",
                            "text-sm text-slate-200",
                        ),
                    ),
                    rx.spacer(),
                    quest_type_badge(quest["type"]),
                    align="center", width="100%",
                ),
                rx.text(
                    "+100 XP",
                    class_name="text-[10px] neon-text-blue font-mono",
                ),
                gap="0.5", width="100%",
            ),
            gap="3", align="center", width="100%",
        ),
        class_name=rx.cond(
            quest["done"],
            "system-card p-3 md:p-4 opacity-50 transition-all duration-300",
            "system-card p-3 md:p-4 hover:border-neon-blue/20 transition-all duration-300 cursor-pointer",
        ),
    )


def _quest_row_other(quest: QuestItem, on_toggle, xp_label: str) -> rx.Component:
    """Weekly or monthly quest toggle row."""
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
                    "w-5 h-5 rounded-sm bg-neon-purple flex items-center justify-center cursor-pointer flex-shrink-0",
                    "w-5 h-5 rounded-sm border border-slate-700 flex items-center justify-center "
                    "cursor-pointer flex-shrink-0 hover:border-neon-purple/50 transition-colors",
                ),
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        quest["title"],
                        class_name=rx.cond(
                            quest["done"],
                            "text-sm text-slate-600 line-through",
                            "text-sm text-slate-300",
                        ),
                    ),
                    rx.spacer(),
                    quest_type_badge(quest["type"]),
                    align="center", width="100%",
                ),
                rx.text(xp_label, class_name="text-[10px] neon-text-purple font-mono"),
                gap="0.5", width="100%",
            ),
            gap="3", align="center", width="100%",
        ),
        class_name=rx.cond(
            quest["done"],
            "system-card p-3 md:p-4 opacity-50 transition-all duration-300",
            "system-card p-3 md:p-4 hover:border-neon-purple/20 transition-all duration-300 cursor-pointer",
        ),
    )


# ─── ADD QUEST FORM ───────────────────────────────────────────────────

def _add_quest_form(mode: str) -> rx.Component:
    return rx.cond(
        AppState.add_quest_mode == mode,
        rx.box(
            rx.vstack(
                rx.input(
                    placeholder="Quest title...",
                    value=AppState.new_add_quest_title,
                    on_change=AppState.set_new_add_quest_title,
                    class_name="system-input w-full",
                    style={"fontSize": "0.82rem"},
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
                            "fontSize": "0.78rem",
                            "padding": "6px 12px",
                            "borderRadius": "2px",
                            "flex": "1",
                        },
                    ),
                    rx.button(
                        "ADD",
                        on_click=AppState.submit_add_quest,
                        class_name="system-button text-xs",
                        style={"padding": "8px 20px", "flexShrink": "0"},
                    ),
                    rx.button(
                        "✕",
                        on_click=AppState.close_add_quest_form,
                        variant="ghost",
                        style={"color": "rgba(100,116,139,0.4)", "cursor": "pointer",
                               "fontSize": "0.85rem", "flexShrink": "0"},
                    ),
                    gap="2", align="center", width="100%",
                ),
                gap="2", width="100%",
            ),
            class_name="quest-add-form",
        ),
        rx.fragment(),
    )


# ─── SECTION HEADERS ──────────────────────────────────────────────────

def _section_header(title: str, done_count, total_count, pct, mode: str,
                    accent_class: str = "neon-text-blue") -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(title, class_name=f"system-font text-[10px] tracking-widest {accent_class}"),
            rx.hstack(
                rx.text(done_count, class_name="font-mono text-xs neon-text-blue font-bold"),
                rx.text("/", class_name="text-slate-800 text-xs"),
                rx.text(total_count, class_name="font-mono text-xs text-slate-600"),
                rx.text("COMPLETE", class_name="text-[9px] tracking-wider text-slate-700"),
                gap="1", align="center",
            ),
            gap="0",
        ),
        rx.spacer(),
        rx.box(
            rx.box(
                style={"width": pct.to_string() + "%", "height": "100%",
                       "background": "var(--color-neon-blue)", "transition": "width 0.4s ease",
                       "borderRadius": "9999px"},
            ),
            class_name="w-12 h-0.5 bg-system-border rounded-full overflow-hidden",
        ),
        rx.button(
            "+ ADD",
            on_click=AppState.open_add_quest_form(mode),
            class_name="system-font text-[9px] tracking-widest neon-text-blue "
                        "border border-neon-blue/30 px-2 py-1 rounded-sm cursor-pointer "
                        "hover:bg-neon-blue/5 transition-colors flex-shrink-0",
            variant="ghost",
        ),
        width="100%", gap="2", align="center",
    )


# ─── RIFT SPINNER ─────────────────────────────────────────────────────

def _rift_spinner() -> rx.Component:
    """Compact rift spinner beside monthly quests."""
    return rx.vstack(
        rx.box(
            rx.box(class_name="rift-outer"),
            rx.box(class_name="rift-inner"),
            rx.box(class_name="rift-core"),
            class_name="rift-container",
            style={"width": "60px", "height": "60px", "position": "relative"},
        ),
        rx.hstack(
            rx.text("🗝",
                    style={"fontSize": "0.75rem",
                           "filter": rx.cond(
                               AppState.instance_dungeon_key_count > 0,
                               "drop-shadow(0 0 4px rgba(255,215,0,0.8))",
                               "grayscale(1) opacity(0.3)",
                           )}),
            rx.text(AppState.instance_dungeon_key_count,
                    style={"fontFamily": "monospace", "fontWeight": "700",
                           "fontSize": "0.9rem",
                           "color": rx.cond(AppState.instance_dungeon_key_count > 0,
                                            "#f5d17a", "rgba(100,116,139,0.3)")}),
            gap="1", align="center",
        ),
        rx.text("INSTANCE RIFT",
                class_name="text-[8px] tracking-widest",
                style={"color": rx.cond(AppState.instance_dungeon_key_count > 0,
                                        "rgba(255,255,255,0.4)",
                                        "rgba(100,116,139,0.2)")}),
        gap="2",
        align="center",
        class_name="rift-mini",
        style={"minHeight": "140px"},
    )


# ─── DAILY QUESTS SECTION ─────────────────────────────────────────────

def _daily_section() -> rx.Component:
    sinful_style = rx.cond(
        AppState.perception_is_sinful,
        {"background": "linear-gradient(135deg,rgba(100,0,0,0.25),rgba(15,0,0,0.4))",
         "border": "1px solid rgba(239,68,68,0.2)", "borderRadius": "6px", "padding": "16px"},
        {"padding": "0"},
    )
    return rx.box(
        rx.vstack(
            rx.hstack(
                _section_header("DAILY QUESTS",
                                AppState.completed_daily_count, AppState.total_daily_count,
                                AppState.daily_progress_pct, "daily"),
                rx.cond(
                    AppState.perception_is_sinful,
                    rx.text("SINFUL",
                            class_name="system-font text-[8px] tracking-widest text-red-500 "
                                       "border border-red-800/40 bg-red-900/20 px-2 py-0.5 "
                                       "rounded-sm animate-pulse"),
                    rx.fragment(),
                ),
                width="100%", gap="2", align="center",
            ),
            _add_quest_form("daily"),
            rx.cond(
                AppState.daily_quests.length() > 0,
                rx.vstack(rx.foreach(AppState.daily_quests, _quest_row_daily), gap="2", width="100%"),
                rx.box(
                    rx.text("No daily quests. Complete awakening to populate.",
                            class_name="text-slate-600 text-xs text-center"),
                    class_name="system-card p-6",
                ),
            ),
            gap="3", width="100%",
        ),
        style=sinful_style,
    )


# ─── WEEKLY SECTION ───────────────────────────────────────────────────

def _weekly_section() -> rx.Component:
    return rx.vstack(
        _section_header("WEEKLY QUESTS",
                        AppState.completed_weekly_count, AppState.total_weekly_count,
                        AppState.weekly_progress_pct, "weekly", "neon-text-purple"),
        _add_quest_form("weekly"),
        rx.foreach(
            AppState.weekly_quests,
            lambda q: _quest_row_other(q, AppState.toggle_weekly_quest, "+500 XP"),
        ),
        gap="3", width="100%",
    )


# ─── MONTHLY SECTION + RIFT ───────────────────────────────────────────

def _monthly_section() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            _section_header("MONTHLY QUESTS",
                            AppState.completed_monthly_count, AppState.total_monthly_count,
                            AppState.monthly_progress_pct, "monthly", "text-yellow-600"),
            _add_quest_form("monthly"),
            rx.foreach(
                AppState.monthly_quests,
                lambda q: _quest_row_other(q, AppState.toggle_monthly_quest, "+2000 XP"),
            ),
            gap="3", width="100%", flex="1",
        ),
        _rift_spinner(),
        gap="4", width="100%", align="start",
    )


# ─── TOP STAT ROW ─────────────────────────────────────────────────────

def _top_stat_row() -> rx.Component:
    """XP bar + streak + stat cards in a single responsive row."""
    return rx.flex(
        # XP + Level card
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("LEVEL",
                            class_name="system-font text-[10px] tracking-widest neon-text-blue opacity-60"),
                    rx.spacer(),
                    rx.text(AppState.hunter_rank,
                            class_name=f"system-font text-lg font-black {AppState.rank_color_class}"),
                    width="100%",
                ),
                rx.text(
                    AppState.level,
                    class_name="system-font text-4xl font-black neon-text-blue",
                    style={"textShadow": "0 0 20px rgba(0,212,255,0.4)", "lineHeight": "1"},
                ),
                rx.box(class_name="h-2"),
                xp_bar(),
                gap="1",
            ),
            class_name="system-card p-4 flex-1 min-w-[180px]",
        ),
        # Streak card
        streak_counter(),
        # Stat cards
        stat_card("STR", AppState.strength_display, AppState.strength_pct,
                  "rgba(239,68,68,0.7)", AppState.missed_strength_days),
        stat_card("INT", AppState.intelligence_display, AppState.intelligence_pct,
                  "var(--color-neon-blue)", AppState.missed_intelligence_days),
        stat_card("PER", AppState.perception_display, AppState.perception_pct,
                  "var(--color-neon-purple)", AppState.missed_perception_days),
        gap="3",
        wrap="wrap",
        width="100%",
    )


# ─── DEBUG PANEL ──────────────────────────────────────────────────────

def _debug_panel() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("DEBUG",
                    class_name="system-font text-[9px] tracking-widest text-slate-700"),
            rx.spacer(),
            rx.button(
                "RESET DAY",
                on_click=AppState.reset_daily_quests,
                class_name="system-font text-[9px] tracking-widest text-red-700 "
                           "border border-red-900/30 px-3 py-1 rounded-sm cursor-pointer "
                           "hover:bg-red-900/10 transition-colors",
                variant="ghost",
            ),
            width="100%", align="center",
        ),
        class_name="border border-dashed border-slate-800/50 rounded px-4 py-2",
    )


# ─── MAIN PAGE ────────────────────────────────────────────────────────

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

                rx.box(class_name="h-1"),

                # Quest columns
                rx.grid(
                    _daily_section(),
                    _weekly_section(),
                    _monthly_section(),
                    columns=rx.breakpoints(initial="1", md="3"),
                    gap="4",
                    width="100%",
                ),

                rx.box(class_name="h-4"),
                _debug_panel(),

                gap="4", width="100%",
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
