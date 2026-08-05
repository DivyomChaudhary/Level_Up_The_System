"""
pages/awakening.py — Full-screen cinematic onboarding experience.

Steps:
  0 → Reawakening intro animation  (click to proceed)
  1 → Name + physical aim          (Enter / Continue)
  2 → Class selection split-screen (click to choose)
  3 → Daily target + custom quests (Continue)
  4 → Extracurriculars             (Continue / Skip)
  5 → Commitment plan preview      (Awaken)
"""
import reflex as rx
from solo_leveling_app.state import AppState


# ── Step progress dots ─────────────────────────────────────────────

def _step_dots(current: int) -> rx.Component:
    """Small progress indicators shown on steps 1-5."""
    total = 5
    dots = []
    for i in range(1, total + 1):
        cls = rx.cond(
            current == i,
            "step-dot step-dot-active",
            rx.cond(current > i, "step-dot step-dot-done", "step-dot"),
        )
        dots.append(rx.box(class_name=cls))
    return rx.hstack(*dots, gap="8px",
                     class_name="fixed top-8 left-1/2 -translate-x-1/2 z-50")


# ── Step label ────────────────────────────────────────────────────

def _step_label(text: str) -> rx.Component:
    return rx.text(
        text,
        class_name="awaken-sub mb-6",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 0 — REAWAKENING INTRO
# ══════════════════════════════════════════════════════════════════

def _intro_screen() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Pulsing ellipsis
            rx.text("· · ·",
                    class_name="text-slate-800 text-3xl tracking-[0.6em] intro-1",
                    style={"fontFamily": "monospace"}),

            rx.box(class_name="h-8"),

            rx.text("A FAINT PULSE DETECTED",
                    class_name="awaken-sub intro-2"),

            rx.box(class_name="h-2"),

            rx.text("HUNTER IDENTIFIED",
                    class_name="awaken-sub intro-3",
                    style={"color": "rgba(0,212,255,0.25)", "letterSpacing": "0.5em"}),

            rx.box(class_name="h-10"),

            # Main title — large glitch effect
            rx.text(
                "LEVELING UP: THE SYSTEM",
                class_name="app-name-cinzel intro-4",
                style={
                    "fontSize": "clamp(1.8rem, 6vw, 3.5rem)",
                    "fontWeight": "900",
                    "letterSpacing": "0.06em",
                },
            ),

            rx.box(class_name="h-6"),

            rx.text("INITIATING AWAKENING SEQUENCE",
                    class_name="awaken-sub intro-5",
                    style={"color": "rgba(155,89,255,0.4)", "letterSpacing": "0.4em"}),

            rx.box(class_name="h-16"),

            rx.text(
                "[ CLICK ANYWHERE TO BEGIN ]",
                class_name="awaken-sub animate-pulse intro-6",
                style={"letterSpacing": "0.3em", "color": "rgba(100,116,139,0.5)"},
            ),

            align="center", gap="0",
        ),
        on_click=AppState.next_step,
        class_name="min-h-screen flex items-center justify-center bg-black cursor-pointer overflow-hidden",
        style={
            "background": (
                "radial-gradient(ellipse at 50% 60%, rgba(0,212,255,0.04) 0%, transparent 60%),"
                "radial-gradient(ellipse at 30% 30%, rgba(155,89,255,0.03) 0%, transparent 50%),"
                "#020205"
            )
        },
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 1 — NAME + PHYSICAL AIM
# ══════════════════════════════════════════════════════════════════

