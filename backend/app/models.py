"""
Pydantic models for request/response validation.
Ensures type safety and automatic documentation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AuditRequest(BaseModel):
    """Request model for audit endpoint."""
    
    file_name: str = Field(..., description="Uploaded file name")
    protected_attributes: List[str] = Field(
        ..., 
        description="List of protected attribute column names",
        min_items=1
    )
    outcome_column: str = Field(
        ..., 
        description="Column name representing the outcome"
    )
    positive_outcome_value: Optional[Any] = Field(
        None, 
        description="Value representing positive outcome (e.g., 'Yes', 1)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "hiring_data.csv",
                "protected_attributes": ["gender", "race"],
                "outcome_column": "hired",
                "positive_outcome_value": "Yes"
            }
        }


class FairnessMetrics(BaseModel):
    """Fairness metrics computed from dataset."""
    
    demographic_parity_difference: Dict[str, float] = Field(
        ..., 
        description="DP difference per protected attribute"
    )
    equalized_odds_difference: Dict[str, float] = Field(
        ..., 
        description="EOD per protected attribute"
    )
    equal_opportunity_difference: Dict[str, float] = Field(
        ..., 
        description="Equal Opportunity difference per protected attribute"
    )
    overall_score: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Fairness score 0-100"
    )


class AuditResult(BaseModel):
    """Complete audit result."""
    
    audit_id: str
    timestamp: datetime
    file_name: str
    protected_attributes: List[str]
    outcome_column: str
    metrics: FairnessMetrics
    explanation: str = Field(..., description="Plain English explanation from Gemini")
    recommendations: List[str] = Field(
        ..., 
        description="Actionable recommendations"
    )
    gcs_file_path: str = Field(..., description="GCS path to uploaded dataset")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HistoryResponse(BaseModel):
    """Response for audit history."""
    
    audits: List[AuditResult]
    total_count: int


class HealthCheck(BaseModel):
    """Health check response."""
    
    status: str
    version: str
    timestamp: datetime