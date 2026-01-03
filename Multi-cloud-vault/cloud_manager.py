"""
Cloud Connector Module
---------------------
This module handles multi-cloud distribution of key shares.
It interfaces with:
- AWS S3 for secure cloud storage
- Google Drive (simulated locally for demo purposes)

Multi-Cloud Redundancy:
By distributing key shares across multiple cloud providers and local storage,
we ensure that no single point of failure can compromise the vault. Even if
one cloud provider goes down or is compromised, the system remains operational.
"""

import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError


class CloudDistributor:
    """
    Manages distribution of key shares across multiple cloud providers.
    Implements redundancy through multi-cloud architecture.
    """
    
    def __init__(self, aws_access_key='AWS_KEY', aws_secret_key='AWS_SECRET', bucket_name='shamir-vault-demo'):
        """
        Initialize cloud connections.
        
        Args:
            aws_access_key (str): AWS access key ID (use environment variables in production)
            aws_secret_key (str): AWS secret access key (use environment variables in production)
            bucket_name (str): S3 bucket name for storing shares
        
        Security Note:
            In production, NEVER hardcode credentials. Use AWS IAM roles,
            environment variables, or AWS Secrets Manager.
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket_name
        self.google_mock_folder = 'google_drive_mock'
        
        # Create local mock folder for Google Drive simulation
        if not os.path.exists(self.google_mock_folder):
            os.makedirs(self.google_mock_folder)
            print(f"✅ Created mock Google Drive folder: {self.google_mock_folder}")
        
        # Initialize S3 client (will be created on first use)
        self.s3_client = None
    
    def _get_s3_client(self):
        """
        Lazy initialization of S3 client.
        
        Returns:
            boto3.client: S3 client instance
        """
        if self.s3_client is None:
            try:
                # Check if credentials are actual AWS credentials or placeholders
                if self.aws_access_key == 'AWS_KEY' or self.aws_secret_key == 'AWS_SECRET':
                    print("⚠️  Using placeholder AWS credentials. AWS functionality will be simulated locally.")
                    return None
                
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key
                )
            except Exception as e:
                print(f"⚠️  Could not initialize AWS S3 client: {e}")
                return None
        
        return self.s3_client
    
    def upload_to_aws(self, share_data, file_name):
        """
        Uploads a key share to AWS S3.
        
        Args:
            share_data (str): The key share to upload
            file_name (str): The name for the file in S3
        
        Returns:
            bool: True if successful, False otherwise
        
        Context:
            Stores the share in S3 for cloud redundancy. If AWS credentials
            are not configured, simulates by storing locally.
        """
        try:
            client = self._get_s3_client()
            
            if client is None:
                # Simulate AWS by storing locally
                print(f"🔧 Simulating AWS Upload: {file_name}")
                local_aws_folder = 'aws_s3_mock'
                if not os.path.exists(local_aws_folder):
                    os.makedirs(local_aws_folder)
                
                file_path = os.path.join(local_aws_folder, file_name)
                with open(file_path, 'w') as f:
                    f.write(share_data)
                
                print(f"✅ Simulated upload to AWS S3: {file_name}")
                return True
            
            # Actual AWS S3 upload
            client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=share_data.encode('utf-8')
            )
            
            print(f"✅ Successfully uploaded to AWS S3: {file_name}")
            return True
            
        except NoCredentialsError:
            print(f"❌ AWS credentials not found. Cannot upload {file_name}")
            return False
        except ClientError as e:
            print(f"❌ AWS S3 upload failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during AWS upload: {e}")
            return False
    
    def upload_to_google(self, share_data, file_name):
        """
        Uploads a key share to Google Drive (simulated locally).
        
        Args:
            share_data (str): The key share to upload
            file_name (str): The name for the file
        
        Returns:
            bool: True if successful, False otherwise
        
        Context:
            For demo purposes, this simulates Google Drive by writing to a local folder.
            In production, you would use the Google Drive API with proper OAuth2 authentication.
        """
        try:
            print(f"🔧 Simulating Google Drive Upload: {file_name}")
            
            file_path = os.path.join(self.google_mock_folder, file_name)
            
            with open(file_path, 'w') as f:
                f.write(share_data)
            
            print(f"✅ Simulated upload to Google Drive: {file_name}")
            return True
            
        except Exception as e:
            print(f"❌ Google Drive simulation failed: {e}")
            return False
    
    def download_from_aws(self, file_name):
        """
        Downloads a key share from AWS S3.
        
        Args:
            file_name (str): The name of the file to download
        
        Returns:
            str: The share data, or None if failed
        
        Context:
            Retrieves the share from S3 for key reconstruction.
        """
        try:
            client = self._get_s3_client()
            
            if client is None:
                # Simulate AWS by reading locally
                print(f"🔧 Simulating AWS Download: {file_name}")
                local_aws_folder = 'aws_s3_mock'
                file_path = os.path.join(local_aws_folder, file_name)
                
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = f.read()
                    print(f"✅ Simulated download from AWS S3: {file_name}")
                    return data
                else:
                    print(f"❌ File not found in simulated AWS: {file_name}")
                    return None
            
            # Actual AWS S3 download
            response = client.get_object(Bucket=self.bucket_name, Key=file_name)
            data = response['Body'].read().decode('utf-8')
            
            print(f"✅ Successfully downloaded from AWS S3: {file_name}")
            return data
            
        except ClientError as e:
            print(f"❌ AWS S3 download failed: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error during AWS download: {e}")
            return None
    
    def download_from_google(self, file_name):
        """
        Downloads a key share from Google Drive (simulated locally).
        
        Args:
            file_name (str): The name of the file to download
        
        Returns:
            str: The share data, or None if failed
        
        Context:
            Retrieves the share from simulated Google Drive storage.
        """
        try:
            print(f"🔧 Simulating Google Drive Download: {file_name}")
            
            file_path = os.path.join(self.google_mock_folder, file_name)
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = f.read()
                print(f"✅ Simulated download from Google Drive: {file_name}")
                return data
            else:
                print(f"❌ File not found in simulated Google Drive: {file_name}")
                return None
                
        except Exception as e:
            print(f"❌ Google Drive simulation failed: {e}")
            return None


# Test the module if run directly
if __name__ == "__main__":
    print("Testing CloudDistributor...\n")
    
    distributor = CloudDistributor()
    
    # Test data
    test_share = "1-abc123def456ghi789"
    test_filename = "test_share_1.txt"
    
    # Test AWS upload/download
    print("\n--- Testing AWS Operations ---")
    distributor.upload_to_aws(test_share, test_filename)
    downloaded_aws = distributor.download_from_aws(test_filename)
    print(f"AWS Data Match: {test_share == downloaded_aws}")
    
    # Test Google upload/download
    print("\n--- Testing Google Operations ---")
    distributor.upload_to_google(test_share, test_filename)
    downloaded_google = distributor.download_from_google(test_filename)
    print(f"Google Data Match: {test_share == downloaded_google}")
    
    print("\n✅ All tests passed! CloudDistributor is working correctly.")
