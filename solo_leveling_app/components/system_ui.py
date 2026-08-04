"""
components/system_ui.py
Reusable UI primitives: Sidebar, SystemAlerts, StatCards, badges, XP bar.
All components import from solo_leveling_app.state.
"""
import reflex as rx
from solo_leveling_app.state import AppState, QuestItem


def _quest_type_color(quest_type) -> str:
    """rx.match-based color picker — safe for use with Reflex Var values."""
    return rx.match(
        quest_type,
        ("FITNESS", "#f97316"),
        ("DSA",     "#22d3ee"),
        ("DEV",     "#a78bfa"),
        "#94a3b8",
    )


def _rank_hex(rank) -> str:
    return rx.match(
        rank,
        ("S", "#ffd700"),
        ("A", "#c084fc"),
        ("B", "#60a5fa"),
        ("C", "#4ade80"),
        ("D", "#94a3b8"),
        "#6b7280",
    )


# ─── BADGE COMPONENTS ───

def rank_badge(rank: str, size: str = "sm") -> rx.Component:
    """Static rank badge — only used where rank is a known Python string (not a Var)."""
    size_cls = "text-xs px-2 py-0.5" if size == "sm" else "text-sm px-3 py-1 font-black"
    return rx.box(
        rx.text(rank, class_name=f"{size_cls} system-font font-bold"),
        class_name=f"border rounded-sm inline-flex items-center rank-{rank.lower()} border-current/30 bg-current/5",
    )


def quest_type_badge(quest_type) -> rx.Component:
    """Var-safe type badge using rx.match for color — works inside rx.foreach."""
    col = _quest_type_color(quest_type)
    return rx.box(
        rx.text(
            quest_type,
            style={"color": col, "fontSize": "0.625rem",
                   "letterSpacing": "0.1em", "fontWeight": "600"},
        ),
        style={
            "border": f"1px solid color-mix(in srgb, {col} 30%, transparent)",
            "backgroundColor": f"color-mix(in srgb, {col} 10%, transparent)",
            "padding": "2px 8px", "borderRadius": "2px",
            "display": "inline-flex", "alignItems": "center",
        },
    )


# ─── NAVIGATION BAR ───

def system_nav() -> rx.Component:
    """Fixed top navigation bar with page links and hunter summary."""
    nav_items = [
        ("DASHBOARD",   "dashboard"),
        ("DUNGEONS",    "gates"),
        ("LEADERBOARD", "leaderboard"),
    ]
    return rx.box(
        rx.hstack(
            # Logo
            rx.hstack(
                rx.text("⚡", class_name="text-xl"),
                rx.text(
                    "THE SYSTEM",
                    class_name="system-font text-sm tracking-[0.3em] neon-text-blue hidden sm:block",
                ),
                gap="2",
                align="center",
            ),
            rx.spacer(),
            # Nav links
            rx.hstack(
                *[
                    rx.button(
                        label,
                        on_click=AppState.navigate_to(page),
                        class_name=rx.cond(
                            AppState.active_page == page,
                            "system-font text-xs tracking-widest neon-text-blue "
                            "bg-neon-blue/10 border border-neon-blue/30 px-3 py-1.5 rounded-sm cursor-pointer",
                            "system-font text-xs tracking-widest text-slate-500 "
                            "hover:text-slate-300 px-3 py-1.5 transition-colors cursor-pointer",
                        ),
                        variant="ghost",
                    )
                    for label, page in nav_items
                ],
                gap="1",
            ),
            rx.spacer(),
            # Hunter summary
            rx.hstack(
                rx.vstack(
                    rx.text(AppState.user_name, class_name="text-xs font-medium text-right"),
                    rx.hstack(
                        rx.text("LVL", class_name="text-[10px] text-slate-600"),
                        rx.text(AppState.level,        class_name="text-[10px] neon-text-blue font-bold"),
                        rx.text("•",                   class_name="text-slate-700"),
                        rx.text(AppState.hunter_rank,  class_name=f"text-[10px] font-bold"),
                        gap="1",
                        align="center",
                    ),
                    gap="0",
                    align="end",
                ),
                rx.box(
                    rx.text(AppState.hunter_rank, class_name="system-font text-sm font-bold"),
                    class_name=f"w-8 h-8 rounded-full border-2 border-current flex items-center justify-center {AppState.rank_color_class}",
                ),
                gap="2",
                align="center",
            ),
            align="center",
            width="100%",
        ),
        class_name=(
            "fixed top-0 left-0 right-0 z-50 px-4 md:px-8 py-3 "
            "border-b border-system-border bg-system-dark/95 backdrop-blur-md"
        ),
    )


# ─── XP BAR ───

