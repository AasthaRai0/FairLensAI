"""
History endpoint - retrieves past audit results.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.services.firestore_service import FirestoreService
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("/history")
async def get_audit_history(user_id: str, limit: int = 50):
    """
    Retrieve audit history for user.
    
    Args:
        user_id: Firebase user ID
        limit: Maximum number of audits to return
        
    Returns:
        List of past audits
    """
    
    try:
        firestore_service = FirestoreService(settings.PROJECT_ID)
        audits = firestore_service.get_user_audits(user_id, limit)
        
        # Convert datetime objects to ISO format
        for audit in audits:
            if "timestamp" in audit:
                audit["timestamp"] = audit["timestamp"].isoformat()
        
        return JSONResponse(
            status_code=200,
            content={
                "audits": audits,
                "total_count": len(audits)
            }
        )
    
    except Exception as e:
        logger.error(f"Failed to retrieve history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve audit history"
        )


@router.get("/audit/{audit_id}")
async def get_audit_detail(audit_id: str):
    """
    Retrieve specific audit details.
    
    Args:
        audit_id: Audit ID
        
    Returns:
        Audit details
    """
    
    try:
        firestore_service = FirestoreService(settings.PROJECT_ID)
        audit = firestore_service.get_audit_by_id(audit_id)
        
        if not audit:
            raise HTTPException(
                status_code=404,
                detail=f"Audit {audit_id} not found"
            )
        
        if "timestamp" in audit:
            audit["timestamp"] = audit["timestamp"].isoformat()
        
        return JSONResponse(
            status_code=200,
            content=audit
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve audit: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve audit details"
        )