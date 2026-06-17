from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


def write_reports(scored_designs: List[Dict], top_designs: List[Dict], output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    (out / "report.json").write_text(
        json.dumps(
            {
                "total_designs": len(scored_designs),
                "top_10": top_designs,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    if not scored_designs:
        return

    fieldnames = list(scored_designs[0].keys())
    with (out / "designs.csv").open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_designs)
