"""
pages/gates.py — Phase 3.
• Gates use GateDisplayEntry (from state.gate_display_list)
• Persistent gates: ↺ badge, recur every 7 days, -700 MP if missed
• Iterative gates: ⟳ badge, cleared permanently
• Rewards are MP (not XP, not stats)
• Rank-colored borders + preview cards
"""
import reflex as rx
from solo_leveling_app.state import AppState, GateDisplayEntry
from solo_leveling_app.components.system_ui import system_nav


# ── Color helpers (rx.match on Var) ──────────────────────────────────

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


def _rank_glow(rank) -> str:
    return rx.match(
        rank,
        ("S", "0 0 24px rgba(255,215,0,0.12)"),
        ("A", "0 0 24px rgba(192,132,252,0.10)"),
        ("B", "0 0 24px rgba(96,165,250,0.10)"),
        ("C", "0 0 20px rgba(74,222,128,0.08)"),
        ("D", "0 0 16px rgba(148,163,184,0.06)"),
        "none",
    )


def _type_color(quest_type) -> str:
    return rx.match(
        quest_type,
        ("FITNESS", "#f97316"),
        ("DSA",     "#22d3ee"),
        ("DEV",     "#a78bfa"),
        "#94a3b8",
    )


def _status_badge(status, days_remaining) -> rx.Component:
    return rx.cond(
        status == "cleared",
        rx.text("✓ CLEARED", class_name="gate-badge-cleared"),
        rx.cond(
            status == "refreshing",
            rx.text(
                "↺ REFRESHES IN " + days_remaining.to_string() + "D",
                class_name="gate-badge-persistent",
            ),
            rx.cond(
                status == "overdue",
                rx.text("⚠ OVERDUE — -700 MP", class_name="gate-badge-overdue"),
                rx.fragment(),
            ),
        ),
    )


def _gate_type_badge(gate_type) -> rx.Component:
    return rx.cond(
        gate_type == "persistent",
        rx.text("↺ RECURRING", class_name="gate-badge-persistent"),
        rx.text("⟳ ONCE", class_name="gate-badge-iterative"),
    )


# ── Gate card ──────────────────────────────────────────────────────

