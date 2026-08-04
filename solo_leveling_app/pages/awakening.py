"""
pages/awakening.py — Multi-step onboarding / The Awakening flow.
"""
import reflex as rx
from solo_leveling_app.state import AppState


def _step_dot(step: int, label: str) -> rx.Component:
    is_active = AppState.onboarding_step == step
    is_done   = AppState.onboarding_step > step
    return rx.vstack(
        rx.box(
            rx.cond(
                is_done,
                rx.text("✓", class_name="text-[11px] font-black text-system-black"),
                rx.text(str(step), class_name="text-[11px] font-bold system-font"),
            ),
            class_name=rx.cond(
                is_done,
                "w-7 h-7 rounded-full flex items-center justify-center bg-neon-blue text-black",
                rx.cond(
                    is_active,
                    "w-7 h-7 rounded-full flex items-center justify-center border-2 border-neon-blue "
                    "text-neon-blue neon-blue-glow",
                    "w-7 h-7 rounded-full flex items-center justify-center border border-slate-700 text-slate-600",
                ),
            ),
        ),
        rx.text(
            label,
            class_name=rx.cond(
                is_active,
                "text-[10px] neon-text-blue hidden sm:block tracking-wider",
                "text-[10px] text-slate-700 hidden sm:block tracking-wider",
            ),
        ),
        align="center",
        gap="1",
    )


def _step_line() -> rx.Component:
    return rx.box(class_name="flex-1 h-px bg-system-border mt-3.5")


def step_indicator() -> rx.Component:
    steps = [
        (1, "IDENTITY"),
        (2, "ALGORITHM"),
        (3, "DEV"),
        (4, "VERIFY"),
        (5, "NEGOTIATE"),
    ]
    children = []
    for i, (n, label) in enumerate(steps):
        children.append(_step_dot(n, label))
        if i < len(steps) - 1:
            children.append(_step_line())
    return rx.hstack(*children, align="center", width="100%", class_name="mb-8")


# ── Step panels ──

