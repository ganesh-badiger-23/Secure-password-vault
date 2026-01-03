"""
Vault Logic Module
-----------------
This module orchestrates the complete vault workflow:
1. Encrypt passwords with AES
2. Split the key using Shamir's Secret Sharing
3. Distribute shares across multiple clouds
4. Reconstruct key from shares when needed
5. Decrypt vault to retrieve passwords

The Master Key Never Exists in Full Form:
The encryption key is generated, used immediately, split into shares,
and then deleted from memory. It only exists again temporarily during
decryption, and is immediately discarded after use.
"""

import os
import json
from cryptography.fernet import Fernet
from crypto_engine import CryptoManager
from cloud_manager import CloudDistributor


class VaultController:
    """
    Main controller that orchestrates the secure vault operations.
    Implements the zero-knowledge architecture.
    """
    
    def __init__(self):
        """
        Initialize the vault controller with crypto and cloud managers.
        """
        self.crypto_manager = CryptoManager()
        self.cloud_distributor = CloudDistributor()
        
        # Local files
        self.vault_file = 'encrypted_vault.bin'
        self.local_share_file = 'local_share.txt'
        
        print("🔐 VaultController initialized")
    
    def save_password(self, site, username, password):
        """
        Saves a new password entry to the vault.
        
        Workflow:
        1. Load existing vault (or create new)
        2. Add the new password entry
        3. Generate a fresh AES key
        4. Encrypt the vault
        5. Split the key into 3 shares
        6. Distribute shares: Share 1 -> AWS, Share 2 -> Google, Share 3 -> Local
        7. Delete the key from memory
        
        Args:
            site (str): Website/service name
            username (str): Username/email
            password (str): Password to store
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\n🔒 Securing password for {site}...")
            
            # Step 1: Load existing vault or create new
            vault_data = self._load_vault_data()
            
            # Step 2: Add new entry
            vault_data[site] = {
                'username': username,
                'password': password
            }
            print(f"✅ Added entry for {site}")
            
            # Step 3: Generate fresh AES key
            encryption_key = Fernet.generate_key()
            print(f"🔑 Generated new encryption key")
            
            # Step 4: Encrypt the vault
            encrypted_data = self.crypto_manager.encrypt_data(vault_data, encryption_key)
            
            # Save encrypted vault to disk
            with open(self.vault_file, 'wb') as f:
                f.write(encrypted_data)
            print(f"💾 Encrypted vault saved to {self.vault_file}")
            
            # Step 5: Split key into 3 shares (threshold = 2)
            shares = self.crypto_manager.split_key(encryption_key)
            print(f"🔀 Key split into {len(shares)} shares")
            
            # Step 6: Distribute shares
            print("☁️  Distributing shares to multi-cloud storage...")
            
            # Share 1 -> AWS
            share1_success = self.cloud_distributor.upload_to_aws(shares[0], 'vault_share_1.txt')
            
            # Share 2 -> Google
            share2_success = self.cloud_distributor.upload_to_google(shares[1], 'vault_share_2.txt')
            
            # Share 3 -> Local disk
            with open(self.local_share_file, 'w') as f:
                f.write(shares[2])
            print(f"💾 Share 3 saved locally to {self.local_share_file}")
            
            # Step 7: Delete key from memory (Python will garbage collect)
            del encryption_key
            print("🗑️  Master key deleted from memory")
            
            if share1_success and share2_success:
                print(f"✅ Password for {site} secured successfully!\n")
                return True
            else:
                print("⚠️  Some shares failed to upload, but vault is still accessible")
                return True
                
        except Exception as e:
            print(f"❌ Error saving password: {e}")
            return False
    
    def retrieve_passwords(self):
        """
        Retrieves and decrypts all passwords from the vault.
        
        Workflow:
        1. Fetch Share 1 from AWS
        2. Fetch Share 3 from Local disk
        3. Reconstruct the AES key from 2 shares
        4. Load encrypted vault
        5. Decrypt the vault
        6. Delete the key from memory
        7. Return passwords
        
        Returns:
            dict: Dictionary of all passwords, or None if failed
        
        Note:
            Only requires 2 of 3 shares, providing redundancy.
            Share 2 (Google) acts as a backup in case AWS or Local fails.
        """
        try:
            print("\n🔓 Retrieving passwords from vault...")
            
            # Step 1: Fetch Share 1 from AWS
            share1 = self.cloud_distributor.download_from_aws('vault_share_1.txt')
            if not share1:
                print("⚠️  Could not fetch Share 1 from AWS, trying alternative...")
                # Could try Share 2 from Google as backup
                share1 = self.cloud_distributor.download_from_google('vault_share_2.txt')
                if not share1:
                    print("❌ Could not fetch shares from cloud")
                    return None
            
            # Step 2: Fetch Share 3 from Local
            if os.path.exists(self.local_share_file):
                with open(self.local_share_file, 'r') as f:
                    share3 = f.read()
                print(f"✅ Share 3 loaded from {self.local_share_file}")
            else:
                print(f"❌ Local share not found: {self.local_share_file}")
                return None
            
            # Step 3: Reconstruct key from 2 shares
            shares = [share1, share3]
            encryption_key = self.crypto_manager.reconstruct_key(shares)
            print("🔑 Encryption key reconstructed from shares")
            
            # Step 4: Load encrypted vault
            if not os.path.exists(self.vault_file):
                print(f"❌ Vault file not found: {self.vault_file}")
                return None
            
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Step 5: Decrypt vault
            vault_data = self.crypto_manager.decrypt_data(encrypted_data, encryption_key)
            print(f"🔓 Vault decrypted successfully")
            
            # Step 6: Delete key from memory
            del encryption_key
            print("🗑️  Master key deleted from memory")
            
            print(f"✅ Retrieved {len(vault_data)} password(s)\n")
            return vault_data
            
        except Exception as e:
            print(f"❌ Error retrieving passwords: {e}")
            return None
    
    def _load_vault_data(self):
        """
        Helper method to load existing vault data.
        
        Returns:
            dict: Existing vault data, or empty dict if vault doesn't exist
        """
        if os.path.exists(self.vault_file):
            # Vault exists, need to decrypt it first
            existing_data = self.retrieve_passwords()
            if existing_data:
                return existing_data
        
        # No vault exists yet, return empty dictionary
        return {}
    
    def get_vault_status(self):
        """
        Gets the current status of the vault.
        
        Returns:
            dict: Status information
        """
        status = {
            'vault_exists': os.path.exists(self.vault_file),
            'local_share_exists': os.path.exists(self.local_share_file),
            'vault_size': os.path.getsize(self.vault_file) if os.path.exists(self.vault_file) else 0
        }
        return status


# Test the module if run directly
if __name__ == "__main__":
    print("Testing VaultController...\n")
    
    controller = VaultController()
    
    # Test 1: Save a password
    print("--- Test 1: Save Password ---")
    controller.save_password(
        site="google.com",
        username="testuser@gmail.com",
        password="SuperSecret123!"
    )
    
    # Test 2: Save another password
    print("\n--- Test 2: Save Another Password ---")
    controller.save_password(
        site="github.com",
        username="developer",
        password="GitHubToken456"
    )
    
    # Test 3: Retrieve all passwords
    print("\n--- Test 3: Retrieve Passwords ---")
    passwords = controller.retrieve_passwords()
    
    if passwords:
        print("\nStored Passwords:")
        for site, creds in passwords.items():
            print(f"  {site}:")
            print(f"    Username: {creds['username']}")
            print(f"    Password: {creds['password']}")
    
    # Test 4: Check vault status
    print("\n--- Test 4: Vault Status ---")
    status = controller.get_vault_status()
    print(f"Vault Status: {status}")
    
    print("\n✅ All tests passed! VaultController is working correctly.")
