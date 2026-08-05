"""
pages/commitment.py — The Commitment: Digital Wallet & Accountability System.

How it works:
  • User commits Rs. (up to level × 10) via UPI QR code
  • Missing daily quests freezes 1% of balance per missed quest
  • Frozen money is NOT lost — it's accountability in action
  • Level up = cap increases, room to add more
"""
import reflex as rx
from solo_leveling_app.state import AppState
from solo_leveling_app.components.system_ui import system_nav


# ── UPI ID Settings Card ──────────────────────────────────────────────

def _upi_settings() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("UPI PAYMENT ID",
                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "700",
                           "fontSize": "0.65rem", "letterSpacing": "0.2em",
                           "color": "rgba(100,116,139,0.5)"}),
            rx.spacer(),
            rx.text("Change in .env → COMMITMENT_UPI_ID",
                    style={"fontFamily": "'Rajdhani',sans-serif", "fontSize": "0.6rem",
                           "color": "rgba(100,116,139,0.3)", "fontStyle": "italic"}),
            width="100%",
        ),
        rx.input(
            placeholder="your-upi@bank",
            value=AppState.commitment_upi_id,
            on_change=AppState.set_commitment_upi_id,
            class_name="commitment-input",
            style={"fontSize": "0.9rem"},
        ),
        rx.text(
            "This UPI ID receives your commitment deposit. Keep it private.",
            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                   "fontSize": "0.65rem", "color": "rgba(100,116,139,0.35)"},
        ),
        gap="3", width="100%",
    )


# ── Wallet Balance Card ───────────────────────────────────────────────

def _wallet_balance_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text("COMMITMENT WALLET",
                            style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                                   "fontSize": "0.6rem", "letterSpacing": "0.3em",
                                   "color": "rgba(0,212,255,0.6)"}),
                    rx.hstack(
                        rx.text("₹",
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "1.1rem", "color": "rgba(0,212,255,0.5)"}),
                        rx.text(AppState.wallet_balance.to(str),
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "2.8rem", "letterSpacing": "-0.02em",
                                       "color": "#00d4ff",
                                       "textShadow": "0 0 20px rgba(0,212,255,0.4)"}),
                        gap="1", align="end",
                    ),
                    gap="1",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("LEVEL CAP",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                   "fontSize": "0.6rem", "letterSpacing": "0.15em",
                                   "color": "rgba(100,116,139,0.4)", "textAlign": "right"}),
                    rx.hstack(
                        rx.text("₹",
                                style={"color": "rgba(100,116,139,0.4)",
                                       "fontFamily": "monospace", "fontSize": "0.7rem"}),
                        rx.text(AppState.wallet_cap,
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                                       "fontSize": "1.2rem", "color": "rgba(100,116,139,0.6)"}),
                        gap="1", align="end",
                    ),
                    rx.text(
                        rx.cond(
                            AppState.wallet_room_left > 0,
                            "Room left: ₹" + AppState.wallet_room_left.to(str),
                            "Cap reached — level up to add more",
                        ),
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                               "fontSize": "0.6rem",
                               "color": rx.cond(
                                   AppState.wallet_room_left > 0,
                                   "rgba(34,197,94,0.5)",
                                   "rgba(239,68,68,0.4)",
                               )},
                    ),
                    gap="1", align="end",
                ),
                width="100%", align="start",
            ),

            rx.box(class_name="h-3"),

            # Balance bar
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.box(style={"width": "10px", "height": "10px", "borderRadius": "50%",
                                      "background": "linear-gradient(135deg, #00d4ff, #9b59ff)"}),
                        rx.text("AVAILABLE",
                                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                       "fontSize": "0.6rem", "letterSpacing": "0.1em",
                                       "color": "rgba(0,212,255,0.6)"}),
                        rx.text("₹" + AppState.wallet_available.to(str),
                                style={"fontFamily": "monospace", "fontWeight": "700",
                                       "fontSize": "0.75rem", "color": "#00d4ff"}),
                        gap="2", align="center",
                    ),
                    rx.spacer(),
                    rx.cond(
                        AppState.wallet_frozen > 0,
                        rx.hstack(
                            rx.box(style={"width": "10px", "height": "10px", "borderRadius": "50%",
                                          "background": "rgba(148,163,184,0.4)"}),
                            rx.text("FROZEN",
                                    style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                           "fontSize": "0.6rem", "letterSpacing": "0.1em",
                                           "color": "rgba(100,116,139,0.5)"}),
                            rx.text("₹" + AppState.wallet_frozen.to(str),
                                    style={"fontFamily": "monospace", "fontWeight": "700",
                                           "fontSize": "0.75rem",
                                           "color": "rgba(148,163,184,0.6)"}),
                            gap="2", align="center",
                        ),
                        rx.fragment(),
                    ),
                    width="100%",
                ),
                # Combined bar
                rx.box(
                    rx.box(
                        style={
                            "height": "100%",
                            "width": AppState.wallet_available_pct.to_string() + "%",
                            "background": "linear-gradient(90deg, #00d4ff, #9b59ff)",
                            "borderRadius": "5px",
                            "transition": "width 0.5s cubic-bezier(0.4,0,0.2,1)",
                        },
                    ),
                    class_name="wallet-bar-container",
                ),
                gap="2", width="100%",
            ),

            rx.box(class_name="h-1"),

            rx.cond(
                AppState.wallet_frozen > 0,
                rx.hstack(
                    rx.text("❄",
                            style={"fontSize": "0.7rem", "color": "rgba(148,163,184,0.5)"}),
                    rx.text(
                        AppState.wallet_frozen_pct.to_string() + "% of your commitment is frozen due to missed quests.",
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                               "fontSize": "0.65rem", "color": "rgba(100,116,139,0.5)"},
                    ),
                    gap="2", align="center",
                ),
                rx.fragment(),
            ),

            gap="0", width="100%",
        ),
        class_name="wallet-card",
        width="100%",
    )


