"""
pages/dashboard.py — Main quest tracking screen.
"""
import reflex as rx
from solo_leveling_app.state import AppState, QuestItem
from solo_leveling_app.components.system_ui import (
    system_nav, xp_bar, streak_counter, stat_card,
    quest_type_badge, penalty_dialog,
)


def _quest_row(quest: QuestItem, on_toggle) -> rx.Component:
    """Single quest row with checkbox, title, type badge, and XP."""
    return rx.box(
        rx.hstack(
            # Checkbox
            rx.box(
                rx.cond(
                    quest["done"],
                    rx.text("✓", class_name="text-[11px] font-black text-system-black"),
                    rx.fragment(),
                ),
                on_click=on_toggle(quest["id"]),
                class_name=rx.cond(
                    quest["done"],
                    "w-5 h-5 rounded-sm bg-neon-blue flex items-center justify-center "
                    "cursor-pointer flex-shrink-0",
                    "w-5 h-5 rounded-sm border border-slate-700 flex items-center justify-center "
                    "cursor-pointer flex-shrink-0 hover:border-neon-blue/50 transition-colors",
                ),
            ),
            # Info
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
                # XP — use .to_string() since quest["xp"] is a Reflex Var
                rx.text(
                    "+" + quest["xp"].to_string() + " XP",
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


def _quest_section(
    title: str,
    dot_cls: str,
    quests,
    on_toggle,
    completed,
    total,
    pct_var,
) -> rx.Component:
    """
    pct_var must be a pre-computed rx.Var[int] (0-100) from AppState.
    We cannot evaluate Python if/else on Reflex Var objects at compile time.
    """
    return rx.vstack(
        # Header
        rx.hstack(
            rx.hstack(
                rx.box(class_name=f"w-2 h-2 rounded-full {dot_cls} bg-current flex-shrink-0"),
                rx.text(title, class_name="system-font text-xs tracking-widest text-slate-300"),
                gap="2", align="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.text(completed, class_name="text-xs font-mono text-slate-400"),
                rx.text("/", class_name="text-xs text-slate-700"),
                rx.text(total, class_name="text-xs font-mono text-slate-600"),
                gap="0.5",
            ),
            width="100%",
        ),
        # Thin progress bar — width driven by pre-computed Var
        rx.box(
            rx.box(
                style={
                    "width": pct_var.to_string() + "%",
                    "background": "linear-gradient(90deg,rgba(0,212,255,0.6),rgba(155,89,255,0.6))",
                    "transition": "width 0.4s ease",
                    "height": "100%",
                    "borderRadius": "9999px",
                },
            ),
            class_name="w-full h-0.5 bg-system-border rounded-full overflow-hidden",
        ),
        # Quest rows
        rx.vstack(
            rx.foreach(quests, lambda q: _quest_row(q, on_toggle)),
            gap="2", width="100%",
        ),
        gap="3", width="100%",
    )


def verification_panel() -> rx.Component:
    """Verification Engine — submit LeetCode / GitHub proof."""
    return rx.box(
        rx.vstack(
            rx.text("[ VERIFICATION ENGINE ]",
                    class_name="system-font text-xs tracking-widest neon-text-purple mb-1"),
            rx.text("Submit proof of completion for your DSA Quest.",
                    class_name="text-slate-500 text-xs mb-3"),
            rx.hstack(
                rx.input(
                    placeholder="https://leetcode.com/submissions/detail/...",
                    value=AppState.verification_url,
                    on_change=AppState.set_verification_url,
                    class_name="system-input flex-1",
                ),
                rx.button(
                    "SUBMIT",
                    on_click=AppState.submit_verification("d2"),
                    class_name="system-button text-xs px-4 flex-shrink-0",
                ),
                gap="2", width="100%",
            ),
            rx.cond(
                AppState.verification_message != "",
                rx.text(
                    AppState.verification_message,
                    class_name=rx.cond(
                        AppState.verification_message.contains("ERROR"),
                        "text-xs text-red-500 font-mono mt-1",
                        "text-xs text-green-400 font-mono mt-1",
                    ),
                ),
                rx.fragment(),
            ),
            gap="1", width="100%",
        ),
        class_name="system-card p-4 border-neon-purple/20",
    )


def penalty_triggers() -> rx.Component:
    """Debug panel: manually fire penalty dialogs for demo."""
    return rx.box(
        rx.vstack(
            rx.text("[ SIMULATE FAILURE — DEMO ]",
                    class_name="system-font text-[10px] tracking-widest text-slate-700 mb-2"),
            rx.hstack(
                rx.button(
                    "B-RANK PENALTY",
                    on_click=AppState.trigger_penalty("B", "Daily Push-ups"),
                    class_name=(
                        "text-[10px] px-3 py-1.5 border border-red-900/40 text-red-700 "
                        "hover:text-red-400 hover:border-red-700/50 transition-colors "
                        "rounded-sm system-font tracking-widest"
                    ),
                    variant="ghost",
                ),
                rx.button(
                    "A-RANK PENALTY",
                    on_click=AppState.trigger_penalty("A", "Weekly LeetCode Target"),
                    class_name=(
                        "text-[10px] px-3 py-1.5 border border-red-900/40 text-red-700 "
                        "hover:text-red-400 hover:border-red-700/50 transition-colors "
                        "rounded-sm system-font tracking-widest"
                    ),
                    variant="ghost",
                ),
                rx.button(
                    "S-RANK PENALTY",
                    on_click=AppState.trigger_penalty("S", "Monthly Project Ship"),
                    class_name=(
                        "text-[10px] px-3 py-1.5 border border-red-900/40 text-red-700 "
                        "hover:text-red-400 hover:border-red-700/50 transition-colors "
                        "rounded-sm system-font tracking-widest"
                    ),
                    variant="ghost",
                ),
                gap="2", flex_wrap="wrap",
            ),
            gap="1", width="100%",
        ),
        class_name="p-3 border border-dashed border-red-900/20 rounded-sm",
    )


def dashboard_page() -> rx.Component:
    return rx.box(
        penalty_dialog(),
        system_nav(),
        rx.box(
            rx.vstack(
                # Stat row
                rx.hstack(
                    stat_card("TOTAL XP",  AppState.total_xp,    "experience points", "blue"),
                    stat_card("LEVEL",      AppState.level,       "hunter level",      "purple"),
                    streak_counter(),
                    stat_card("RANK",       AppState.hunter_rank, "classification",    "gold"),
                    gap="3", width="100%", flex_wrap="wrap",
                ),

                # XP bar
                rx.box(xp_bar(), class_name="system-card p-4 w-full"),

                # Quest columns
                rx.grid(
                    _quest_section(
                        "DAILY QUESTS", "text-blue-400",
                        AppState.daily_quests, AppState.toggle_daily_quest,
                        AppState.completed_daily_count, AppState.total_daily_count,
                        AppState.daily_progress_pct,
                    ),
                    _quest_section(
                        "WEEKLY QUESTS", "text-purple-400",
                        AppState.weekly_quests, AppState.toggle_weekly_quest,
                        AppState.completed_weekly_count, AppState.total_weekly_count,
                        AppState.weekly_progress_pct,
                    ),
                    _quest_section(
                        "MONTHLY QUESTS", "text-yellow-400",
                        AppState.monthly_quests, AppState.toggle_monthly_quest,
                        AppState.completed_monthly_count, AppState.total_monthly_count,
                        AppState.monthly_progress_pct,
                    ),
                    columns=rx.breakpoints(initial="1", md="3"),
                    gap="4", width="100%",
                ),

                # Verification
                verification_panel(),

                # Demo penalty triggers
                penalty_triggers(),

                gap="4", width="100%",
            ),
            class_name="pt-20 px-4 md:px-8 pb-12 max-w-7xl mx-auto",
        ),
        class_name="min-h-screen portal-bg",
    )
