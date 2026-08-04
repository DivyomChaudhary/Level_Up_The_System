"""
pages/gates.py — Dungeon selection & gate clearing screen.

NOTE: Inside rx.foreach, gate["rank"] is a Reflex Var — we cannot call .lower()
or use Python f-strings with it. Use rx.match() for all conditional class/style
selections on Var values.
"""
import reflex as rx
from solo_leveling_app.state import AppState, GateEntry
from solo_leveling_app.components.system_ui import system_nav


def _rank_color(rank) -> str:
    """rx.match on rank Var → CSS color hex for inline styles."""
    return rx.match(
        rank,
        ("S", "#ffd700"),
        ("A", "#c084fc"),
        ("B", "#60a5fa"),
        ("C", "#4ade80"),
        ("D", "#94a3b8"),
        "#6b7280",  # default E
    )


def _rank_border_color(rank) -> str:
    return rx.match(
        rank,
        ("S", "rgba(255,215,0,0.35)"),
        ("A", "rgba(192,132,252,0.35)"),
        ("B", "rgba(96,165,250,0.35)"),
        ("C", "rgba(74,222,128,0.35)"),
        ("D", "rgba(148,163,184,0.3)"),
        "rgba(107,114,128,0.3)",
    )


def _type_color(quest_type) -> str:
    return rx.match(
        quest_type,
        ("FITNESS", "#f97316"),
        ("DSA",     "#22d3ee"),
        ("DEV",     "#a78bfa"),
        "#94a3b8",
    )


def gate_card(gate: GateEntry) -> rx.Component:
    rank       = gate["rank"]
    rank_col   = _rank_color(rank)
    border_col = _rank_border_color(rank)
    type_col   = _type_color(gate["type"])
    is_cleared = AppState.gate_cleared_ids.contains(gate["title"])

    return rx.box(
        rx.vstack(
            # Rank icon + title row
            rx.hstack(
                rx.box(
                    rx.text(
                        rank,
                        style={"color": rank_col, "fontFamily": "'Orbitron',monospace",
                               "fontSize": "0.875rem", "fontWeight": "800"},
                    ),
                    style={
                        "width": "2rem", "height": "2rem",
                        "border": f"1px solid {border_col}",
                        "display": "flex", "alignItems": "center", "justifyContent": "center",
                        "borderRadius": "2px", "flexShrink": "0",
                        "backgroundColor": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                    },
                ),
                rx.vstack(
                    rx.text(gate["title"], class_name="text-sm font-semibold text-slate-200"),
                    rx.text(
                        rx.fragment("RANK ", rank, " GATE"),
                        style={"color": rank_col,
                               "fontSize": "0.625rem", "letterSpacing": "0.15em"},
                    ),
                    gap="0",
                ),
                rx.spacer(),
                # Type badge
                rx.box(
                    rx.text(
                        gate["type"],
                        style={"color": type_col,
                               "fontSize": "0.625rem", "letterSpacing": "0.1em",
                               "fontWeight": "600"},
                    ),
                    style={
                        "border": f"1px solid color-mix(in srgb, {type_col} 30%, transparent)",
                        "backgroundColor": f"color-mix(in srgb, {type_col} 10%, transparent)",
                        "padding": "2px 8px", "borderRadius": "2px",
                    },
                ),
                align="center", gap="2", width="100%",
            ),

            # Description
            rx.text(gate["desc"], class_name="text-xs text-slate-400 leading-relaxed"),

            # XP + action
            rx.hstack(
                rx.text(gate["xp"].to_string() + " XP", class_name="text-xs font-mono neon-text-blue"),
                rx.spacer(),
                rx.cond(
                    is_cleared,
                    rx.box(
                        rx.text("✓ CLEARED",
                                class_name="text-[10px] text-green-400 tracking-widest font-bold"),
                        class_name="px-2 py-0.5 border border-green-700/40 bg-green-950/30 rounded-sm",
                    ),
                    rx.button(
                        "ENTER GATE",
                        on_click=AppState.select_gate(gate),
                        style={
                            "color": rank_col,
                            "border": f"1px solid {border_col}",
                            "backgroundColor": f"color-mix(in srgb, {rank_col} 6%, transparent)",
                            "fontSize": "0.625rem", "letterSpacing": "0.15em",
                            "padding": "4px 12px", "borderRadius": "2px",
                            "cursor": "pointer", "transition": "all 0.2s",
                        },
                        variant="ghost",
                    ),
                ),
                align="center", width="100%",
            ),
            gap="3", width="100%",
        ),
        style={
            "border": f"1px solid {border_col}",
            "transition": "all 0.3s",
        },
        class_name="system-card p-4 hover:opacity-90",
    )


