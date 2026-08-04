"""
solo_leveling_app.py — Main entry point & routing only.
All business logic lives in state.py.
All UI lives in pages/ and components/.
"""
import reflex as rx

from solo_leveling_app.state import AppState
from solo_leveling_app.pages.awakening  import awakening_page
from solo_leveling_app.pages.dashboard  import dashboard_page
from solo_leveling_app.pages.gates      import gates_page
from solo_leveling_app.pages.leaderboard import leaderboard_page


def index() -> rx.Component:
    """
    Root page — conditionally renders awakening flow or the main app.
    Navigation between main app pages is handled via AppState.active_page.
    """
    return rx.box(
        rx.cond(
            AppState.awakened,
            # ── Awakened: route between main app pages ──
            rx.cond(
                AppState.active_page == "dashboard",
                dashboard_page(),
                rx.cond(
                    AppState.active_page == "gates",
                    gates_page(),
                    rx.cond(
                        AppState.active_page == "leaderboard",
                        leaderboard_page(),
                        dashboard_page(),   # fallback
                    ),
                ),
            ),
            # ── Not awakened: show onboarding ──
            awakening_page(),
        ),
        class_name="min-h-screen",
    )


# ── App configuration ──

app = rx.App(
    stylesheets=["/style.css"],
)


app.add_page(
    index,
    title="The System | Solo Leveling Habit Enforcer",
    route="/",
)