# ── Add Commitment Card ───────────────────────────────────────────────

def _add_commitment_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("ADD COMMITMENT",
                        style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                               "fontSize": "0.6rem", "letterSpacing": "0.25em",
                               "color": "rgba(0,212,255,0.6)"}),
                rx.spacer(),
                rx.cond(
                    AppState.wallet_room_left > 0,
                    rx.text(
                        "Max addable: ₹" + AppState.wallet_room_left.to(str),
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                               "fontSize": "0.62rem", "color": "rgba(34,197,94,0.5)"},
                    ),
                    rx.text("Level cap reached",
                            style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                                   "fontSize": "0.62rem", "color": "rgba(239,68,68,0.4)"}),
                ),
                width="100%",
            ),

            rx.box(class_name="h-2"),

            rx.hstack(
                rx.text("₹",
                        style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                               "fontSize": "1.2rem", "color": "rgba(0,212,255,0.6)",
                               "alignSelf": "center"}),
                rx.input(
                    placeholder="Enter amount (min ₹1)",
                    value=AppState.add_commitment_amount,
                    on_change=AppState.set_add_commitment_amount,
                    type="number",
                    class_name="commitment-input",
                    style={"fontSize": "1rem"},
                ),
                gap="2", width="100%", align="center",
            ),

            rx.box(class_name="h-3"),

            rx.button(
                "GENERATE UPI QR  →",
                on_click=AppState.open_commitment_qr,
                disabled=AppState.wallet_room_left <= 0,
                style={
                    "fontFamily": "'Orbitron',monospace",
                    "fontWeight": "700",
                    "fontSize": "0.6rem",
                    "letterSpacing": "0.2em",
                    "color": "#00d4ff",
                    "border": "1px solid rgba(0,212,255,0.4)",
                    "background": "rgba(0,212,255,0.05)",
                    "padding": "12px 28px",
                    "cursor": "pointer",
                    "borderRadius": "3px",
                    "transition": "all 0.25s",
                    "width": "100%",
                },
            ),

            rx.box(class_name="h-2"),

            rx.text(
                "A UPI QR code will appear. Scan it with any UPI app to deposit.",
                style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                       "fontSize": "0.65rem", "color": "rgba(100,116,139,0.35)",
                       "textAlign": "center"},
            ),

            gap="0", width="100%",
        ),
        class_name="wallet-card",
        width="100%",
    )