def xp_bar() -> rx.Component:
    """Horizontal XP progress bar with label."""
    return rx.vstack(
        rx.hstack(
            rx.text("XP", class_name="text-[10px] text-slate-600 tracking-widest"),
            rx.text(AppState.total_xp,   class_name="text-[10px] neon-text-blue font-mono"),
            rx.text("/",                 class_name="text-slate-700 text-[10px]"),
            rx.text(AppState.xp_to_next, class_name="text-[10px] text-slate-600 font-mono"),
            justify="between",
            width="100%",
        ),
        rx.box(
            rx.box(
                style={
                    "width": f"{AppState.xp_progress_pct}%",
                    "background": "linear-gradient(90deg, #00d4ff, #9b59ff)",
                    "boxShadow": "0 0 8px rgba(0,212,255,0.5)",
                    "transition": "width 0.5s ease",
                    "height": "100%",
                    "borderRadius": "9999px",
                },
            ),
            class_name="w-full h-1.5 bg-system-border rounded-full overflow-hidden",
        ),
        gap="1",
        width="100%",
    )


# ─── STREAK COUNTER ───

def streak_counter() -> rx.Component:
    """Glowing streak card."""
    return rx.box(
        rx.vstack(
            rx.text("🔥", class_name="text-3xl"),
            rx.text(AppState.streak, class_name="system-font text-4xl font-black neon-text-blue"),
            rx.text("DAY STREAK", class_name="text-[10px] tracking-[0.3em] text-slate-500"),
            align="center",
            gap="1",
        ),
        class_name="system-card p-6 text-center neon-blue-glow",
    )


# ─── STAT CARD ───

def stat_card(
    label: str,
    value,
    sub: str = "",
    accent: str = "blue",
) -> rx.Component:
    accent_map = {
        "blue":   "neon-text-blue",
        "purple": "neon-text-purple",
        "gold":   "text-yellow-400",
        "green":  "text-green-400",
    }
    return rx.box(
        rx.vstack(
            rx.text(label, class_name="text-[10px] tracking-widest text-slate-600"),
            rx.text(value, class_name=f"system-font text-2xl font-bold {accent_map.get(accent, 'neon-text-blue')}"),
            rx.cond(
                sub != "",
                rx.text(sub, class_name="text-[10px] text-slate-600"),
                rx.fragment(),
            ),
            gap="0.5",
            align="center",
        ),
        class_name="system-card p-4 text-center flex-1 min-w-[100px]",
    )


# ─── SYSTEM ALERT (PENALTY) DIALOG ───

def penalty_dialog() -> rx.Component:
    """Full-screen penalty overlay dialog."""
    return rx.cond(
        AppState.penalty_active,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.vstack(
                        rx.text(
                            "⚠ SYSTEM ALERT ⚠",
                            class_name="system-font text-red-500 text-sm tracking-[0.4em] animate-pulse",
                        ),
                        rx.text(
                            rx.cond(
                                AppState.penalty_rank == "S",
                                "S-RANK PENALTY PROTOCOL",
                                rx.cond(
                                    AppState.penalty_rank == "A",
                                    "A-RANK PENALTY QUEST",
                                    "B-RANK PENALTY QUEST",
                                ),
                            ),
                            class_name="system-font text-xl font-black text-white tracking-widest mt-1",
                        ),
                        align="center",
                        gap="1",
                    ),
                    rx.box(class_name="w-full h-px bg-gradient-to-r from-transparent via-red-800/50 to-transparent"),
                    # Message
                    rx.box(
                        rx.text(
                            AppState.penalty_message,
                            class_name="text-xs text-red-300 font-mono leading-relaxed text-center",
                        ),
                        class_name="p-4 bg-red-950/20 border border-red-900/30 rounded-sm w-full",
                    ),
                    # Assigned quest
                    rx.box(
                        rx.vstack(
                            rx.text("PENALTY QUEST ASSIGNED:", class_name="text-[10px] text-slate-500 tracking-widest"),
                            rx.cond(
                                AppState.penalty_rank == "S",
                                rx.text(
                                    "COMPLETE ENTIRE MONTH'S QUOTA IN ONE WEEK. No exceptions.",
                                    class_name="text-sm text-yellow-400 font-bold",
                                ),
                                rx.cond(
                                    AppState.penalty_rank == "A",
                                    rx.text(
                                        "Solve 5 Medium LeetCode problems before this week ends.",
                                        class_name="text-sm text-purple-400 font-medium",
                                    ),
                                    rx.text(
                                        "200 Push-ups + 200 Squats within 24 hours.",
                                        class_name="text-sm text-blue-400 font-medium",
                                    ),
                                ),
                            ),
                            gap="1",
                        ),
                        class_name="w-full p-3 border border-dashed border-red-800/40 rounded-sm",
                    ),
                    rx.button(
                        "I UNDERSTAND. PROCEEDING.",
                        on_click=AppState.dismiss_penalty,
                        class_name="system-button system-button-danger w-full tracking-widest",
                    ),
                    gap="4",
                    width="100%",
                    align="center",
                ),
                class_name="system-card p-8 max-w-lg w-full mx-4 border-red-900/30",
                style={"boxShadow": "0 0 60px rgba(239,68,68,0.25), 0 0 120px rgba(239,68,68,0.08)"},
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm",
        ),
        rx.fragment(),
    )
