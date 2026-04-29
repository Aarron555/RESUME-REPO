"""AXE-LAB v4 Streamlit dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RESULTS_PATH = Path("benchmarks/results.json")
STATS_PATH = Path("benchmarks/statistical_summary.json")


def _load_df() -> pd.DataFrame:
    payload = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    rows = []
    for r in payload["records"]:
        rows.append(
            {
                "model": r["model_name"],
                "system": r["system_type"],
                "task": r["task_type"],
                "run": r["run_id"],
                "success": int(r["success"]),
                "attempts": r["attempts_to_success"],
                "cost": r["total_cost"],
                "failure_count": len(r.get("failure_tags", [])),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    st.title("AXE-LAB v4 Dashboard")
    if not RESULTS_PATH.exists() or not STATS_PATH.exists():
        st.error("Run `python run.py` first.")
        return

    df = _load_df()
    selected_model = st.selectbox("Model comparison selector", sorted(df["model"].unique()))
    mdf = df[df["model"] == selected_model]

    st.subheader("Success rate bar chart")
    success_bar = mdf.groupby("system", as_index=False)["success"].mean()
    st.plotly_chart(px.bar(success_bar, x="system", y="success", color="system"), use_container_width=True)

    st.subheader("Cost vs success scatter plot")
    scatter_df = mdf.groupby(["system", "task"], as_index=False).agg({"cost": "mean", "success": "mean"})
    st.plotly_chart(px.scatter(scatter_df, x="cost", y="success", color="system", hover_name="task", size="success"), use_container_width=True)

    st.subheader("Retry distribution histogram")
    st.plotly_chart(px.histogram(mdf, x="attempts", color="system", barmode="group"), use_container_width=True)

    st.subheader("Cost efficiency comparison")
    cost_eff = mdf.groupby("system", as_index=False).agg(success_rate=("success", "mean"), cost_per_run=("cost", "mean"))
    cost_eff["cost_efficiency"] = cost_eff["success_rate"] / cost_eff["cost_per_run"].clip(lower=1e-9)
    st.plotly_chart(px.bar(cost_eff, x="system", y="cost_efficiency", color="system"), use_container_width=True)


if __name__ == "__main__":
    main()