def _name_screen() -> rx.Component:
    return rx.box(
        _step_dots(1),
        rx.vstack(
            _step_label("HUNTER IDENTIFICATION"),

            rx.text("What is your name?",
                    class_name="awaken-question screen-enter"),

            rx.box(class_name="h-5"),

            rx.input(
                placeholder="Enter your name...",
                value=AppState.user_name,
                on_change=AppState.set_user_name,
                on_key_down=AppState.handle_name_key,
                class_name="awaken-input",
                auto_focus=True,
            ),

            rx.box(class_name="h-14"),

            _step_label("PHYSICAL OBJECTIVE"),

            rx.text("State your fitness commitment.",
                    class_name="awaken-question screen-enter",
                    style={"fontSize": "clamp(1.1rem, 3vw, 1.6rem)"}),

            rx.box(class_name="h-4"),

            rx.text_area(
                placeholder="e.g. 100 push-ups, 100 squats, and a 3km run every day...",
                value=AppState.fitness_goal,
                on_change=AppState.set_fitness_goal,
                rows="3",
                class_name="awaken-textarea",
            ),

            rx.box(class_name="h-10"),

            rx.button(
                "CONTINUE  →",
                on_click=AppState.next_step,
                class_name="awaken-continue",
                disabled=AppState.user_name == "",
            ),

            align="center", gap="0", width="100%", max_width="600px",
        ),
        class_name="awaken-screen portal-bg",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 2 — CLASS SELECTION (SPLIT SCREEN)
# ══════════════════════════════════════════════════════════════════

def _class_screen() -> rx.Component:
    return rx.box(
        # Title overlay
        rx.box(
            rx.vstack(
                rx.text("SELECT YOUR MAIN CLASS",
                        class_name="awaken-sub screen-enter",
                        style={"letterSpacing": "0.5em", "color": "rgba(100,116,139,0.6)"}),
                rx.text(
                    "Your main class sets recommended targets — you will do both DSA and Projects.",
                    style={"fontSize": "0.65rem", "color": "rgba(100,116,139,0.3)",
                           "letterSpacing": "0.05em", "textAlign": "center",
                           "maxWidth": "420px"},
                    class_name="screen-enter",
                ),
                align="center", gap="2",
            ),
            class_name="absolute top-8 left-0 right-0 flex justify-center z-10",
        ),

        # Split halves
        rx.box(
            # ── LEFT: Shadow Mage ─────────────────────────────────
            rx.box(
                rx.vstack(
                    rx.text("✦",
                            style={"fontSize": "3.5rem", "color": "#c084fc",
                                   "textShadow": "0 0 30px rgba(192,132,252,0.6)"},
                            class_name="screen-enter"),
                    rx.box(class_name="h-4"),
                    rx.text("SHADOW MAGE",
                            class_name="system-font screen-enter",
                            style={"fontSize": "clamp(1.4rem, 3vw, 2rem)",
                                   "fontWeight": "900", "letterSpacing": "0.15em",
                                   "color": "#c084fc",
                                   "textShadow": "0 0 15px rgba(192,132,252,0.4)"}),
                    rx.text("DSA  ·  Algorithms  ·  Logic",
                            style={"fontSize": "0.65rem", "letterSpacing": "0.35em",
                                   "color": "rgba(192,132,252,0.5)"},
                            class_name="mt-1 screen-enter"),
                    rx.box(class_name="h-6"),
                    rx.text(
                        "Master the arcane arts of data structures. "
                        "Conjure solutions from silence. Every algorithm a spell — "
                        "every submission a strike.",
                        style={"maxWidth": "280px", "textAlign": "center",
                               "color": "rgba(148,163,184,0.7)",
                               "fontSize": "0.82rem", "lineHeight": "1.7"},
                        class_name="screen-enter",
                    ),
                    rx.box(class_name="h-8"),
                    rx.text("[ CLICK TO CHOOSE ]",
                            style={"fontSize": "0.6rem", "letterSpacing": "0.3em",
                                   "color": "rgba(192,132,252,0.3)"}),
                    align="center", gap="0",
                ),
                on_click=AppState.choose_class("Shadow Mage"),
                class_name="class-side class-mage",
            ),

            # ── CENTER DIVIDER ────────────────────────────────────
            rx.box(
                rx.text("VS",
                        class_name="system-font",
                        style={"fontSize": "0.6rem", "letterSpacing": "0.3em",
                               "color": "rgba(100,116,139,0.2)",
                               "writingMode": "vertical-rl",
                               "textOrientation": "mixed"}),
                style={
                    "position": "absolute",
                    "left": "50%", "top": "50%",
                    "transform": "translate(-50%, -50%)",
                    "zIndex": "20",
                    "display": "flex", "alignItems": "center", "justifyContent": "center",
                },
            ),

            # ── RIGHT: Shadow Assassin ───────────────────────────
            rx.box(
                rx.vstack(
                    rx.text("⚔",
                            style={"fontSize": "3.5rem", "color": "#f87171",
                                   "textShadow": "0 0 30px rgba(239,68,68,0.6)"},
                            class_name="screen-enter"),
                    rx.box(class_name="h-4"),
                    rx.text("SHADOW ASSASSIN",
                            class_name="system-font screen-enter",
                            style={"fontSize": "clamp(1.1rem, 2.5vw, 1.7rem)",
                                   "fontWeight": "900", "letterSpacing": "0.12em",
                                   "color": "#f87171",
                                   "textShadow": "0 0 15px rgba(239,68,68,0.4)"}),
                    rx.text("Projects  ·  Build  ·  Deploy",
                            style={"fontSize": "0.65rem", "letterSpacing": "0.35em",
                                   "color": "rgba(248,113,113,0.5)"},
                            class_name="mt-1 screen-enter"),
                    rx.box(class_name="h-6"),
                    rx.text(
                        "Strike with precision. Build things that bleed. "
                        "Every commit a kill — every deployment a conquest. "
                        "No half measures.",
                        style={"maxWidth": "280px", "textAlign": "center",
                               "color": "rgba(148,163,184,0.7)",
                               "fontSize": "0.82rem", "lineHeight": "1.7"},
                        class_name="screen-enter",
                    ),
                    rx.box(class_name="h-8"),
                    rx.text("[ CLICK TO CHOOSE ]",
                            style={"fontSize": "0.6rem", "letterSpacing": "0.3em",
                                   "color": "rgba(248,113,113,0.3)"}),
                    align="center", gap="0",
                ),
                on_click=AppState.choose_class("Shadow Assassin"),
                class_name="class-side class-assassin",
            ),

            class_name="class-choice-container",
            style={"position": "relative"},
        ),

        class_name="min-h-screen bg-black overflow-hidden relative",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 3 — DAILY TARGET + CUSTOM QUESTS
# ══════════════════════════════════════════════════════════════════

def _custom_quest_tag(quest: str) -> rx.Component:
    return rx.hstack(
        rx.text(quest, class_name="text-xs text-slate-300"),
        rx.text(
            "✕",
            on_click=AppState.remove_custom_quest(quest),
            class_name="text-slate-600 hover:text-red-400 cursor-pointer text-xs ml-1",
        ),
        class_name="px-3 py-1.5 border border-slate-800 rounded-sm bg-slate-900/60 items-center",
        gap="2",
    )


def _stepper(label: str, sub: str, value_var, on_inc, on_dec,
             rec_var, value_color: str = "stepper-value") -> rx.Component:
    """A +/- stepper with recommended badge."""
    return rx.vstack(
        rx.text(label,
                class_name="awaken-sub",
                style={"letterSpacing": "0.25em", "color": "rgba(148,163,184,0.5)"}),
        rx.text(sub,
                style={"fontSize": "0.6rem", "color": "rgba(100,116,139,0.35)",
                       "letterSpacing": "0.1em"}),
        rx.box(class_name="h-2"),
        rx.hstack(
            rx.button(
                "−",
                on_click=on_dec,
                class_name="stepper-btn",
            ),
            rx.text(value_var, class_name=value_color),
            rx.button(
                "+",
                on_click=on_inc,
                class_name="stepper-btn",
            ),
            gap="3", align="center",
        ),
        rx.cond(
            rec_var,
            rx.text("✓ RECOMMENDED", class_name="recommended-badge"),
            rx.box(class_name="h-5"),  # spacer to maintain height
        ),
        align="center", gap="1",
    )


def _target_screen() -> rx.Component:
    return rx.box(
        _step_dots(3),
        rx.vstack(
            _step_label("TARGET CONFIGURATION"),

            rx.text("Set your daily commitment.",
                    class_name="awaken-question screen-enter"),

            rx.box(class_name="h-2"),

            rx.text(
                "Both DSA and Projects are required. Your main class recommendation is shown below.",
                style={"color": "rgba(100,116,139,0.4)", "fontSize": "0.75rem",
                       "textAlign": "center", "maxWidth": "480px"},
            ),

            rx.box(class_name="h-10"),

            # Dual steppers
            rx.flex(
                _stepper(
                    label="DSA PROBLEMS / DAY",
                    sub="WEEKDAYS ONLY · WEEKENDS = REVISION",
                    value_var=AppState.dsa_per_day,
                    on_inc=AppState.increment_dsa,
                    on_dec=AppState.decrement_dsa,
                    rec_var=AppState.dsa_is_recommended,
                    value_color="stepper-value",
                ),
                # Divider
                rx.box(
                    style={"width": "1px", "background": "rgba(26,26,51,0.8)",
                           "margin": "0 40px", "alignSelf": "stretch"},
                ),
                _stepper(
                    label="PROJECTS / WEEK",
                    sub="DEPLOYMENTS · GITHUB MERGES · RELEASES",
                    value_var=AppState.projects_per_week,
                    on_inc=AppState.increment_projects,
                    on_dec=AppState.decrement_projects,
                    rec_var=AppState.projects_is_recommended,
                    value_color="stepper-value stepper-value-purple",
                ),
                justify="center",
                align="start",
                wrap="wrap",
                gap="0",
            ),

            rx.box(class_name="h-10"),

            # Custom quests section
            rx.vstack(
                rx.text("ADD CUSTOM DAILY / WEEKLY QUESTS",
                        class_name="awaken-sub",
                        style={"color": "rgba(148,163,184,0.4)", "letterSpacing": "0.3em"}),

                rx.box(class_name="h-3"),

                rx.hstack(
                    rx.input(
                        placeholder="e.g. Read 10 pages every night...",
                        value=AppState.new_quest_input,
                        on_change=AppState.set_new_quest_input,
                        on_key_down=AppState.handle_quest_key,
                        class_name="system-input",
                        style={"maxWidth": "400px"},
                    ),
                    rx.button(
                        "ADD",
                        on_click=AppState.add_custom_quest,
                        class_name="system-button text-xs",
                        style={"padding": "10px 20px", "flexShrink": "0"},
                    ),
                    gap="3", align="center",
                ),

                rx.cond(
                    AppState.custom_quests.length() > 0,
                    rx.box(
                        rx.flex(
                            rx.foreach(AppState.custom_quests, _custom_quest_tag),
                            flex_wrap="wrap",
                            gap="2",
                        ),
                        class_name="mt-3 max-w-lg",
                    ),
                    rx.fragment(),
                ),

                align="center", gap="0", width="100%",
            ),

            rx.box(class_name="h-10"),

            rx.button(
                "CONTINUE  →",
                on_click=AppState.next_step,
                class_name="awaken-continue",
            ),

            align="center", gap="0", width="100%", max_width="700px",
        ),
        class_name="awaken-screen portal-bg",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 4 — EXTRACURRICULARS
# ══════════════════════════════════════════════════════════════════

def _extras_screen() -> rx.Component:
    return rx.box(
        _step_dots(4),
        rx.vstack(
            _step_label("OPTIONAL PROTOCOL"),

            rx.text("Any other pursuits?",
                    class_name="awaken-question screen-enter"),

            rx.box(class_name="h-3"),

            rx.text(
                "Clubs, competitions, languages, instruments... anything you track.",
                style={"color": "rgba(100,116,139,0.6)", "fontSize": "0.8rem",
                       "letterSpacing": "0.05em", "textAlign": "center"},
            ),

            rx.box(class_name="h-8"),

            rx.text_area(
                placeholder="e.g. Chess club Tuesdays, learning Spanish 15 min/day...",
                value=AppState.extra_activities,
                on_change=AppState.set_extra_activities,
                rows="4",
                class_name="awaken-textarea",
            ),

            rx.box(class_name="h-8"),

            rx.hstack(
                rx.button(
                    "SKIP  →",
                    on_click=AppState.next_step,
                    class_name="awaken-continue",
                    style={"color": "rgba(100,116,139,0.5)",
                           "borderColor": "rgba(100,116,139,0.2)",
                           "fontSize": "0.65rem"},
                ),
                rx.button(
                    "CONTINUE  →",
                    on_click=AppState.next_step,
                    class_name="awaken-continue",
                ),
                gap="4",
            ),

            align="center", gap="0", width="100%", max_width="580px",
        ),
        class_name="awaken-screen portal-bg",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 5 — URL VERIFICATION
# ══════════════════════════════════════════════════════════════════

def _url_field(
    label: str,
    placeholder: str,
    value,
    on_change,
    error_var,
    prefix: str,
) -> rx.Component:
    return rx.vstack(
        rx.text(label,
                class_name="awaken-sub self-start",
                style={"letterSpacing": "0.25em", "color": "rgba(148,163,184,0.5)"}),

        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            class_name="system-input",
            style={"maxWidth": "520px", "fontFamily": "monospace", "fontSize": "0.82rem"},
        ),

        rx.cond(
            error_var != "",
            rx.hstack(
                rx.text("⚠", style={"color": "#ef4444", "fontSize": "0.75rem"}),
                rx.text(
                    error_var,
                    class_name="url-error",
                ),
                rx.text(
                    prefix,
                    style={"color": "rgba(239,68,68,0.5)", "fontFamily": "monospace",
                           "fontSize": "0.7rem"},
                ),
                align="center", gap="2",
            ),
            rx.text(
                prefix + "...",
                style={"fontSize": "0.65rem", "color": "rgba(100,116,139,0.3)",
                       "fontFamily": "monospace"},
            ),
        ),

        gap="2", width="100%", max_width="520px", align="start",
    )


def _verify_screen() -> rx.Component:
    return rx.box(
        _step_dots(5),
        rx.vstack(
            _step_label("IDENTITY VERIFICATION"),

            rx.text("Prove your presence.",
                    class_name="awaken-question screen-enter"),

            rx.box(class_name="h-2"),

            rx.text(
                "Links are optional but tracked. Invalid format will be flagged.",
                style={"color": "rgba(100,116,139,0.5)", "fontSize": "0.78rem",
                       "textAlign": "center"},
            ),

            rx.box(class_name="h-10"),

            _url_field(
                label="GITHUB PROFILE",
                placeholder="https://github.com/your-username",
                value=AppState.github_url,
                on_change=AppState.set_github_url,
                error_var=AppState.url_github_error,
                prefix="https://github.com/",
            ),

            rx.box(class_name="h-6"),

            _url_field(
                label="LINKEDIN PROFILE",
                placeholder="https://linkedin.com/in/your-username",
                value=AppState.linkedin_url,
                on_change=AppState.set_linkedin_url,
                error_var=AppState.url_linkedin_error,
                prefix="https://linkedin.com/in/",
            ),

            rx.box(class_name="h-10"),

            rx.button(
                "CONTINUE  →",
                on_click=AppState.try_next_from_verify,
                class_name="awaken-continue",
            ),

            align="center", gap="0", width="100%", max_width="580px",
        ),
        class_name="awaken-screen portal-bg",
    )


# ══════════════════════════════════════════════════════════════════
# SCREEN 6 — COMMITMENT PLAN PREVIEW (no negotiate)
# ══════════════════════════════════════════════════════════════════

def _plan_screen() -> rx.Component:
    return rx.box(
        _step_dots(6),
        rx.vstack(
            _step_label("SYSTEM CONFIGURATION"),

            rx.text("Your commitment.",
                    class_name="awaken-question screen-enter"),

            rx.box(class_name="h-2"),

            rx.text(
                "This is exactly what you agreed to. The System remembers everything.",
                style={"color": "rgba(100,116,139,0.5)", "fontSize": "0.78rem",
                       "textAlign": "center"},
            ),

            rx.box(class_name="h-8"),

            # Terminal plan display
            rx.box(
                rx.text(
                    AppState.commitment_plan_text,
                    class_name="plan-terminal screen-enter",
                ),
                width="100%",
                max_width="660px",
                overflow_x="auto",
            ),

            rx.box(class_name="h-8"),

            rx.button(
                "⚡  AWAKEN",
                on_click=AppState.accept_awakening,
                class_name="awaken-continue awaken-continue-purple",
                style={"fontSize": "0.8rem", "letterSpacing": "0.3em",
                       "padding": "14px 52px"},
            ),

            align="center", gap="0", width="100%",
        ),
        class_name="awaken-screen portal-bg",
        style={"paddingTop": "5rem", "paddingBottom": "4rem",
               "alignItems": "center", "justifyContent": "flex-start"},
    )


# ══════════════════════════════════════════════════════════════════
# ROOT PAGE — routes between all 7 screens
# ══════════════════════════════════════════════════════════════════

def awakening_page() -> rx.Component:
    return rx.cond(
        AppState.onboarding_step == 0, _intro_screen(),
        rx.cond(
        AppState.onboarding_step == 1, _name_screen(),
        rx.cond(
        AppState.onboarding_step == 2, _class_screen(),
        rx.cond(
        AppState.onboarding_step == 3, _target_screen(),
        rx.cond(
        AppState.onboarding_step == 4, _extras_screen(),
        _plan_screen(),  # step 5 = plan (URL step removed)
        ))))
    )
