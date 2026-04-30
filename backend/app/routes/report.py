"""
Report endpoint - generates PDF reports.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import logging
import io

from app.services.firestore_service import FirestoreService
from app.services.pdf_service import PDFService
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("/report/{audit_id}")
async def generate_report(audit_id: str):
    """
    Generate and download PDF report for audit.
    
    Args:
        audit_id: Audit ID
        
    Returns:
        PDF file stream
    """
    
    try:
        # Retrieve audit from Firestore
        firestore_service = FirestoreService(settings.PROJECT_ID)
        audit_data = firestore_service.get_audit_by_id(audit_id)
        
        if not audit_data:
            raise HTTPException(
                status_code=404,
                detail=f"Audit {audit_id} not found"
            )
        
        # Generate PDF
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generate_report(audit_data)
        
        logger.info(f"Generated PDF report for audit {audit_id}")
        
        # Return as streaming response
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=audit_{audit_id}.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate PDF report"
        )