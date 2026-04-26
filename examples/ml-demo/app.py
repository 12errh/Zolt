"""
Zeno Example — ML Model Inference UI

Run with: zeno run examples/ml-demo/app.py
"""

import random

from pyui import (
    Alert, App, Badge, Button, Chart, Flex, Grid,
    Heading, Page, Select, Slider, Stat, Text, reactive,
)

# ── Mock model ────────────────────────────────────────────────────────────────


def _predict(model: str, threshold: float) -> dict:
    random.seed(hash(model))
    accuracy  = round(random.uniform(0.82, 0.97), 3)
    precision = round(random.uniform(0.80, 0.96), 3)
    recall    = round(random.uniform(0.78, 0.95), 3)
    f1        = round(2 * precision * recall / (precision + recall), 3)
    return {
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1,
        "above_threshold": accuracy >= threshold,
    }


# ── Shared state ──────────────────────────────────────────────────────────────

_selected_model = reactive("bert-base")
_threshold      = reactive(0.90)
_ran            = reactive(False)
_results: dict  = {}


def _run_inference() -> None:
    global _results
    _results = _predict(_selected_model.get(), _threshold.get())
    _ran.set(True)


# ── Pages ─────────────────────────────────────────────────────────────────────


class InferencePage(Page):
    title = "ML Inference Demo"
    route = "/"

    def compose(self) -> None:
        with Flex(direction="col", gap=8).className("max-w-3xl mx-auto py-12 px-4"):
            with Flex(align="center", gap=3):
                Heading("ML Inference Demo", level=1)
                Badge("PyUI Example", variant="secondary")

            Text(
                "Select a model, set a confidence threshold, and run inference "
                "to see performance metrics."
            ).style("muted").paragraph()

            with Flex(direction="col", gap=4).className(
                "bg-white border border-gray-100 rounded-2xl p-6 shadow-sm"
            ):
                Heading("Configuration", level=3)
                Select(
                    options=[
                        ("bert-base",   "BERT Base"),
                        ("bert-large",  "BERT Large"),
                        ("roberta",     "RoBERTa"),
                        ("distilbert",  "DistilBERT"),
                    ],
                    value=_selected_model,
                    label="Model",
                ).onChange(lambda: None)

                Slider(
                    value=_threshold,
                    min=0.5, max=1.0, step=0.01,
                    label=lambda: f"Confidence Threshold: {_threshold.get():.2f}",
                )

                Button("Run Inference").style("primary").size("lg").onClick(_run_inference)

            if _ran.get() and _results:
                r = _results
                status = "success" if r["above_threshold"] else "warning"
                Alert(
                    "Model meets threshold." if r["above_threshold"] else "Below threshold.",
                    variant=status,
                )
                with Grid(cols=4, gap=4):
                    Stat("Accuracy",  f"{r['accuracy']:.1%}")
                    Stat("Precision", f"{r['precision']:.1%}")
                    Stat("Recall",    f"{r['recall']:.1%}")
                    Stat("F1 Score",  f"{r['f1']:.1%}")

                Chart(
                    type="bar",
                    labels=["Accuracy", "Precision", "Recall", "F1"],
                    datasets=[{
                        "label": _selected_model.get(),
                        "data": [
                            round(r["accuracy"]  * 100, 1),
                            round(r["precision"] * 100, 1),
                            round(r["recall"]    * 100, 1),
                            round(r["f1"]        * 100, 1),
                        ],
                        "backgroundColor": "#6C63FF",
                    }],
                )


# ── App ───────────────────────────────────────────────────────────────────────


class MLDemoApp(App):
    name = "ML Inference Demo"
    theme = "light"

    selected_model = _selected_model
    threshold      = _threshold
    ran            = _ran

    home = InferencePage()
