import vertexai
from vertexai.generative_models import GenerativeModel
import logging
from typing import Tuple, List
from armoriq_service import verify_ai_action

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.model_name = "gemini-1.5-pro"

        vertexai.init(project=project_id, location=location)

        # ✅ Initialize once (performance boost)
        self.model = GenerativeModel(self.model_name)

    def generate_explanation_and_recommendations(
        self,
        user_id: str,
        metrics: dict,
        protected_attributes: list,
        outcome_column: str,
        overall_score: float
    ) -> Tuple[str, List[str], bool]:

        try:
            # 🔐 STEP 1 — ARMORIQ VERIFICATION
            verification = verify_ai_action(
                user_id,
                {
                    "metrics": metrics,
                    "score": overall_score
                }
            )

            if not verification or not verification.get("allowed", False):
                logger.warning("ArmorIQ blocked AI action")

                return (
                    "AI explanation blocked due to policy restrictions.",
                    ["Check access permissions", "Review policy settings"],
                    False
                )

            # ✅ STEP 2 — FORMAT METRICS PROPERLY
            metrics_summary = self._format_metrics_for_prompt(
                metrics,
                protected_attributes
            )

            # ✅ STEP 3 — STRONG PROMPT
            prompt = f"""
You are an AI fairness expert.

Fairness Score: {overall_score}/100
Protected Attributes: {', '.join(protected_attributes)}
Outcome Column: {outcome_column}

Metrics:
{metrics_summary}

Task:
1. Explain bias in simple language (2-3 lines)
2. Identify if unfair treatment exists
3. Give 3-5 clear actionable fixes

Format:
EXPLANATION:
...

RECOMMENDATIONS:
1. ...
2. ...
"""

            # ✅ STEP 4 — GEMINI CALL
            response = self.model.generate_content(prompt)

            explanation, recommendations = self._parse_response(response.text)

            return explanation, recommendations, True

        except Exception as e:
            logger.error(f"Gemini failed: {str(e)}", exc_info=True)

            return (
                self._fallback_explanation(overall_score),
                self._fallback_recommendations(),
                False
            )

    # ---------------- HELPERS ----------------

    def _format_metrics_for_prompt(self, metrics, protected_attributes):
        lines = []

        for attr in protected_attributes:
            dp = metrics.get("demographic_parity_difference", {}).get(attr, 0)
            eo = metrics.get("equal_opportunity_difference", {}).get(attr, 0)
            eod = metrics.get("equalized_odds_difference", {}).get(attr, 0)

            lines.append(
                f"{attr} → DP: {dp:.3f}, EO: {eo:.3f}, EOD: {eod:.3f}"
            )

        return "\n".join(lines)

    def _parse_response(self, text: str) -> Tuple[str, List[str]]:
        try:
            explanation = ""
            recommendations = []

            if "EXPLANATION:" in text and "RECOMMENDATIONS:" in text:
                exp_part = text.split("EXPLANATION:")[1].split("RECOMMENDATIONS:")[0]
                rec_part = text.split("RECOMMENDATIONS:")[1]

                explanation = exp_part.strip()

                for line in rec_part.split("\n"):
                    line = line.strip()
                    if line and line[0].isdigit():
                        recommendations.append(line.split(".", 1)[1].strip())

            return explanation, recommendations[:5]

        except:
            return text[:200], ["Improve data quality", "Retrain model"]

    def _fallback_explanation(self, score: float) -> str:
        if score < 40:
            return "Significant bias detected across groups."
        elif score < 70:
            return "Moderate bias detected."
        return "System appears relatively fair."

    def _fallback_recommendations(self) -> List[str]:
        return [
            "Balance dataset",
            "Retrain model",
            "Adjust decision thresholds",
            "Monitor fairness regularly",
            "Audit periodically"
        ]