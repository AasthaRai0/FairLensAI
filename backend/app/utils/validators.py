"""
Validation utilities for dataset and configuration.
Ensures data quality before processing.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates datasets for fairness auditing."""
    
    @staticmethod
    def validate_dataset(
        df: pd.DataFrame,
        protected_attributes: List[str],
        outcome_column: str
    ) -> Tuple[bool, str]:
        """
        Validate dataset for fairness analysis.
        
        Args:
            df: Pandas DataFrame
            protected_attributes: List of protected attribute column names
            outcome_column: Target outcome column name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        # Check if DataFrame is empty
        if df.empty:
            return False, "Dataset is empty"
        
        # Check minimum rows
        if len(df) < 30:
            return False, f"Dataset must have at least 30 rows, got {len(df)}"
        
        # Check outcome column exists
        if outcome_column not in df.columns:
            return False, f"Outcome column '{outcome_column}' not found"
        
        # Check all protected attributes exist
        missing_attrs = [attr for attr in protected_attributes if attr not in df.columns]
        if missing_attrs:
            return False, f"Missing columns: {', '.join(missing_attrs)}"
        
        # Check for sufficient variation in protected attributes
        for attr in protected_attributes:
            unique_values = df[attr].nunique()
            if unique_values < 2:
                return False, f"Protected attribute '{attr}' must have at least 2 distinct values"
        
        # Check for missing values in critical columns
        critical_cols = protected_attributes + [outcome_column]
        missing_pct = df[critical_cols].isnull().sum() / len(df) * 100
        
        for col, pct in missing_pct.items():
            if pct > 10:
                return False, f"Column '{col}' has {pct:.1f}% missing values"
        
        # Check outcome column has binary or categorical outcome
        outcome_unique = df[outcome_column].nunique()
        if outcome_unique > 10:
            return False, f"Outcome column has too many unique values ({outcome_unique})"
        
        logger.info(f"Dataset validation passed: {len(df)} rows, {len(df.columns)} columns")
        return True, ""
    
    @staticmethod
    def clean_dataset(df: pd.DataFrame, critical_cols: List[str]) -> pd.DataFrame:
        """
        Clean dataset by removing rows with missing critical values.
        
        Args:
            df: DataFrame to clean
            critical_cols: Columns that must have values
            
        Returns:
            Cleaned DataFrame
        """
        initial_size = len(df)
        df_clean = df.dropna(subset=critical_cols)
        removed = initial_size - len(df_clean)
        
        if removed > 0:
            logger.info(f"Removed {removed} rows with missing critical values")
        
        return df_clean