def gate_card(gate: GateDisplayEntry) -> rx.Component:
    rank        = gate["rank"]
    rank_col    = _rank_color(rank)
    border_col  = _rank_border_color(rank)
    glow        = _rank_glow(rank)
    type_col    = _type_color(gate["type"])
    is_inactive = (gate["status"] == "cleared") | (gate["status"] == "refreshing")

    return rx.box(
        rx.vstack(
            # Top row: rank badge + type color dot + gate type badge
            rx.hstack(
                # Rank badge
                rx.text(
                    rank,
                    style={
                        "fontFamily": "'Orbitron',monospace",
                        "fontSize": "0.75rem", "fontWeight": "900",
                        "color": rank_col,
                        "padding": "3px 8px",
                        "border": f"1px solid {border_col}",
                        "borderRadius": "2px",
                        "background": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                    },
                ),
                # Type dot
                rx.box(
                    style={"width": "7px", "height": "7px", "borderRadius": "50%",
                           "background": type_col, "flexShrink": "0",
                           "boxShadow": f"0 0 8px {type_col}"},
                ),
                rx.spacer(),
                _gate_type_badge(gate["gate_type"]),
                gap="2", align="center", width="100%",
            ),

            # Title + type
            rx.vstack(
                rx.text(
                    gate["title"],
                    style={"color": rank_col, "fontFamily": "'Orbitron',monospace",
                           "fontSize": "0.72rem", "fontWeight": "700",
                           "letterSpacing": "0.05em", "lineHeight": "1.3"},
                ),
                rx.text(
                    gate["type"],
                    style={"color": type_col, "fontSize": "0.6rem",
                           "letterSpacing": "0.15em"},
                ),
                gap="0.5",
            ),

            # Description
            rx.text(
                gate["desc"],
                style={"color": "rgba(148,163,184,0.55)", "fontSize": "0.72rem",
                       "lineHeight": "1.5"},
            ),

            # MP reward
            rx.hstack(
                rx.text("⬡", style={"color": "#9D00FF", "fontSize": "1rem"}),
                rx.text(
                    "+" + gate["mp"].to_string() + " MP",
                    style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.75rem",
                           "fontWeight": "700", "color": "#9D00FF",
                           "textShadow": "0 0 12px rgba(157,0,255,0.4)"},
                ),
                rx.spacer(),
                _status_badge(gate["status"], gate["days_remaining"]),
                gap="2", align="center", width="100%",
            ),

            # Action button (only if active or overdue)
            rx.cond(
                is_inactive,
                rx.fragment(),
                rx.button(
                    rx.cond(
                        gate["status"] == "overdue",
                        "RE-CLEAR GATE (Overdue)",
                        "ENTER GATE →",
                    ),
                    on_click=AppState.select_gate(gate),
                    style={
                        "fontFamily": "'Orbitron',monospace",
                        "fontSize": "0.6rem", "letterSpacing": "0.15em",
                        "color": rank_col,
                        "background": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                        "border": f"1px solid {border_col}",
                        "padding": "7px 16px", "cursor": "pointer", "width": "100%",
                        "textAlign": "center", "transition": "all 0.2s ease",
                    },
                    variant="ghost",
                ),
            ),

            gap="3", width="100%",
        ),
        style={
            "border": f"1px solid {border_col}",
            "boxShadow": glow,
            "opacity": rx.cond(is_inactive & (gate["status"] != "overdue"), "0.45", "1"),
            "transition": "all 0.3s ease",
            "background": "rgba(8,8,15,0.8)",
        },
        class_name="system-card p-4",
    )


# ── Gate submit modal ─────────────────────────────────────────────

