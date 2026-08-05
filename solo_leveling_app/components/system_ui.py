"""
components/system_ui.py — Phase 2
Reusable UI: Sidebar, SystemAlerts, StatCards, XP bar,
             Profile panel, Stat bars, Quest verify overlay.
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
        ("CUSTOM",  "#6ee7b7"),
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


# ─── BADGE COMPONENTS ────────────────────────────────────────────────

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


# ─── PROFILE PANEL ───────────────────────────────────────────────────

def _stat_bar(label: str, pct_var, value_var, bar_class: str) -> rx.Component:
    """Horizontal stat bar with label, fill, and numeric value."""
    return rx.box(
        rx.text(label, class_name="stat-label"),
        rx.box(
            rx.box(
                class_name=f"stat-bar-fill {bar_class}",
                style={"width": pct_var.to_string() + "%"},
            ),
            class_name="stat-bar-track",
        ),
        rx.text(value_var, class_name="stat-value"),
        class_name="stat-row",
    )


def _profile_xp_bar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("XP", style={"fontSize": "0.6rem", "letterSpacing": "0.2em",
                                  "color": "rgba(100,116,139,0.5)"}),
            rx.spacer(),
            rx.hstack(
                rx.text(AppState.current_xp, style={"fontSize": "0.7rem",
                                                     "color": "rgba(0,212,255,0.7)",
                                                     "fontFamily": "monospace"}),
                rx.text("/", style={"color": "#1e293b", "fontSize": "0.7rem"}),
                rx.text(AppState.xp_to_level_up, style={"fontSize": "0.7rem",
                                                          "color": "rgba(100,116,139,0.4)",
                                                          "fontFamily": "monospace"}),
                gap="1",
            ),
            width="100%",
        ),
        rx.box(
            rx.box(
                style={
                    "width": AppState.xp_progress_pct.to_string() + "%",
                    "background": "linear-gradient(90deg, #00d4ff, #9b59ff)",
                    "boxShadow": "0 0 8px rgba(0,212,255,0.4)",
                    "transition": "width 0.5s ease",
                    "height": "100%",
                    "borderRadius": "9999px",
                },
            ),
            style={"width": "100%", "height": "6px",
                   "background": "rgba(255,255,255,0.04)",
                   "borderRadius": "9999px", "overflow": "hidden"},
        ),
        gap="1", width="100%",
    )


def _performance_chart() -> rx.Component:
    """Weekly performance line chart using recharts."""
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                stroke="rgba(255,255,255,0.04)",
            ),
            rx.recharts.x_axis(
                data_key="day",
                stroke="#1e293b",
                tick={"fill": "#4b5563", "fontSize": 9},
            ),
            rx.recharts.y_axis(
                stroke="#1e293b",
                tick={"fill": "#4b5563", "fontSize": 9},
                width=24,
            ),
            rx.recharts.line(
                data_key="expected",
                stroke="#1e3a5f",
                stroke_width=2,
                dot=False,
                name="Expected",
            ),
            rx.recharts.line(
                data_key="actual",
                stroke=rx.cond(AppState.is_on_track, "#22c55e", "#ef4444"),
                stroke_width=2,
                dot={"r": 3, "fill": rx.cond(AppState.is_on_track, "#22c55e", "#ef4444")},
                name="Actual",
            ),
            data=AppState.chart_data,
        ),
        width="100%",
        height=170,
    )


def _profile_mp_bar() -> rx.Component:
    """MP bar for profile panel — purple #9D00FF."""
    return rx.vstack(
        rx.hstack(
            rx.text("MANA",
                    style={"fontSize": "0.6rem", "letterSpacing": "0.2em",
                           "color": "rgba(157,0,255,0.5)"}),
            rx.spacer(),
            rx.hstack(
                rx.text("MP LV",
                        style={"fontSize": "0.55rem", "color": "rgba(157,0,255,0.35)",
                               "letterSpacing": "0.1em"}),
                rx.text(AppState.mp_level,
                        style={"fontSize": "0.7rem", "color": "#9D00FF",
                               "fontFamily": "'Orbitron',monospace", "fontWeight": "700"}),
                rx.text("·",
                        style={"color": "#1e293b"}),
                rx.text(AppState.current_mp,
                        style={"fontSize": "0.65rem", "color": "#9D00FF",
                               "fontFamily": "monospace"}),
                rx.text("/",
                        style={"color": "#1e293b", "fontSize": "0.65rem"}),
                rx.text(AppState.mp_to_level_up,
                        style={"fontSize": "0.65rem", "color": "rgba(100,116,139,0.3)",
                               "fontFamily": "monospace"}),
                gap="1", align="center",
            ),
            width="100%",
        ),
        rx.box(
            rx.box(
                style={"width": AppState.mp_progress_pct.to_string() + "%"},
                class_name="mp-bar-fill",
            ),
            style={"width": "100%", "height": "4px",
                   "background": "rgba(255,255,255,0.04)",
                   "borderRadius": "9999px", "overflow": "hidden"},
        ),
        gap="1", width="100%",
    )