# ── Commitment Rules ─────────────────────────────────────────────────

def _commitment_rules() -> rx.Component:
    rules = [
        ("📊", "Max wallet balance = Level × ₹10", "rgba(0,212,255,0.5)"),
        ("📈", "Level up unlocks more room to commit", "rgba(0,212,255,0.5)"),
        ("❄",  "Each missed daily quest = 1% of balance frozen", "rgba(148,163,184,0.5)"),
        ("🔒", "Frozen money is NOT lost — it's accountability", "rgba(34,197,94,0.4)"),
        ("⚡", "Complete all daily quests for a full day = no new freeze", "rgba(155,89,255,0.5)"),
    ]
    return rx.vstack(
        rx.text("THE COMMITMENT PROTOCOL",
                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                       "fontSize": "0.55rem", "letterSpacing": "0.3em",
                       "color": "rgba(100,116,139,0.4)"}),
        rx.box(class_name="h-3"),
        *[
            rx.hstack(
                rx.text(icon, style={"fontSize": "0.85rem", "flexShrink": "0"}),
                rx.text(text,
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "600",
                               "fontSize": "0.78rem", "color": col}),
                gap="3", align="center",
            )
            for icon, text, col in rules
        ],
        gap="3",
        width="100%",
        style={"padding": "20px 24px",
               "background": "rgba(13,13,26,0.5)",
               "border": "1px solid rgba(26,26,51,0.6)",
               "borderRadius": "4px"},
    )


# ── Commitment History ────────────────────────────────────────────────

def _commitment_history() -> rx.Component:
    return rx.cond(
        AppState.commitment_history.length() > 0,
        rx.vstack(
            rx.text("COMMITMENT LOG",
                    style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                           "fontSize": "0.55rem", "letterSpacing": "0.3em",
                           "color": "rgba(100,116,139,0.4)"}),
            rx.vstack(
                rx.foreach(
                    AppState.commitment_history,
                    lambda entry: rx.text(
                        entry,
                        class_name="commitment-history-entry",
                        style={"width": "100%"},
                    ),
                ),
                gap="0", width="100%",
                style={"maxHeight": "200px", "overflowY": "auto"},
            ),
            gap="3", width="100%",
        ),
        rx.fragment(),
    )


# ── UPI QR Popup ──────────────────────────────────────────────────────

