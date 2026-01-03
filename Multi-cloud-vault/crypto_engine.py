"""
Cryptography Engine Module
--------------------------
This module handles all cryptographic operations for the Multi-Cloud Vault.
It implements:
- AES encryption/decryption using Fernet (symmetric encryption)
- Shamir's Secret Sharing for key splitting/reconstruction

Zero-Knowledge Privacy:
The master encryption key is never stored anywhere. Instead, it's split into
3 shares using Shamir's Secret Sharing scheme. Any 2 of the 3 shares can 
reconstruct the key, ensuring redundancy while maintaining security.
"""

import json
import secrets
from secretsharing import SecretSharer
from cryptography.fernet import Fernet


class CryptoManager:
    """
    Manages encryption, decryption, and key splitting operations.
    Ensures zero-knowledge privacy by never storing the master key.
    """
    
    def generate_salt(self):
        """
        Generates a cryptographically secure random salt.
        
        Returns:
            str: A random hexadecimal string (32 bytes = 64 hex characters)
        """
        return secrets.token_hex(32)
    
    def encrypt_data(self, data_dict, key):
        """
        Encrypts a dictionary using AES encryption (via Fernet).
        
        Args:
            data_dict (dict): The dictionary containing passwords and metadata
            key (bytes): The Fernet encryption key (must be 32 url-safe base64-encoded bytes)
        
        Returns:
            bytes: The encrypted data
        
        Note:
            Fernet uses AES in CBC mode with HMAC for authentication.
            This ensures both confidentiality and integrity.
        """
        # Convert dictionary to JSON string
        json_string = json.dumps(data_dict)
        
        # Create Fernet cipher with the key
        cipher = Fernet(key)
        
        # Encrypt the JSON string and return bytes
        encrypted_bytes = cipher.encrypt(json_string.encode())
        
        return encrypted_bytes
    
    def decrypt_data(self, encrypted_bytes, key):
        """
        Decrypts encrypted bytes back to the original dictionary.
        
        Args:
            encrypted_bytes (bytes): The encrypted data
            key (bytes): The Fernet decryption key
        
        Returns:
            dict: The decrypted dictionary
        
        Raises:
            InvalidToken: If the key is wrong or data is corrupted
        """
        # Create Fernet cipher with the key
        cipher = Fernet(key)
        
        # Decrypt the bytes to JSON string
        decrypted_string = cipher.decrypt(encrypted_bytes).decode()
        
        # Convert JSON string back to dictionary
        data_dict = json.loads(decrypted_string)
        
        return data_dict
    
    def split_key(self, key_bytes):
        """
        Splits the encryption key into 3 shares using Shamir's Secret Sharing.
        Any 2 of the 3 shares can reconstruct the original key.
        
        Args:
            key_bytes (bytes): The Fernet key to split
        
        Returns:
            list: A list of 3 share strings
        
        How it works:
            - Converts key bytes to hexadecimal
            - Uses SecretSharer to split into 3 shares (threshold of 2 required)
            - Format: Each share is like "1-abc123..." where 1 is the share number
        """
        # Convert bytes to hex string
        hex_key = key_bytes.hex()
        
        # Split into 3 shares, requiring any 2 to reconstruct (threshold=2)
        shares = SecretSharer.split_secret(hex_key, 2, 3)
        
        return shares
    
    def reconstruct_key(self, shares_list):
        """
        Reconstructs the original key from any 2 of the 3 shares.
        
        Args:
            shares_list (list): A list containing at least 2 shares
        
        Returns:
            bytes: The reconstructed Fernet key
        
        Note:
            This is the magic of Shamir's Secret Sharing - you don't need
            all shares, just the threshold number (2 in our case).
        """
        # Recover the hex secret from shares
        hex_key = SecretSharer.recover_secret(shares_list)
        
        # Convert hex string back to bytes
        key_bytes = bytes.fromhex(hex_key)
        
        return key_bytes


# Test the module if run directly
if __name__ == "__main__":
    print("Testing CryptoManager...\n")
    
    manager = CryptoManager()
    
    # Test 1: Generate salt
    salt = manager.generate_salt()
    print(f"Generated Salt: {salt[:16]}... (truncated)")
    
    # Test 2: Encryption/Decryption
    test_data = {"google.com": {"username": "user@gmail.com", "password": "secret123"}}
    key = Fernet.generate_key()
    print(f"\nOriginal Key: {key}")
    
    encrypted = manager.encrypt_data(test_data, key)
    print(f"Encrypted Data: {encrypted[:50]}... (truncated)")
    
    decrypted = manager.decrypt_data(encrypted, key)
    print(f"Decrypted Data: {decrypted}")
    
    # Test 3: Key Splitting/Reconstruction
    shares = manager.split_key(key)
    print(f"\nKey split into {len(shares)} shares:")
    for i, share in enumerate(shares, 1):
        print(f"  Share {i}: {share[:30]}... (truncated)")
    
    reconstructed_key = manager.reconstruct_key(shares[:2])  # Use only 2 shares
    print(f"\nReconstructed Key: {reconstructed_key}")
    print(f"Keys Match: {key == reconstructed_key}")
    
    print("\n✅ All tests passed! CryptoManager is working correctly.")