def profile_panel() -> rx.Component:
    """Slide-in profile panel from the right. Triggered by toggle_profile."""
    rank_col = _rank_hex(AppState.hunter_rank)
    return rx.cond(
        AppState.profile_open,
        rx.box(
            # Backdrop click closes the panel
            rx.box(
                on_click=AppState.close_profile,
                style={"position": "absolute", "inset": "0"},
            ),
            # Panel itself
            rx.box(
                # Close button
                rx.hstack(
                    rx.text("HUNTER PROFILE",
                            style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.6rem",
                                   "letterSpacing": "0.3em", "color": "rgba(100,116,139,0.5)"}),
                    rx.spacer(),
                    rx.button(
                        "✕",
                        on_click=AppState.close_profile,
                        variant="ghost",
                        style={"color": "rgba(100,116,139,0.5)", "cursor": "pointer",
                               "fontSize": "0.9rem", "padding": "0"},
                    ),
                    width="100%",
                ),

                # Hunter identity
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.text(AppState.hunter_rank,
                                    style={"fontFamily": "'Orbitron',monospace",
                                           "fontSize": "1rem", "fontWeight": "900",
                                           "color": rank_col}),
                            style={
                                "width": "44px", "height": "44px",
                                "border": f"2px solid color-mix(in srgb, {rank_col} 40%, transparent)",
                                "background": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                                "display": "flex", "alignItems": "center",
                                "justifyContent": "center", "borderRadius": "4px",
                                "flexShrink": "0",
                            },
                        ),
                        rx.vstack(
                            rx.text(AppState.user_name,
                                    style={"color": "#f1f5f9", "fontSize": "1rem",
                                           "fontWeight": "600"}),
                            rx.hstack(
                                rx.text("Level",
                                        style={"color": "rgba(100,116,139,0.5)",
                                               "fontSize": "0.6rem", "letterSpacing": "0.15em"}),
                                rx.text(AppState.level,
                                        style={"color": "rgba(0,212,255,0.7)",
                                               "fontFamily": "monospace", "fontSize": "0.75rem",
                                               "fontWeight": "bold"}),
                                rx.text("·", style={"color": "#1e293b"}),
                                rx.text("🔥",
                                        style={"fontSize": "0.75rem"}),
                                rx.text(AppState.streak,
                                        style={"color": "#fb923c", "fontFamily": "monospace",
                                               "fontSize": "0.75rem", "fontWeight": "bold"}),
                                gap="2", align="center",
                            ),
                            gap="0.5",
                        ),
                        gap="3", align="center",
                    ),

                    # XP bar
                    _profile_xp_bar(),

                    # MP bar
                    _profile_mp_bar(),

                    gap="3", width="100%",
                    style={"padding": "16px", "border": "1px solid rgba(26,26,51,0.8)",
                           "borderRadius": "4px", "background": "rgba(13,13,26,0.5)"},
                ),

                # Divider
                rx.box(style={"height": "1px", "background": "rgba(26,26,51,0.8)"}),

                # Stats section
                rx.vstack(
                    rx.text("ATTRIBUTES",
                            style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.55rem",
                                   "letterSpacing": "0.3em", "color": "rgba(100,116,139,0.4)"}),
                    rx.box(class_name="h-1"),
                    _stat_bar("STRENGTH",     AppState.strength_pct,     AppState.strength_display,     "stat-bar-str"),
                    _stat_bar("INTELLIGENCE", AppState.intelligence_pct, AppState.intelligence_display, "stat-bar-int"),
                    _stat_bar("PERCEPTION",   AppState.perception_pct,   AppState.perception_display,   "stat-bar-per"),
                    rx.box(class_name="h-1"),
                    rx.hstack(
                        rx.text("STR = Fitness  ·  INT = DSA/Dev  ·  PER = Extras",
                                style={"fontSize": "0.55rem", "color": "rgba(100,116,139,0.3)",
                                       "letterSpacing": "0.05em"}),
                        gap="0",
                    ),
                    gap="2", width="100%",
                ),

                # Divider
                rx.box(style={"height": "1px", "background": "rgba(26,26,51,0.8)"}),

                # Performance chart
                rx.vstack(
                    rx.hstack(
                        rx.text("WEEKLY PERFORMANCE",
                                style={"fontFamily": "'Orbitron',monospace", "fontSize": "0.55rem",
                                       "letterSpacing": "0.3em", "color": "rgba(100,116,139,0.4)"}),
                        rx.spacer(),
                        rx.hstack(
                            rx.box(style={"width": "12px", "height": "2px",
                                          "background": "#1e3a5f", "borderRadius": "1px"}),
                            rx.text("Expected", style={"fontSize": "0.55rem",
                                                        "color": "rgba(100,116,139,0.4)"}),
                            rx.box(style={"width": "12px", "height": "2px",
                                          "background": rx.cond(AppState.is_on_track,
                                                                 "#22c55e", "#ef4444"),
                                          "borderRadius": "1px"}),
                            rx.text("Actual", style={"fontSize": "0.55rem",
                                                      "color": "rgba(100,116,139,0.4)"}),
                            gap="2", align="center",
                        ),
                        width="100%",
                    ),
                    _performance_chart(),
                    gap="2", width="100%",
                ),

                class_name="profile-panel",
            ),
            class_name="profile-overlay",
        ),
        rx.fragment(),
    )