def _qr_popup() -> rx.Component:
    return rx.cond(
        AppState.show_commitment_qr,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.text("SCAN TO DEPOSIT",
                            style={"fontFamily": "'Orbitron',monospace", "fontWeight": "700",
                                   "fontSize": "0.55rem", "letterSpacing": "0.3em",
                                   "color": "rgba(0,212,255,0.6)"}),

                    rx.hstack(
                        rx.text("₹",
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "1.2rem", "color": "rgba(0,212,255,0.5)"}),
                        rx.text(AppState.commitment_qr_amount.to(str),
                                style={"fontFamily": "'Orbitron',monospace", "fontWeight": "900",
                                       "fontSize": "2.2rem", "color": "#00d4ff",
                                       "textShadow": "0 0 16px rgba(0,212,255,0.5)"}),
                        gap="1", align="end",
                    ),

                    rx.box(class_name="h-2"),

                    # QR Code from qrserver.com
                    rx.cond(
                        AppState.upi_qr_url != "",
                        rx.image(
                            src=AppState.upi_qr_url,
                            width="220px",
                            height="220px",
                            style={"borderRadius": "4px",
                                   "border": "2px solid rgba(0,212,255,0.3)"},
                        ),
                        rx.box(
                            rx.text("QR unavailable — add UPI ID above",
                                    style={"fontFamily": "'Rajdhani',sans-serif",
                                           "fontWeight": "500", "fontSize": "0.7rem",
                                           "color": "rgba(239,68,68,0.6)", "textAlign": "center"}),
                            style={"width": "220px", "height": "220px",
                                   "display": "flex", "alignItems": "center",
                                   "justifyContent": "center",
                                   "border": "1px dashed rgba(239,68,68,0.3)",
                                   "borderRadius": "4px"},
                        ),
                    ),

                    rx.box(class_name="h-2"),

                    rx.text(
                        "Scan with Google Pay, PhonePe, Paytm, or any UPI app.",
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                               "fontSize": "0.68rem", "color": "rgba(100,116,139,0.6)",
                               "textAlign": "center", "maxWidth": "260px"},
                    ),

                    rx.box(class_name="h-3"),

                    rx.hstack(
                        rx.button(
                            "CANCEL",
                            on_click=AppState.cancel_commitment_qr,
                            style={"fontFamily": "'Orbitron',monospace",
                                   "fontSize": "0.55rem", "letterSpacing": "0.2em",
                                   "color": "rgba(100,116,139,0.5)",
                                   "border": "1px solid rgba(100,116,139,0.2)",
                                   "background": "transparent",
                                   "padding": "10px 20px", "cursor": "pointer",
                                   "borderRadius": "2px"},
                        ),
                        rx.button(
                            "✓  I HAVE PAID",
                            on_click=AppState.confirm_commitment_paid,
                            style={"fontFamily": "'Orbitron',monospace",
                                   "fontWeight": "700",
                                   "fontSize": "0.55rem", "letterSpacing": "0.2em",
                                   "color": "#22c55e",
                                   "border": "1px solid rgba(34,197,94,0.4)",
                                   "background": "rgba(34,197,94,0.06)",
                                   "padding": "10px 24px", "cursor": "pointer",
                                   "borderRadius": "2px"},
                        ),
                        gap="3",
                    ),

                    align="center", gap="1",
                ),
                class_name="qr-popup-card",
            ),
            class_name="qr-popup-overlay",
        ),
        rx.fragment(),
    )


# ── Main Page ────────────────────────────────────────────────────────

def commitment_page() -> rx.Component:
    return rx.box(
        system_nav(),
        _qr_popup(),

        rx.box(
            rx.vstack(

                # Page header
                rx.vstack(
                    rx.text("THE COMMITMENT",
                            class_name="app-name-cinzel",
                            style={"fontSize": "2rem", "fontWeight": "900"}),
                    rx.text(
                        "Your money. Your accountability. The System doesn't steal — it freezes.",
                        style={"fontFamily": "'Rajdhani',sans-serif", "fontWeight": "500",
                               "fontSize": "0.85rem", "color": "rgba(100,116,139,0.55)",
                               "textAlign": "center", "maxWidth": "500px"},
                    ),
                    align="center", gap="2",
                    class_name="mb-8",
                ),

                # Main 2-col layout
                rx.grid(
                    # Left col: wallet balance + add commitment
                    rx.vstack(
                        _wallet_balance_card(),
                        _add_commitment_card(),
                        _commitment_history(),
                        gap="6", width="100%",
                    ),
                    # Right col: UPI settings + rules
                    rx.vstack(
                        _upi_settings(),
                        rx.box(class_name="h-2"),
                        _commitment_rules(),
                        gap="0", width="100%",
                    ),
                    columns=rx.breakpoints(initial="1", lg="2"),
                    gap="6",
                    width="100%",
                ),

                gap="0",
                width="100%",
            ),
            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "padding": "100px 32px 60px",
            },
        ),

        class_name="min-h-screen",
        style={
            "background": (
                "radial-gradient(ellipse at 70% 30%, rgba(0,212,255,0.04) 0%, transparent 60%),"
                "radial-gradient(ellipse at 20% 80%, rgba(155,89,255,0.03) 0%, transparent 50%),"
                "#020205"
            )
        },
    )