def gate_modal() -> rx.Component:
    """Submission modal for a selected gate."""
    rank     = AppState.selected_gate["rank"]
    rank_col = _rank_color(rank)
    mp_val   = AppState.selected_gate["mp"]
    return rx.cond(
        AppState.selected_gate != {},
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text("GATE ENTRY",
                                    style={"fontFamily": "'Orbitron',monospace",
                                           "fontSize": "0.55rem", "letterSpacing": "0.3em",
                                           "color": "rgba(100,116,139,0.4)"}),
                            rx.text(AppState.selected_gate["title"],
                                    style={"fontFamily": "'Orbitron',monospace",
                                           "fontSize": "1rem", "fontWeight": "800",
                                           "color": "#f1f5f9"}),
                            gap="0",
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=AppState.clear_gate,
                            variant="ghost",
                            style={"color": "rgba(100,116,139,0.5)", "cursor": "pointer",
                                   "fontSize": "1.1rem"},
                        ),
                        gap="3", align="start", width="100%",
                    ),

                    rx.box(style={"height": "1px", "background": "rgba(26,26,51,0.8)"}),

                    # MP reward display
                    rx.hstack(
                        rx.text("⬡", style={"color": "#9D00FF", "fontSize": "1.5rem"}),
                        rx.vstack(
                            rx.text("MANA REWARD",
                                    style={"fontSize": "0.55rem", "letterSpacing": "0.2em",
                                           "color": "rgba(157,0,255,0.4)"}),
                            rx.text(
                                "+" + mp_val.to_string() + " MP",
                                style={"fontFamily": "'Orbitron',monospace",
                                       "fontSize": "1.5rem", "fontWeight": "900",
                                       "color": "#9D00FF",
                                       "textShadow": "0 0 20px rgba(157,0,255,0.5)"},
                            ),
                            gap="0",
                        ),
                        gap="3", align="center",
                    ),

                    # Gate type info
                    rx.cond(
                        AppState.selected_gate["gate_type"] == "persistent",
                        rx.box(
                            rx.text(
                                "↺  RECURRING GATE — refreshes in 7 days after clearing.",
                                style={"fontSize": "0.68rem", "color": "rgba(34,211,238,0.5)",
                                       "fontFamily": "monospace"},
                            ),
                            style={"padding": "8px 12px",
                                   "border": "1px solid rgba(34,211,238,0.12)",
                                   "background": "rgba(34,211,238,0.04)",
                                   "borderRadius": "2px"},
                        ),
                        rx.box(
                            rx.text(
                                "⟳  ONE-TIME GATE — permanently cleared after submission.",
                                style={"fontSize": "0.68rem", "color": "rgba(167,139,250,0.5)",
                                       "fontFamily": "monospace"},
                            ),
                            style={"padding": "8px 12px",
                                   "border": "1px solid rgba(167,139,250,0.12)",
                                   "background": "rgba(167,139,250,0.04)",
                                   "borderRadius": "2px"},
                        ),
                    ),

                    # Proof URL
                    rx.vstack(
                        rx.text("PROOF URL",
                                style={"fontSize": "0.6rem", "letterSpacing": "0.2em",
                                       "color": "rgba(100,116,139,0.4)"}),
                        rx.input(
                            placeholder="https://github.com/... or LeetCode URL",
                            value=AppState.gate_proof_url,
                            on_change=AppState.set_gate_proof_url,
                            class_name="system-input",
                        ),
                        gap="1", width="100%",
                    ),

                    # Error / success message
                    rx.cond(
                        AppState.gate_verify_message != "",
                        rx.text(
                            AppState.gate_verify_message,
                            style={
                                "fontSize": "0.72rem", "fontFamily": "monospace",
                                "color": rx.cond(
                                    AppState.gate_verify_message.contains("ERROR"),
                                    "#ef4444", "#22c55e",
                                ),
                            },
                        ),
                        rx.fragment(),
                    ),

                    rx.hstack(
                        rx.button(
                            "CANCEL",
                            on_click=AppState.clear_gate,
                            variant="ghost",
                            style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.6rem",
                                   "letterSpacing": "0.2em", "color": "rgba(100,116,139,0.4)",
                                   "border": "1px solid rgba(100,116,139,0.15)",
                                   "padding": "8px 16px", "cursor": "pointer"},
                        ),
                        rx.button(
                            "SUBMIT PROOF →",
                            on_click=AppState.submit_gate_clear,
                            style={
                                "fontFamily": "'Orbitron',monospace", "fontSize": "0.65rem",
                                "letterSpacing": "0.2em", "color": "#020205",
                                "background": "linear-gradient(135deg, #6b21a8, #9D00FF)",
                                "border": "none", "padding": "10px 28px",
                                "cursor": "pointer", "fontWeight": "700",
                                "boxShadow": "0 0 20px rgba(157,0,255,0.35)",
                            },
                        ),
                        gap="3", justify="end", width="100%",
                    ),

                    gap="4", width="100%",
                ),
                class_name="system-card p-8 max-w-lg w-full mx-4",
                style={"boxShadow": "0 0 60px rgba(157,0,255,0.12)"},
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm",
        ),
        rx.fragment(),
    )


# ── Gates page ───────────────────────────────────────────────────────

