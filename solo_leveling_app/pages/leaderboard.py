"""
pages/leaderboard.py — S-Rank to D-Rank Hunter mock data with rx.hover_card.

NOTE: hunter["rank"] is a Reflex Var inside rx.foreach.
      We use rx.match() for all rank-based styling — no .lower() calls.
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


def _rank_border(rank) -> str:
    return rx.match(
        rank,
        ("S", "rgba(255,215,0,0.3)"),
        ("A", "rgba(192,132,252,0.3)"),
        ("B", "rgba(96,165,250,0.3)"),
        ("C", "rgba(74,222,128,0.25)"),
        ("D", "rgba(148,163,184,0.2)"),
        "rgba(107,114,128,0.2)",
    )


def _row_hover_bg(rank) -> str:
    return rx.match(
        rank,
        ("S", "rgba(255,215,0,0.04)"),
        ("A", "rgba(192,132,252,0.04)"),
        ("B", "rgba(96,165,250,0.04)"),
        "rgba(255,255,255,0.02)",
    )


def hunter_row(hunter: HunterEntry) -> rx.Component:
    rank     = hunter["rank"]
    pos      = hunter["pos"]
    rank_col = _rank_color(rank)
    bdr_col  = _rank_border(rank)

    pos_icon = rx.cond(
        pos == 1,
        rx.text("👑", class_name="text-base"),
        rx.cond(
            pos <= 3,
            rx.text("⚔", class_name="text-sm"),
            rx.text(pos, class_name="text-xs text-slate-600 font-mono"),
        ),
    )

    return rx.hover_card.root(
        rx.hover_card.trigger(
            rx.box(
                rx.hstack(
                    rx.box(pos_icon, class_name="w-8 text-center flex-shrink-0"),
                    # Rank badge
                    rx.box(
                        rx.text(
                            rank,
                            style={"color": rank_col,
                                   "fontFamily": "'Orbitron',monospace",
                                   "fontSize": "0.75rem", "fontWeight": "800"},
                        ),
                        style={
                            "width": "1.75rem", "height": "1.75rem",
                            "border": f"1px solid {bdr_col}",
                            "backgroundColor": f"color-mix(in srgb, {rank_col} 6%, transparent)",
                            "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "borderRadius": "2px",
                            "flexShrink": "0",
                        },
                    ),
                    rx.text(
                        hunter["name"],
                        class_name=rx.cond(
                            rank == "S",
                            "text-sm font-medium text-slate-100",
                            "text-sm text-slate-300",
                        ),
                    ),
                    rx.spacer(),
                    rx.text(hunter["region"],
                            class_name="text-[10px] text-slate-600 hidden sm:block"),
                    rx.text("ℹ",
                            class_name="text-[10px] text-slate-700 hover:text-neon-blue transition-colors ml-2"),
                    gap="3", align="center", width="100%",
                ),
                style={"transition": "background 0.2s"},
                class_name="p-3 border-b border-system-border hover:bg-white/[0.03] cursor-pointer",
            ),
        ),
        rx.hover_card.content(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text(
                            rank,
                            style={"color": rank_col,
                                   "fontFamily": "'Orbitron',monospace",
                                   "fontSize": "0.875rem", "fontWeight": "800"},
                        ),
                        style={
                            "width": "2.25rem", "height": "2.25rem",
                            "border": f"1px solid {bdr_col}",
                            "backgroundColor": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                            "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "borderRadius": "2px",
                            "flexShrink": "0",
                        },
                    ),
                    rx.vstack(
                        rx.text(hunter["name"], class_name="text-sm font-semibold text-white"),
                        rx.text(
                            rx.fragment("Rank ", rank, " Hunter"),
                            style={"color": rank_col,
                                   "fontSize": "0.625rem", "letterSpacing": "0.15em"},
                        ),
                        gap="0",
                    ),
                    gap="2", align="center",
                ),
                rx.box(class_name="w-full h-px bg-system-border"),
                rx.text(hunter["info"], class_name="text-xs text-slate-400 leading-relaxed"),
                rx.hstack(
                    rx.text("REGION:", class_name="text-[10px] text-slate-600 tracking-wider"),
                    rx.text(hunter["region"], class_name="text-[10px] text-slate-400"),
                    gap="2",
                ),
                gap="3", align="start",
            ),
            class_name="system-card p-4 min-w-[220px] max-w-[300px]",
            style={
                "background": "rgba(8,8,15,0.98)",
                "border": "1px solid rgba(155,89,255,0.35)",
                "boxShadow": "0 0 25px rgba(155,89,255,0.2)",
            },
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
                            class_name="system-font text-[10px] tracking-widest text-slate-600"),
                    rx.text("Leaderboard",
                            class_name="system-font text-2xl font-black text-white tracking-wider"),
                    rx.text("Registered hunters, ranked by classification. Hover for intel.",
                            class_name="text-slate-500 text-sm"),
                    gap="1", class_name="mb-6",
                ),

                # Your card
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("YOUR STATUS",
                                    class_name="text-[10px] tracking-widest text-slate-600"),
                            rx.text(AppState.user_name,
                                    class_name="text-sm font-semibold text-white"),
                            rx.text("HUNTER IN TRAINING",
                                    class_name="text-[10px] text-slate-500 tracking-wider"),
                            gap="0.5",
                        ),
                        rx.spacer(),
                        rx.vstack(
                            rx.text("RANK",
                                    class_name="text-[10px] text-slate-600 tracking-wider"),
                            rx.text(
                                AppState.hunter_rank,
                                class_name=f"system-font text-3xl font-black {AppState.rank_color_class}",
                            ),
                            gap="0", align="center",
                        ),
                        rx.vstack(
                            rx.text("LEVEL",
                                    class_name="text-[10px] text-slate-600 tracking-wider"),
                            rx.text(AppState.level,
                                    class_name="system-font text-3xl font-black neon-text-blue"),
                            gap="0", align="center",
                        ),
                        rx.vstack(
                            rx.text("STREAK",
                                    class_name="text-[10px] text-slate-600 tracking-wider"),
                            rx.hstack(
                                rx.text("🔥", class_name="text-xl"),
                                rx.text(AppState.streak,
                                        class_name="system-font text-2xl font-black text-orange-400"),
                                gap="1", align="center",
                            ),
                            gap="0", align="center",
                        ),
                        gap="5", align="center", width="100%",
                    ),
                    class_name="system-card p-5 border-neon-purple/25 mb-4",
                    style={"boxShadow": "0 0 25px rgba(155,89,255,0.08)"},
                ),

                # Leaderboard table
                rx.box(
                    # Header row
                    rx.box(
                        rx.hstack(
                            rx.text("#",      class_name="text-[10px] tracking-widest text-slate-600 w-8"),
                            rx.text("RANK",   class_name="text-[10px] tracking-widest text-slate-600 w-7"),
                            rx.text("HUNTER", class_name="text-[10px] tracking-widest text-slate-600"),
                            rx.spacer(),
                            rx.text("REGION", class_name="text-[10px] tracking-widest text-slate-600 hidden sm:block"),
                            rx.text("INFO",   class_name="text-[10px] tracking-widest text-slate-600 ml-2"),
                            gap="3", align="center", width="100%",
                        ),
                        class_name="px-3 py-2 border-b border-system-border bg-system-card/50",
                    ),
                    # Hunter rows
                    rx.vstack(
                        rx.foreach(AppState.leaderboard, hunter_row),
                        gap="0", width="100%",
                    ),
                    class_name="system-card overflow-hidden",
                ),
                gap="0", width="100%",
            ),
            class_name="pt-20 px-4 md:px-8 pb-12 max-w-3xl mx-auto",
        ),
        class_name="min-h-screen portal-bg",
    )