# ─── NAVIGATION BAR ──────────────────────────────────────────────────

def system_nav() -> rx.Component:
    """Fixed top navigation bar."""
    nav_items = [
        ("DASHBOARD",   "dashboard"),
        ("DUNGEONS",    "gates"),
        ("LEADERBOARD", "leaderboard"),
        ("COMMITMENT",  "commitment"),
    ]
    rank_col = _rank_hex(AppState.hunter_rank)
    return rx.box(
        # Profile overlay rendered at top level so it overlays everything
        profile_panel(),

        rx.hstack(
        rx.hstack(
                rx.text("⚡", style={"fontSize": "1.1rem",
                                     "filter": "drop-shadow(0 0 6px rgba(0,212,255,0.8))"}),
                rx.box(
                    rx.text(
                        "LEVELING UP:",
                        style={"fontFamily": "'Cinzel Decorative', serif",
                               "fontSize": "0.52rem",
                               "fontWeight": "400",
                               "letterSpacing": "0.18em",
                               "color": "rgba(100,116,139,0.6)",
                               "lineHeight": "1"},
                    ),
                    rx.text(
                        "THE SYSTEM",
                        class_name="app-name-cinzel",
                        style={"fontSize": "0.85rem", "lineHeight": "1.1"},
                    ),
                    class_name="hidden sm:flex flex-col gap-0",
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
            # Hunter summary — clickable to open profile
            rx.hstack(
                rx.vstack(
                    rx.text(AppState.user_name,
                            style={"fontSize": "0.75rem", "fontWeight": "500",
                                   "color": "#f1f5f9", "textAlign": "right"}),
                    rx.hstack(
                        rx.text("LVL",
                                style={"fontSize": "0.6rem", "color": "rgba(100,116,139,0.5)",
                                       "letterSpacing": "0.15em"}),
                        rx.text(AppState.level,
                                style={"fontSize": "0.65rem", "color": "rgba(0,212,255,0.7)",
                                       "fontFamily": "monospace", "fontWeight": "bold"}),
                        rx.text("·", style={"color": "#1e293b"}),
                        rx.text("🔥", style={"fontSize": "0.65rem"}),
                        rx.text(AppState.streak,
                                style={"fontSize": "0.65rem", "color": "#fb923c",
                                       "fontFamily": "monospace", "fontWeight": "bold"}),
                        gap="1", align="center",
                    ),
                    gap="0", align="end",
                ),
                # Rank avatar button
                rx.box(
                    rx.text(AppState.hunter_rank,
                            style={"fontFamily": "'Orbitron',monospace",
                                   "fontSize": "0.75rem", "fontWeight": "900",
                                   "color": rank_col}),
                    style={
                        "width": "32px", "height": "32px",
                        "border": f"2px solid color-mix(in srgb, {rank_col} 40%, transparent)",
                        "background": f"color-mix(in srgb, {rank_col} 8%, transparent)",
                        "display": "flex", "alignItems": "center",
                        "justifyContent": "center", "borderRadius": "50%",
                        "cursor": "pointer", "flexShrink": "0",
                        "transition": "box-shadow 0.2s ease",
                    },
                ),
                on_click=AppState.toggle_profile,
                gap="2",
                align="center",
                style={"cursor": "pointer"},
            ),
            align="center",
            width="100%",
        ),
        class_name=(
            "fixed top-0 left-0 right-0 z-50 px-4 md:px-8 py-3 "
            "border-b border-system-border bg-system-dark/95 backdrop-blur-md"
        ),
    )


# ─── XP BAR (updated: uses current_xp not total_xp) ─────────────────

def xp_bar() -> rx.Component:
    """Horizontal XP progress bar for dashboard card."""
    return rx.vstack(
        rx.hstack(
            rx.text("XP TO NEXT LEVEL", style={"fontSize": "0.6rem", "letterSpacing": "0.15em",
                                                "color": "rgba(100,116,139,0.5)"}),
            rx.spacer(),
            rx.hstack(
                rx.text(AppState.current_xp,
                        style={"fontSize": "0.7rem", "color": "rgba(0,212,255,0.7)",
                               "fontFamily": "monospace"}),
                rx.text("/", style={"color": "#1e293b", "fontSize": "0.7rem"}),
                rx.text(AppState.xp_to_level_up,
                        style={"fontSize": "0.7rem", "color": "rgba(100,116,139,0.4)",
                               "fontFamily": "monospace"}),
                gap="1",
            ),
            width="100%",
        ),
        rx.box(
            rx.box(
                style={
                    "width": AppState.xp_progress_pct.to_string() + "%",
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


# ─── STREAK COUNTER ───────────────────────────────────────────────────

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


# ─── STAT CARD ────────────────────────────────────────────────────────

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


# ─── QUEST VERIFICATION POPUP ─────────────────────────────────────────

def _verify_link_input(label: str, value_var, on_change) -> rx.Component:
    return rx.vstack(
        rx.text(label,
                style={"fontSize": "0.6rem", "letterSpacing": "0.2em",
                       "color": "rgba(100,116,139,0.5)"}),
        rx.input(
            placeholder="https://...",
            value=value_var,
            on_change=on_change,
            style={
                "width": "100%",
                "background": "transparent",
                "border": "none",
                "borderBottom": "1px solid rgba(0,212,255,0.2)",
                "color": "#e2e8f0",
                "fontFamily": "monospace",
                "fontSize": "0.8rem",
                "padding": "8px 0",
                "outline": "none",
            },
        ),
        gap="1", width="100%",
    )


def quest_verify_overlay() -> rx.Component:
    """Full-screen popup when quest checkbox is clicked (not yet done)."""
    quest_title_display = rx.cond(
        AppState.verify_quest_type == "DSA",
        "SOLUTION LINKS",
        rx.cond(
            AppState.verify_quest_type == "DEV",
            "PROJECT PROOF",
            "ACTIVITY PROOF",
        ),
    )
    return rx.cond(
        AppState.verify_is_open,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.text("VERIFICATION ENGINE",
                                    style={"fontFamily": "'Orbitron',monospace",
                                           "fontSize": "0.55rem", "letterSpacing": "0.35em",
                                           "color": "rgba(0,212,255,0.35)"}),
                            rx.text(quest_title_display,
                                    style={"fontFamily": "'Orbitron',monospace",
                                           "fontSize": "1rem", "fontWeight": "900",
                                           "color": "#f1f5f9"}),
                            gap="1",
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕", on_click=AppState.cancel_verify,
                            variant="ghost",
                            style={"color": "rgba(100,116,139,0.5)", "cursor": "pointer",
                                   "fontSize": "1rem"},
                        ),
                        width="100%", align="start",
                    ),

                    rx.box(style={"height": "1px", "background": "rgba(26,26,51,0.8)"}),

                    rx.text(
                        rx.cond(
                            AppState.verify_quest_type == "DSA",
                            "Paste your LeetCode solution URLs to verify completion.",
                            rx.cond(
                                AppState.verify_quest_type == "DEV",
                                "Paste your GitHub commit, PR, or deployment URL.",
                                "Paste any proof link (Strava, photo URL, etc.)",
                            ),
                        ),
                        style={"fontSize": "0.75rem", "color": "rgba(100,116,139,0.5)"},
                    ),

                    rx.box(class_name="h-2"),

                    # Link input 1 — always shown
                    _verify_link_input(
                        "LINK 1",
                        AppState.verify_link_1,
                        AppState.set_verify_link_1,
                    ),

                    # Link input 2 — DSA only, if dsa_per_day >= 2
                    rx.cond(
                        (AppState.verify_quest_type == "DSA") & (AppState.dsa_per_day >= 2),
                        _verify_link_input(
                            "LINK 2",
                            AppState.verify_link_2,
                            AppState.set_verify_link_2,
                        ),
                        rx.fragment(),
                    ),

                    # Link input 3 — DSA only, if dsa_per_day >= 3
                    rx.cond(
                        (AppState.verify_quest_type == "DSA") & (AppState.dsa_per_day >= 3),
                        _verify_link_input(
                            "LINK 3",
                            AppState.verify_link_3,
                            AppState.set_verify_link_3,
                        ),
                        rx.fragment(),
                    ),

                    # Error
                    rx.cond(
                        AppState.verify_error != "",
                        rx.hstack(
                            rx.text("⚠", style={"color": "#ef4444", "fontSize": "0.75rem"}),
                            rx.text(AppState.verify_error,
                                    style={"color": "#ef4444", "fontSize": "0.72rem",
                                           "fontFamily": "monospace"}),
                            gap="2", align="center",
                        ),
                        rx.fragment(),
                    ),

                    rx.box(class_name="h-2"),

                    rx.hstack(
                        rx.button(
                            "SKIP / TRUST SYSTEM",
                            on_click=AppState.submit_quest_verify,
                            variant="ghost",
                            style={"fontSize": "0.6rem", "letterSpacing": "0.2em",
                                   "color": "rgba(100,116,139,0.4)", "cursor": "pointer",
                                   "padding": "8px 16px",
                                   "border": "1px solid rgba(100,116,139,0.15)"},
                        ),
                        rx.button(
                            "SUBMIT PROOF  →",
                            on_click=AppState.submit_quest_verify,
                            style={
                                "fontFamily": "'Orbitron',monospace",
                                "fontSize": "0.65rem", "letterSpacing": "0.2em",
                                "color": "#020205",
                                "background": "linear-gradient(135deg, #00d4ff, #9b59ff)",
                                "border": "none", "padding": "10px 28px",
                                "cursor": "pointer", "fontWeight": "700",
                                "boxShadow": "0 0 20px rgba(0,212,255,0.3)",
                            },
                        ),
                        gap="3", justify="end", width="100%",
                    ),

                    gap="4", width="100%",
                ),
                class_name="verify-panel",
            ),
            class_name="verify-overlay",
        ),
        rx.fragment(),
    )


# ─── SYSTEM ALERT (PENALTY) DIALOG ───────────────────────────────────

def penalty_dialog() -> rx.Component:
    """Full-screen penalty overlay dialog."""
    return rx.cond(
        AppState.penalty_active,
        rx.box(
            rx.box(
                rx.vstack(
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
                    rx.box(
                        rx.text(
                            AppState.penalty_message,
                            class_name="text-xs text-red-300 font-mono leading-relaxed text-center",
                        ),
                        class_name="p-4 bg-red-950/20 border border-red-900/30 rounded-sm w-full",
                    ),
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


# ─── INSTANCE DUNGEON KEY POPUP ───────────────────────────────────────

def _vintage_key_svg() -> rx.Component:
    """Vintage brass key rendered as inline SVG."""
    return rx.html(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60" width="140" height="70">
  <defs>
    <radialGradient id="brassG" cx="40%" cy="30%">
      <stop offset="0%"  stop-color="#f5d17a"/>
      <stop offset="45%" stop-color="#c9962b"/>
      <stop offset="100%" stop-color="#7a5200"/>
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Key bow (ring) -->
  <circle cx="22" cy="30" r="16" fill="none" stroke="url(#brassG)" stroke-width="5" filter="url(#glow)"/>
  <circle cx="22" cy="30" r="8"  fill="none" stroke="url(#brassG)" stroke-width="2.5"/>
  <!-- Key blade (shaft) -->
  <line x1="36" y1="30" x2="108" y2="30" stroke="url(#brassG)" stroke-width="5" stroke-linecap="round" filter="url(#glow)"/>
  <!-- Key teeth -->
  <rect x="72" y="30" width="5" height="11" rx="1" fill="url(#brassG)"/>
  <rect x="84" y="30" width="5" height="8"  rx="1" fill="url(#brassG)"/>
  <rect x="96" y="30" width="5" height="14" rx="1" fill="url(#brassG)"/>
  <!-- Notch on shaft -->
  <rect x="60" y="24" width="5" height="6" rx="1" fill="#0a0a1a"/>
  <!-- Inner bow detail -->
  <circle cx="22" cy="30" r="3" fill="url(#brassG)" opacity="0.6"/>
</svg>"""
    )


def key_popup() -> rx.Component:
    """Overlay shown when user earns an instance dungeon key."""
    return rx.cond(
        AppState.show_key_popup,
        rx.box(
            rx.box(
                rx.vstack(
                    # Floating key icon
                    rx.box(
                        _vintage_key_svg(),
                        class_name="key-icon-float",
                        style={"marginBottom": "8px"},
                    ),

                    rx.text(
                        "INSTANCE DUNGEON KEY",
                        style={
                            "fontFamily": "'Orbitron', monospace",
                            "fontSize": "0.7rem",
                            "letterSpacing": "0.35em",
                            "color": "rgba(155,89,255,0.7)",
                        },
                    ),

                    rx.box(class_name="h-2"),

                    rx.text(
                        "ACQUIRED",
                        style={
                            "fontFamily": "'Cinzel Decorative', serif",
                            "fontSize": "1.8rem",
                            "fontWeight": "900",
                            "background": "linear-gradient(135deg, #f5d17a 0%, #c9962b 60%, #ffd700 100%)",
                            "-webkit-background-clip": "text",
                            "-webkit-text-fill-color": "transparent",
                            "backgroundClip": "text",
                            "filter": "drop-shadow(0 0 12px rgba(201,150,43,0.6))",
                        },
                    ),

                    rx.box(class_name="h-3"),

                    rx.text(
                        "The System has rewarded your discipline.",
                        style={
                            "fontFamily": "'Rajdhani', sans-serif",
                            "fontWeight": "500",
                            "fontSize": "0.85rem",
                            "color": "rgba(148,163,184,0.7)",
                            "textAlign": "center",
                            "maxWidth": "260px",
                        },
                    ),

                    rx.text(
                        "A rift has been detected near your monthly quests.",
                        style={
                            "fontFamily": "'Rajdhani', sans-serif",
                            "fontWeight": "400",
                            "fontSize": "0.75rem",
                            "color": "rgba(100,116,139,0.5)",
                            "textAlign": "center",
                            "maxWidth": "280px",
                        },
                    ),

                    rx.box(class_name="h-2"),

                    rx.hstack(
                        rx.text("KEYS HELD:", style={"fontSize": "0.6rem", "color": "rgba(100,116,139,0.4)",
                                                     "letterSpacing": "0.2em", "fontFamily": "'Orbitron',monospace"}),
                        rx.text(AppState.instance_dungeon_key_count,
                                style={"fontFamily": "monospace", "fontWeight": "700",
                                       "color": "#f5d17a", "fontSize": "0.9rem"}),
                        gap="2", align="center",
                    ),

                    rx.box(class_name="h-4"),

                    rx.button(
                        "TAKE THE KEY  →",
                        on_click=AppState.dismiss_key_popup,
                        style={
                            "fontFamily": "'Orbitron', monospace",
                            "fontSize": "0.6rem",
                            "letterSpacing": "0.25em",
                            "color": "#f5d17a",
                            "border": "1px solid rgba(245,209,122,0.4)",
                            "background": "transparent",
                            "padding": "10px 28px",
                            "cursor": "pointer",
                            "borderRadius": "2px",
                            "transition": "all 0.2s",
                        },
                    ),

                    align="center", gap="0",
                ),
                class_name="key-popup-card",
            ),
            class_name="key-popup-overlay",
        ),
        rx.fragment(),
    )
