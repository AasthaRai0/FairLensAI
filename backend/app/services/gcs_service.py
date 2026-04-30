"""
Google Cloud Storage service for dataset upload and retrieval.
Handles file operations in GCS with proper error handling.
"""

from google.cloud import storage
from typing import Optional
import logging
import io
import pandas as pd

logger = logging.getLogger(__name__)


class GCSService:
    """Manages file uploads and downloads from Google Cloud Storage."""
    
    def __init__(self, bucket_name: str, project_id: str):
        """
        Initialize GCS service.
        
        Args:
            bucket_name: GCS bucket name
            project_id: GCP project ID
        """
        self.bucket_name = bucket_name
        self.client = storage.Client(project=project_id)
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(
        self,
        file_content: bytes,
        destination_path: str,
        content_type: str = "text/csv"
    ) -> str:
        """
        Upload file to GCS.
        
        Args:
            file_content: File bytes
            destination_path: GCS path (e.g., "audits/2024-01/file.csv")
            content_type: MIME type
            
        Returns:
            GCS file path
        """
        try:
            blob = self.bucket.blob(destination_path)
            blob.upload_from_string(
                file_content,
                content_type=content_type
            )
            
            logger.info(f"Uploaded file to gs://{self.bucket_name}/{destination_path}")
            return f"gs://{self.bucket_name}/{destination_path}"
            
        except Exception as e:
            logger.error(f"GCS upload failed: {str(e)}")
            raise
    
    def download_file(self, source_path: str) -> bytes:
        """
        Download file from GCS.
        
        Args:
            source_path: GCS path
            
        Returns:
            File bytes
        """
        try:
            blob = self.bucket.blob(source_path)
            content = blob.download_as_bytes()
            
            logger.info(f"Downloaded file from {source_path}")
            return content
            
        except Exception as e:
            logger.error(f"GCS download failed: {str(e)}")
            raise
    
    def load_dataframe(self, gcs_path: str) -> pd.DataFrame:
        """
        Load CSV file from GCS into DataFrame.
        
        Args:
            gcs_path: GCS path
            
        Returns:
            Pandas DataFrame
        """
        try:
            # Remove gs:// prefix if present
            if gcs_path.startswith("gs://"):
                path_parts = gcs_path.replace("gs://", "").split("/", 1)
                file_path = path_parts[1] if len(path_parts) > 1 else path_parts[0]
            else:
                file_path = gcs_path
            
            content = self.download_file(file_path)
            df = pd.read_csv(io.BytesIO(content))
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to load DataFrame from GCS: {str(e)}")
            raise
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists in GCS."""
        blob = self.bucket.blob(file_path)
        return blob.exists()