def step_1() -> rx.Component:
    return rx.vstack(
        rx.text("[ STEP 1: HUNTER IDENTIFICATION ]",
                class_name="system-font neon-text-blue text-xs tracking-widest mb-1"),
        rx.text("State your name and fitness ambition, Hunter.",
                class_name="text-slate-500 text-xs mb-4"),
        rx.box(
            rx.text("HUNTER DESIGNATION", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.input(placeholder="Enter your name...", value=AppState.user_name,
                     on_change=AppState.set_user_name, class_name="system-input"),
            class_name="w-full",
        ),
        rx.box(
            rx.text("FITNESS OBJECTIVE", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.text_area(
                placeholder="e.g. Build calisthenics strength, run 5km daily, lose 10kg...",
                value=AppState.fitness_goal, on_change=AppState.set_fitness_goal,
                class_name="system-input", rows="4",
            ),
            class_name="w-full",
        ),
        gap="4", width="100%",
    )


def step_2() -> rx.Component:
    return rx.vstack(
        rx.text("[ STEP 2: ALGORITHMIC WARFARE ]",
                class_name="system-font neon-text-blue text-xs tracking-widest mb-1"),
        rx.text("Set your LeetCode quotas. The System will enforce them.",
                class_name="text-slate-500 text-xs mb-4"),
        rx.grid(
            rx.box(
                rx.text("DAILY", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
                rx.input(placeholder="3", value=AppState.dsa_daily,
                         on_change=AppState.set_dsa_daily, type="number", class_name="system-input"),
                class_name="w-full",
            ),
            rx.box(
                rx.text("WEEKLY", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
                rx.input(placeholder="21", value=AppState.dsa_weekly,
                         on_change=AppState.set_dsa_weekly, type="number", class_name="system-input"),
                class_name="w-full",
            ),
            rx.box(
                rx.text("MONTHLY", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
                rx.input(placeholder="90", value=AppState.dsa_monthly,
                         on_change=AppState.set_dsa_monthly, type="number", class_name="system-input"),
                class_name="w-full",
            ),
            columns="3", gap="3", width="100%",
        ),
        gap="4", width="100%",
    )


def step_3() -> rx.Component:
    return rx.vstack(
        rx.text("[ STEP 3: DEVELOPMENT MANDATE ]",
                class_name="system-font neon-text-blue text-xs tracking-widest mb-1"),
        rx.text("What will you build? Commit to it now or face consequences.",
                class_name="text-slate-500 text-xs mb-4"),
        rx.box(
            rx.text("WEEKLY PROJECT OBJECTIVE", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.text_area(
                placeholder="e.g. Ship 1 deployable feature per week, 300+ lines committed...",
                value=AppState.dev_goal, on_change=AppState.set_dev_goal,
                class_name="system-input", rows="4",
            ),
            class_name="w-full",
        ),
        rx.box(
            rx.text("EXTRACURRICULARS (OPTIONAL)", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.input(
                placeholder="e.g. Read 10 pages/day, meditate 15 min...",
                value=AppState.extracurricular, on_change=AppState.set_extracurricular,
                class_name="system-input",
            ),
            class_name="w-full",
        ),
        gap="4", width="100%",
    )


def step_4() -> rx.Component:
    return rx.vstack(
        rx.text("[ STEP 4: IDENTITY VERIFICATION ]",
                class_name="system-font neon-text-blue text-xs tracking-widest mb-1"),
        rx.text("Provide your credentials. The System will track you directly.",
                class_name="text-slate-500 text-xs mb-4"),
        rx.box(
            rx.text("GITHUB USERNAME", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.input(placeholder="e.g. octocat", value=AppState.github_id,
                     on_change=AppState.set_github_id, class_name="system-input"),
            class_name="w-full",
        ),
        rx.box(
            rx.text("LEETCODE USERNAME", class_name="text-[10px] text-slate-500 tracking-widest mb-1"),
            rx.input(placeholder="e.g. your_lc_username", value=AppState.leetcode_id,
                     on_change=AppState.set_leetcode_id, class_name="system-input"),
            class_name="w-full",
        ),
        gap="4", width="100%",
    )


def step_5() -> rx.Component:
    return rx.vstack(
        rx.text("[ STEP 5: SYSTEM NEGOTIATION ]",
                class_name="system-font neon-text-blue text-xs tracking-widest mb-1"),
        rx.text("The System will generate your Commitment Plan. Review it. Accept it.",
                class_name="text-slate-500 text-xs mb-4"),

        # Generate button (shown when plan not yet generated)
        rx.cond(
            ~AppState.ai_plan_visible & ~AppState.ai_plan_loading,
            rx.button(
                "⚡ GENERATE COMMITMENT PLAN",
                on_click=[AppState.generate_ai_plan, AppState.finish_ai_loading],
                class_name="system-button w-full py-3 text-xs tracking-[0.2em]",
            ),
            rx.fragment(),
        ),

        # Loading spinner
        rx.cond(
            AppState.ai_plan_loading,
            rx.vstack(
                rx.spinner(size="3", color="cyan"),
                rx.text("SYSTEM PROCESSING...",
                        class_name="system-font text-xs neon-text-blue animate-pulse tracking-widest"),
                align="center", gap="3", class_name="w-full py-8",
            ),
            rx.fragment(),
        ),

        # Plan revealed
        rx.cond(
            AppState.ai_plan_visible,
            rx.vstack(
                rx.box(
                    rx.text(
                        AppState.commitment_plan,
                        class_name="text-xs text-green-400 font-mono whitespace-pre-wrap leading-relaxed",
                    ),
                    class_name="w-full p-4 bg-black/60 border border-green-800/40 rounded overflow-auto max-h-64",
                ),
                rx.hstack(
                    rx.button(
                        "✗ DECLINE",
                        on_click=AppState.decline_plan,
                        class_name="system-button system-button-danger flex-1 text-xs",
                    ),
                    rx.button(
                        "⚡ ACCEPT & AWAKEN",
                        on_click=AppState.accept_awakening,
                        class_name="system-button flex-1 text-xs bg-neon-blue/10",
                    ),
                    gap="3", width="100%",
                ),
                gap="4", width="100%",
            ),
            rx.fragment(),
        ),
        gap="4", width="100%",
    )


# ── Full Page ──

def awakening_page() -> rx.Component:
    return rx.box(
        # Animated background
        rx.box(class_name="fixed inset-0 portal-bg z-0"),
        rx.box(
            class_name="fixed inset-0 z-0 opacity-[0.04]",
            style={
                "backgroundImage": (
                    "linear-gradient(rgba(0,212,255,1) 1px, transparent 1px),"
                    "linear-gradient(90deg, rgba(0,212,255,1) 1px, transparent 1px)"
                ),
                "backgroundSize": "60px 60px",
            },
        ),

        rx.center(
            rx.vstack(
                # Title
                rx.vstack(
                    rx.text(
                        "⚡ THE SYSTEM ⚡",
                        class_name="system-font text-3xl md:text-5xl neon-text-blue tracking-[0.3em] system-flicker",
                    ),
                    rx.text(
                        "AWAKENING PROTOCOL INITIATED",
                        class_name="text-slate-600 text-[10px] tracking-[0.6em] mt-1",
                    ),
                    align="center", gap="1", class_name="mb-10",
                ),

                # Steps
                step_indicator(),

                # Form card
                rx.box(
                    rx.vstack(
                        rx.cond(AppState.onboarding_step == 1, step_1(), rx.fragment()),
                        rx.cond(AppState.onboarding_step == 2, step_2(), rx.fragment()),
                        rx.cond(AppState.onboarding_step == 3, step_3(), rx.fragment()),
                        rx.cond(AppState.onboarding_step == 4, step_4(), rx.fragment()),
                        rx.cond(AppState.onboarding_step == 5, step_5(), rx.fragment()),
                        gap="4", width="100%", class_name="animate-slide-up",
                    ),
                    class_name="system-card p-6 md:p-8 w-full",
                ),

                # Back / Continue nav
                rx.cond(
                    AppState.onboarding_step < 5,
                    rx.hstack(
                        rx.cond(
                            AppState.onboarding_step > 1,
                            rx.button(
                                "← BACK",
                                on_click=AppState.prev_step,
                                class_name="system-button text-xs",
                            ),
                            rx.box(),
                        ),
                        rx.spacer(),
                        rx.button(
                            "CONTINUE →",
                            on_click=AppState.next_step,
                            class_name="system-button text-xs",
                        ),
                        width="100%", class_name="mt-4",
                    ),
                    rx.fragment(),
                ),

                rx.text(
                    "The System does not grant second chances.",
                    class_name="text-slate-700 text-[10px] tracking-widest mt-6",
                ),
                gap="0", width="100%", max_width="700px",
            ),
            class_name="relative z-10 min-h-screen px-4 py-12",
        ),
        class_name="min-h-screen w-full",
    )
