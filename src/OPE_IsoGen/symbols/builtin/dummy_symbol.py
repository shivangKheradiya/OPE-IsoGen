class DummySymbol:
    """
    Minimal test symbol to verify config + CLI + exporter pipeline.
    """

    def __init__(self, size=100):
        self.size = size

    def render_svg(self):
        s = self.size
        svg = f"""
<svg width="{s}" height="{s}" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="{s}" height="{s}" fill="none" stroke="black" stroke-width="2" />
</svg>
"""
        return svg