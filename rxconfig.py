import reflex as rx
from reflex_base.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="solo_leveling_app",
    plugins=[
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                accent_color="cyan",
                gray_color="slate",
                radius="none",
                scaling="100%",
            ),
        ),
    ],
    disable_plugins=[SitemapPlugin],
)