def gates_page() -> rx.Component:
    rank_items = [
        ("E", "#6b7280", 200),
        ("D", "#94a3b8", 400),
        ("C", "#4ade80", 800),
        ("B", "#60a5fa", 1200),
        ("A", "#c084fc", 1800),
        ("S", "#ffd700", 3000),
    ]
    return rx.box(
        gate_modal(),
        system_nav(),
        rx.box(
            rx.vstack(
                # Header
                rx.vstack(
                    rx.text("[ GATE REGISTRY ]",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                   "fontSize": "0.62rem", "letterSpacing": "0.3em",
                                   "color": "#374151"}),
                    rx.text("Dungeons & Gates",
                            class_name="app-name-cinzel",
                            style={"fontSize": "2.2rem", "fontWeight": "900"}),
                    rx.text("Clear gates for massive MP rewards. Proof required.",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                                   "fontSize": "0.8rem", "color": "rgba(100,116,139,0.5)"}),
                    gap="1", class_name="mb-4", align="start",
                ),

                # MP Bar — full width at top of page
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.text("MP LEVEL",
                                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                                           "fontSize": "0.62rem", "letterSpacing": "0.2em",
                                           "color": "rgba(157,0,255,0.7)"}),
                            rx.text(AppState.mp_level,
                                    style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                           "fontSize": "1.1rem", "color": "#9D00FF",
                                           "textShadow": "0 0 12px rgba(157,0,255,0.5)"}),
                            gap="2", align="center",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.text(AppState.current_mp,
                                    style={"fontFamily": "monospace", "fontWeight": "700",
                                           "fontSize": "0.72rem", "color": "rgba(157,0,255,0.7)"}),
                            rx.text("/", style={"color": "#1e293b", "fontSize": "0.72rem"}),
                            rx.text(AppState.mp_to_level_up,
                                    style={"fontFamily": "monospace", "fontSize": "0.72rem",
                                           "color": "rgba(100,116,139,0.35)"}),
                            rx.text("MP", style={"fontFamily": "'Rajdhani',sans-serif",
                                                  "fontWeight": "600", "fontSize": "0.6rem",
                                                  "color": "rgba(100,116,139,0.3)",
                                                  "letterSpacing": "0.1em"}),
                            gap="1", align="center",
                        ),
                        width="100%", align="center",
                    ),
                    rx.box(class_name="h-2"),
                    rx.box(
                        rx.box(
                            style={"width": AppState.mp_progress_pct.to_string() + "%",
                                   "height": "100%",
                                   "background": "linear-gradient(90deg, #9D00FF, #c084fc)",
                                   "borderRadius": "3px",
                                   "transition": "width 0.5s cubic-bezier(0.4,0,0.2,1)",
                                   "boxShadow": "0 0 8px rgba(157,0,255,0.5)"},
                        ),
                        class_name="mp-page-bar",
                    ),
                    style={"padding": "14px 20px",
                           "background": "rgba(157,0,255,0.04)",
                           "border": "1px solid rgba(157,0,255,0.2)",
                           "borderRadius": "4px",
                           "marginBottom": "20px"},
                ),

                # Gate type preview cards
                rx.flex(
                    rx.box(
                        rx.text("♟", style={"fontSize": "1.8rem", "color": "#22d3ee",
                                            "textShadow": "0 0 15px rgba(34,211,238,0.4)"}),
                        rx.text("DSA GATE",
                                style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.65rem",
                                       "fontWeight": "800", "color": "#22d3ee",
                                       "letterSpacing": "0.2em", "marginTop": "8px"}),
                        rx.text("Algorithm challenges. Solve LeetCode problems to grow your intelligence.",
                                style={"fontSize": "0.68rem", "color": "rgba(148,163,184,0.6)",
                                       "lineHeight": "1.5", "marginTop": "6px"}),
                        rx.text("200 — 3000 MP",
                                style={"fontSize": "0.6rem", "color": "rgba(157,0,255,0.5)",
                                       "fontFamily": "'Orbitron',monospace", "marginTop": "auto",
                                       "paddingTop": "12px"}),
                        class_name="gate-type-card",
                        style={"borderColor": "rgba(34,211,238,0.15)",
                               "boxShadow": "0 0 20px rgba(34,211,238,0.03)",
                               "display": "flex", "flexDirection": "column"},
                    ),
                    rx.box(
                        rx.text("⚡", style={"fontSize": "1.8rem", "color": "#f97316",
                                            "textShadow": "0 0 15px rgba(249,115,22,0.4)"}),
                        rx.text("FITNESS GATE",
                                style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.65rem",
                                       "fontWeight": "800", "color": "#f97316",
                                       "letterSpacing": "0.2em", "marginTop": "8px"}),
                        rx.text("Physical trials. Push-ups, squats, runs. Proof required.",
                                style={"fontSize": "0.68rem", "color": "rgba(148,163,184,0.6)",
                                       "lineHeight": "1.5", "marginTop": "6px"}),
                        rx.text("200 — 1200 MP",
                                style={"fontSize": "0.6rem", "color": "rgba(157,0,255,0.5)",
                                       "fontFamily": "'Orbitron',monospace", "marginTop": "auto",
                                       "paddingTop": "12px"}),
                        class_name="gate-type-card",
                        style={"borderColor": "rgba(249,115,22,0.15)",
                               "boxShadow": "0 0 20px rgba(249,115,22,0.03)",
                               "display": "flex", "flexDirection": "column"},
                    ),
                    rx.box(
                        rx.text("⚙", style={"fontSize": "1.8rem", "color": "#a78bfa",
                                            "textShadow": "0 0 15px rgba(167,139,250,0.4)"}),
                        rx.text("DEV GATE",
                                style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.65rem",
                                       "fontWeight": "800", "color": "#a78bfa",
                                       "letterSpacing": "0.2em", "marginTop": "8px"}),
                        rx.text("Build and deploy real projects. From mini-apps to full SaaS.",
                                style={"fontSize": "0.68rem", "color": "rgba(148,163,184,0.6)",
                                       "lineHeight": "1.5", "marginTop": "6px"}),
                        rx.text("800 — 3000 MP",
                                style={"fontSize": "0.6rem", "color": "rgba(157,0,255,0.5)",
                                       "fontFamily": "'Orbitron',monospace", "marginTop": "auto",
                                       "paddingTop": "12px"}),
                        class_name="gate-type-card",
                        style={"borderColor": "rgba(167,139,250,0.15)",
                               "boxShadow": "0 0 20px rgba(167,139,250,0.03)",
                               "display": "flex", "flexDirection": "column"},
                    ),
                    gap="4", wrap="wrap", width="100%", class_name="mb-4",
                ),

                # MP rank legend
                rx.hstack(
                    *[
                        rx.hstack(
                            rx.box(
                                style={"width": "8px", "height": "8px", "borderRadius": "50%",
                                       "backgroundColor": col, "flexShrink": "0"},
                            ),
                            rx.text(f"{r} · {mp}MP",
                                    style={"color": col, "fontSize": "0.68rem",
                                           "fontFamily": "monospace"}),
                            gap="6px", align="center",
                        )
                        for r, col, mp in rank_items
                    ],
                    gap="3", flex_wrap="wrap", class_name="mb-5",
                ),

                # Check persistent gate penalties button
                rx.hstack(
                    rx.button(
                        "↺ CHECK GATE PENALTIES",
                        on_click=AppState.check_persistent_gate_penalties,
                        style={
                            "fontFamily": "'Orbitron',monospace", "fontSize": "0.55rem",
                            "letterSpacing": "0.2em", "color": "rgba(34,211,238,0.4)",
                            "border": "1px solid rgba(34,211,238,0.15)", "padding": "6px 16px",
                            "background": "transparent", "cursor": "pointer", "borderRadius": "2px",
                        },
                        variant="ghost",
                    ),
                    rx.text("(runs 7-day overdue check for persistent gates)",
                            style={"fontSize": "0.6rem", "color": "rgba(100,116,139,0.3)"}),
                    gap="3", align="center", class_name="mb-5",
                ),

                # Gate cards grid
                rx.grid(
                    rx.foreach(AppState.gate_display_list, gate_card),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    gap="4", width="100%",
                ),

                gap="0", width="100%",
            ),
            class_name="pt-20 px-4 md:px-8 pb-12 max-w-7xl mx-auto",
        ),
        class_name="min-h-screen portal-bg",
    )
