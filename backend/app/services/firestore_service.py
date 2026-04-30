"""
Firestore database service for audit result persistence.
Handles audit history and result storage.
"""

from google.cloud import firestore
from typing import List, Dict, Optional
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class FirestoreService:
    """Manages Firestore database operations."""
    
    def __init__(self, project_id: str, database_id: str = "(default)"):
        """
        Initialize Firestore service.
        
        Args:
            project_id: GCP project ID
            database_id: Firestore database ID
        """
        self.client = firestore.Client(project=project_id, database=database_id)
    
    def save_audit_result(
        self,
        user_id: str,
        audit_data: Dict
    ) -> str:
        """
        Save audit result to Firestore.
        
        Args:
            user_id: Firebase user ID
            audit_data: Audit result dictionary
            
        Returns:
            Audit ID
        """
        try:
            audit_id = str(uuid.uuid4())
            
            # Create audit document
            audit_doc = {
                "audit_id": audit_id,
                "user_id": user_id,
                "timestamp": datetime.utcnow(),
                "file_name": audit_data.get("file_name"),
                "protected_attributes": audit_data.get("protected_attributes", []),
                "outcome_column": audit_data.get("outcome_column"),
                "metrics": audit_data.get("metrics", {}),
                "overall_score": audit_data.get("overall_score", 0),
                "explanation": audit_data.get("explanation", ""),
                "recommendations": audit_data.get("recommendations", []),
                "gcs_file_path": audit_data.get("gcs_file_path", ""),
            }
            
            # Save to collection
            self.client.collection("audits").document(audit_id).set(audit_doc)
            
            logger.info(f"Saved audit {audit_id} for user {user_id}")
            return audit_id
            
        except Exception as e:
            logger.error(f"Failed to save audit: {str(e)}")
            raise
    
    def get_user_audits(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Retrieve all audits for a user.
        
        Args:
            user_id: Firebase user ID
            limit: Maximum number of audits to return
            
        Returns:
            List of audit documents
        """
        try:
            query = (
                self.client.collection("audits")
                .where("user_id", "==", user_id)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            
            docs = query.stream()
            audits = [doc.to_dict() for doc in docs]
            
            logger.info(f"Retrieved {len(audits)} audits for user {user_id}")
            return audits
            
        except Exception as e:
            logger.error(f"Failed to retrieve audits: {str(e)}")
            raise
    
    def get_audit_by_id(self, audit_id: str) -> Optional[Dict]:
        """
        Retrieve specific audit by ID.
        
        Args:
            audit_id: Audit ID
            
        Returns:
            Audit document or None
        """
        try:
            doc = self.client.collection("audits").document(audit_id).get()
            
            if doc.exists:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve audit {audit_id}: {str(e)}")
            raise
    
    def delete_audit(self, audit_id: str) -> bool:
        """
        Delete audit from Firestore.
        
        Args:
            audit_id: Audit ID
            
        Returns:
            True if successful
        """
        try:
            self.client.collection("audits").document(audit_id).delete()
            logger.info(f"Deleted audit {audit_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete audit: {str(e)}")
            raise