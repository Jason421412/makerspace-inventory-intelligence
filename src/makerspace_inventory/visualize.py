from __future__ import annotations

from pathlib import Path

from .analysis import summarize
from .models import InventoryItem


def create_status_chart(items: list[InventoryItem], output_path: str | Path) -> Path:
    summary = summarize(items)
    status_counts = summary["status_counts"]
    labels = list(status_counts)
    values = [status_counts[label] for label in labels]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".png":
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise RuntimeError("PNG charts require matplotlib. Use .svg output or install requirements.txt.") from exc

        colors = ["#2f6f4e", "#c75643", "#d7a22a", "#7b68aa", "#2f6f88", "#777777"]
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(labels, values, color=colors[: len(labels)])
        ax.set_title("Inventory Status Distribution")
        ax.set_xlabel("Status")
        ax.set_ylabel("Asset Count")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle=":", alpha=0.35)
        for index, value in enumerate(values):
            ax.text(index, value + 0.4, str(value), ha="center", va="bottom", fontsize=10)
        fig.tight_layout()
        fig.savefig(output, dpi=160)
        plt.close(fig)
        return output

    output.write_text(_render_svg(labels, values), encoding="utf-8")
    return output


def _render_svg(labels: list[str], values: list[int]) -> str:
    width, height = 920, 520
    left, right, top, bottom = 80, 30, 70, 95
    chart_width = width - left - right
    chart_height = height - top - bottom
    max_value = max(values or [1])
    bar_gap = 18
    bar_width = (chart_width - bar_gap * max(0, len(values) - 1)) / max(1, len(values))
    colors = ["#2f6f4e", "#c75643", "#d7a22a", "#7b68aa", "#2f6f88", "#777777"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="80" y="42" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#1f2933">Inventory Status Distribution</text>',
        f'<line x1="{left}" y1="{top + chart_height}" x2="{width - right}" y2="{top + chart_height}" stroke="#9aa4af" stroke-width="1"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" stroke="#9aa4af" stroke-width="1"/>',
    ]
    for tick in range(0, max_value + 1, max(1, max_value // 4)):
        y = top + chart_height - (tick / max_value * chart_height)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="#d8dee6" stroke-width="1" stroke-dasharray="3 5"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#56616f">{tick}</text>')

    for index, (label, value) in enumerate(zip(labels, values)):
        x = left + index * (bar_width + bar_gap)
        bar_height = value / max_value * chart_height
        y = top + chart_height - bar_height
        color = colors[index % len(colors)]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="{color}" rx="3"/>')
        parts.append(f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#1f2933">{value}</text>')
        parts.append(f'<text x="{x + bar_width / 2:.1f}" y="{top + chart_height + 28}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#1f2933">{label}</text>')
    parts.append('<text x="20" y="285" transform="rotate(-90 20 285)" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#56616f">Asset count</text>')
    parts.append("</svg>")
    return "\n".join(parts)
