"""
Audit endpoint - main API for running fairness audits.
Orchestrates the complete audit pipeline.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd
import io
import logging
from datetime import datetime
import uuid

from app.config import get_settings
from app.services.fairness_engine import FairnessEngine
from app.services.gcs_service import GCSService
from app.services.firestore_service import FirestoreService
from app.services.gemini_service import GeminiService
from app.utils.validators import DataValidator

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.post("/audit")
async def run_audit(
    file: UploadFile = File(...),
    protected_attributes: List[str] = None,
    outcome_column: str = None,
    positive_outcome_value: str = None,
    user_id: str = None
):
    audit_id = None
    gcs_path = None

    try:
        # ✅ Validate inputs
        if not protected_attributes or not outcome_column or not user_id:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: protected_attributes, outcome_column, user_id"
            )

        # ✅ Read file
        contents = await file.read()
        file_ext = file.filename.split(".")[-1].lower()

        try:
            if file_ext == "csv":
                df = pd.read_csv(io.BytesIO(contents))
            elif file_ext in ["xlsx", "xls"]:
                df = pd.read_excel(io.BytesIO(contents))
            elif file_ext == "json":
                df = pd.read_json(io.BytesIO(contents))
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format: {file_ext}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse file: {str(e)}"
            )

        # ✅ Validate dataset
        is_valid, error_msg = DataValidator.validate_dataset(
            df,
            protected_attributes,
            outcome_column
        )

        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # ✅ Clean dataset
        critical_cols = protected_attributes + [outcome_column]
        df_clean = DataValidator.clean_dataset(df, critical_cols)

        logger.info(f"Dataset cleaned: {len(df_clean)} rows")

        # ✅ Initialize services
        gcs_service = GCSService(settings.GCS_BUCKET_NAME, settings.PROJECT_ID)
        firestore_service = FirestoreService(settings.PROJECT_ID)
        gemini_service = GeminiService(settings.PROJECT_ID)
        fairness_engine = FairnessEngine()

        # ✅ Upload to GCS
        audit_id = str(uuid.uuid4())
        gcs_path = f"audits/{datetime.utcnow().strftime('%Y/%m/%d')}/{audit_id}/{file.filename}"

        gcs_service.upload_file(
            contents,
            gcs_path,
            content_type=f"text/{file_ext}"
        )

        logger.info(f"Uploaded to GCS: {gcs_path}")

        # ✅ Compute fairness metrics
        metrics = fairness_engine.compute_fairness_metrics(
            df_clean,
            protected_attributes,
            outcome_column,
            positive_outcome_value
        )

        overall_score = metrics.pop("overall_score")

        logger.info(f"Score: {overall_score:.1f}")

        # ✅ 🔐 Gemini + ArmorIQ (CORRECT INDENTATION)
        explanation, recommendations, verified = gemini_service.generate_explanation_and_recommendations(
            user_id=user_id,
            metrics=metrics,
            protected_attributes=protected_attributes,
            outcome_column=outcome_column,
            overall_score=overall_score
        )

        logger.info("Gemini + ArmorIQ executed")

        # ✅ Prepare result
        audit_result = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow(),
            "file_name": file.filename,
            "protected_attributes": protected_attributes,
            "outcome_column": outcome_column,
            "metrics": metrics,
            "overall_score": overall_score,
            "explanation": explanation,
            "recommendations": recommendations,
            "verified": verified,
            "gcs_file_path": gcs_path
        }

        # ✅ Save to Firestore
        firestore_service.save_audit_result(user_id, audit_result)

        logger.info(f"Saved audit: {audit_id}")

        # ✅ Final response
        return JSONResponse(
            status_code=200,
            content={
                "audit_id": audit_id,
                "timestamp": audit_result["timestamp"].isoformat(),
                "file_name": file.filename,
                "protected_attributes": protected_attributes,
                "outcome_column": outcome_column,
                "metrics": metrics,
                "overall_score": overall_score,
                "explanation": explanation,
                "recommendations": recommendations,
                "verified": verified,  # 🔥 IMPORTANT
                "gcs_file_path": gcs_path
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audit failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Audit pipeline failed: {str(e)}"
        )