def gate_modal() -> rx.Component:
    """Submission modal when a gate is selected."""
    type_col = _type_color(AppState.selected_gate["type"])
    return rx.cond(
        AppState.selected_gate != {},
        rx.box(
            rx.box(
                rx.vstack(
                    # Modal header
                    rx.hstack(
                        rx.vstack(
                            rx.text("GATE ENTRY",
                                    class_name="system-font text-[10px] tracking-widest text-slate-500"),
                            rx.text(AppState.selected_gate["title"],
                                    class_name="system-font text-lg font-bold text-white"),
                            gap="0",
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=AppState.clear_gate,
                            class_name="text-slate-500 hover:text-white text-sm px-2 cursor-pointer",
                            variant="ghost",
                        ),
                        width="100%", align="center",
                    ),
                    rx.box(class_name="w-full h-px bg-system-border"),
                    rx.text(AppState.selected_gate["desc"],
                            class_name="text-sm text-slate-400 leading-relaxed"),
                    rx.hstack(
                        rx.text(
                            AppState.selected_gate["xp"].to_string() + " XP",
                            class_name="text-sm font-mono neon-text-blue",
                        ),
                        rx.spacer(),
                        rx.box(
                            rx.text(
                                AppState.selected_gate["type"],
                                style={"color": type_col,
                                       "fontSize": "0.625rem", "letterSpacing": "0.1em",
                                       "fontWeight": "600"},
                            ),
                            style={
                                "border": f"1px solid color-mix(in srgb, {type_col} 30%, transparent)",
                                "backgroundColor": f"color-mix(in srgb, {type_col} 10%, transparent)",
                                "padding": "2px 8px", "borderRadius": "2px",
                            },
                        ),
                        align="center", width="100%",
                    ),
                    rx.box(class_name="w-full h-px bg-system-border"),
                    rx.vstack(
                        rx.text("PROOF OF COMPLETION",
                                class_name="text-[10px] tracking-widest text-slate-500"),
                        rx.input(
                            placeholder="GitHub repo URL or LeetCode submission URL...",
                            value=AppState.gate_proof_url,
                            on_change=AppState.set_gate_proof_url,
                            class_name="system-input",
                        ),
                        gap="2", width="100%",
                    ),
                    rx.cond(
                        AppState.verification_message != "",
                        rx.text(AppState.verification_message,
                                class_name="text-xs font-mono text-green-400"),
                        rx.fragment(),
                    ),
                    rx.hstack(
                        rx.button(
                            "RETREAT",
                            on_click=AppState.clear_gate,
                            class_name="system-button system-button-danger flex-1 text-xs",
                        ),
                        rx.button(
                            "⚡ CLEAR GATE",
                            on_click=AppState.submit_gate_clear,
                            class_name="system-button flex-1 text-xs",
                        ),
                        gap="3", width="100%",
                    ),
                    gap="4", width="100%",
                ),
                class_name="system-card p-6 max-w-md w-full mx-4",
                style={"boxShadow": "0 0 50px rgba(155,89,255,0.2)"},
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm",
        ),
        rx.fragment(),
    )


def gates_page() -> rx.Component:
    rank_items = [
        ("E", "#6b7280"), ("D", "#94a3b8"), ("C", "#4ade80"),
        ("B", "#60a5fa"), ("A", "#c084fc"), ("S", "#ffd700"),
    ]
    return rx.box(
        gate_modal(),
        system_nav(),
        rx.box(
            rx.vstack(
                # Header
                rx.vstack(
                    rx.text("[ GATE REGISTRY ]",
                            class_name="system-font text-[10px] tracking-widest text-slate-600"),
                    rx.text("Dungeons & Gates",
                            class_name="system-font text-2xl font-black text-white tracking-wider"),
                    rx.text("Clear gates to earn bonus XP. Proof required for all submissions.",
                            class_name="text-slate-500 text-sm"),
                    gap="1", class_name="mb-4",
                ),

                # Rank legend (static, no Var ops)
                rx.hstack(
                    *[
                        rx.hstack(
                            rx.box(
                                style={"width": "8px", "height": "8px", "borderRadius": "50%",
                                       "backgroundColor": col, "flexShrink": "0"},
                            ),
                            rx.text(f"{r}-Rank", style={"color": col, "fontSize": "0.75rem"}),
                            gap="6px", align="center",
                        )
                        for r, col in rank_items
                    ],
                    gap="16px", flex_wrap="wrap", class_name="mb-2",
                ),

                # Gate grid
                rx.grid(
                    rx.foreach(AppState.gates, gate_card),
                    columns=rx.breakpoints(initial="1", md="2", lg="3"),
                    gap="3", width="100%",
                ),

                # Cleared counter
                rx.box(
                    rx.hstack(
                        rx.text("GATES CLEARED:", class_name="text-xs text-slate-600 tracking-widest"),
                        rx.text(AppState.gates_cleared_count,
                                class_name="text-xs neon-text-blue font-mono font-bold"),
                        rx.text("/", class_name="text-slate-700 text-xs"),
                        rx.text(AppState.gates_total,
                                class_name="text-xs text-slate-600 font-mono"),
                        gap="2", align="center",
                    ),
                    class_name="system-card p-3 text-center",
                ),
                gap="4", width="100%",
            ),
            class_name="pt-20 px-4 md:px-8 pb-12 max-w-7xl mx-auto",
        ),
        class_name="min-h-screen portal-bg",
    )
