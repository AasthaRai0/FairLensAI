"""
Fairness metrics computation engine.
Uses fairlearn library to compute demographic parity, equalized odds, etc.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from fairlearn.metrics import (
    demographic_parity_difference,
    equalized_odds_difference,
    true_positive_rate_difference,
)
import logging

logger = logging.getLogger(__name__)


class FairnessEngine:
    """Computes fairness metrics on datasets."""

    def __init__(self):
        self.metrics_cache = {}

    def compute_fairness_metrics(
        self,
        df: pd.DataFrame,
        protected_attributes: list,
        outcome_column: str,
        positive_outcome_value: any = None,
    ) -> Dict:
        """
        Compute comprehensive fairness metrics.

        Args:
            df: DataFrame with outcome and protected attributes
            protected_attributes: List of protected attribute columns
            outcome_column: Target outcome column
            positive_outcome_value: Value representing positive outcome

        Returns:
            Dictionary with computed metrics
        """

        # Convert outcome to binary if not already
        y_true = self._prepare_binary_outcome(
            df[outcome_column], positive_outcome_value
        )

        metrics = {
            "demographic_parity_difference": {},
            "equalized_odds_difference": {},
            "equal_opportunity_difference": {},
            "raw_metrics": {},
        }

        # Compute metrics for each protected attribute
        for attr in protected_attributes:
            group_labels = df[attr]

            try:
                # Demographic Parity Difference
                dp_diff = demographic_parity_difference(
                    y_true,
                    y_true,  # Using ground truth as predictions for audit
                    sensitive_features=group_labels,
                )
                metrics["demographic_parity_difference"][attr] = float(dp_diff)

                # Equalized Odds Difference
                eod_diff = equalized_odds_difference(
                    y_true, y_true, sensitive_features=group_labels
                )
                metrics["equalized_odds_difference"][attr] = float(eod_diff)

                # Equal Opportunity Difference (TPR difference)
                tpr_diff = true_positive_rate_difference(
                    y_true, y_true, sensitive_features=group_labels
                )
                metrics["equal_opportunity_difference"][attr] = float(tpr_diff)

                # Store raw group statistics
                metrics["raw_metrics"][attr] = self._compute_group_statistics(
                    df, attr, y_true
                )

                logger.info(f"Computed metrics for attribute: {attr}")

            except Exception as e:
                logger.warning(f"Could not compute metrics for {attr}: {str(e)}")
                metrics["demographic_parity_difference"][attr] = 0.0
                metrics["equalized_odds_difference"][attr] = 0.0
                metrics["equal_opportunity_difference"][attr] = 0.0

        # Compute overall fairness score
        overall_score = self._compute_overall_score(metrics)
        metrics["overall_score"] = overall_score

        logger.info(f"Fairness audit complete. Overall score: {overall_score:.1f}/100")

        return metrics

    def _prepare_binary_outcome(
        self, outcome_series: pd.Series, positive_value: any = None
    ) -> pd.Series:
        """Convert outcome to binary (0/1)."""

        if positive_value is not None:
            return (outcome_series == positive_value).astype(int)

        # Auto-detect binary outcome
        unique_vals = outcome_series.unique()
        if len(unique_vals) == 2:
            # Map to binary
            sorted_vals = sorted(unique_vals)
            mapping = {sorted_vals[0]: 0, sorted_vals[1]: 1}
            return outcome_series.map(mapping).astype(int)

        # For multi-class, take first unique value as negative
        return (outcome_series != outcome_series.iloc[0]).astype(int)

    def _compute_group_statistics(
        self, df: pd.DataFrame, attribute: str, y_true: pd.Series
    ) -> Dict:
        """Compute selection rate and other stats per group."""

        stats = {}
        for group in df[attribute].unique():
            group_mask = df[attribute] == group
            group_outcomes = y_true[group_mask]

            stats[str(group)] = {
                "size": int(group_mask.sum()),
                "positive_rate": float(group_outcomes.mean()),
                "positive_count": int(group_outcomes.sum()),
            }

        return stats

    def _compute_overall_score(self, metrics: Dict) -> float:
        """
        Compute overall fairness score (0-100).

        Lower disparity = higher score.
        Score formula: 100 - (average_disparity * 100)
        """

        all_disparities = []

        # Collect all disparity values
        for attr_disparities in metrics["demographic_parity_difference"].values():
            all_disparities.append(abs(attr_disparities))

        for attr_disparities in metrics["equalized_odds_difference"].values():
            all_disparities.append(abs(attr_disparities))

        for attr_disparities in metrics["equal_opportunity_difference"].values():
            all_disparities.append(abs(attr_disparities))

        if not all_disparities:
            return 100.0

        # Average absolute disparity
        avg_disparity = np.mean(all_disparities)

        # Clamp to 0-1 range and convert to score
        avg_disparity = min(avg_disparity, 1.0)
        score = 100 - (avg_disparity * 100)

        return float(score)

    def get_score_level(self, score: float) -> str:
        """Determine score level (Red/Yellow/Green)."""

        if score <= 40:
            return "red"
        elif score <= 70:
            return "yellow"
        else:
            return "green"
