# 🔐 Decentralized Multi-Cloud Vault

A secure password manager implementing **Zero-Knowledge Architecture** with military-grade encryption and multi-cloud redundancy.

## 🌟 Key Features

- **AES-256 Encryption**: Military-grade symmetric encryption using Fernet
- **Shamir's Secret Sharing**: Master key split into 3 shares (any 2 required for reconstruction)
- **Multi-Cloud Distribution**: Shares distributed across AWS S3, Google Drive, and Local Storage
- **Zero-Knowledge Architecture**: Master encryption key never stored - only exists temporarily during operations
- **Cyberpunk GUI**: Dark-themed interface with real-time status updates

## 🏗️ Architecture

### Security Model
```
Password → AES Encryption → Split Key (3 shares) → Multi-Cloud Distribution
                                  ↓
                    Share 1 → AWS S3
                    Share 2 → Google Drive (Simulated)
                    Share 3 → Local Disk

Retrieval: Any 2 Shares → Reconstruct Key → Decrypt Vault
```

### Why This is Secure
1. **No Single Point of Failure**: Key is never stored in one place
2. **Redundancy**: Only need 2 of 3 shares to access vault
3. **Zero-Knowledge**: Even the application doesn't know your key
4. **Multi-Cloud**: Distributed across different providers for resilience

## 📁 Project Structure

```
MultiCloudVault/
├── crypto_engine.py       # AES encryption + Shamir's Secret Sharing
├── cloud_manager.py       # Multi-cloud distribution (AWS + Google)
├── vault_handler.py       # Main vault logic and orchestration
├── app.py                 # GUI application (tkinter)
└── README.md             # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.9+ (Note: secretsharing library may have compatibility issues with Python 3.14+)
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd MultiCloudVault
pip install secretsharing cryptography boto3 google-api-python-client
```

**Note**: If you encounter issues with `secretsharing` on Python 3.14+, use Python 3.9-3.13:
```bash
# Install with Python 3.9-3.13
python3.9 -m pip install secretsharing cryptography boto3 google-api-python-client
```

### Step 2: Configure AWS (Optional)

For actual AWS S3 integration:
1. Create an AWS account and S3 bucket
2. Get AWS Access Key ID and Secret Access Key
3. Modify `cloud_manager.py` line 41-42:
```python
self.aws_access_key = 'YOUR_AWS_ACCESS_KEY'
self.aws_secret_key = 'YOUR_AWS_SECRET_KEY'
```

**Demo Mode**: The application works without AWS credentials by simulating cloud storage locally.

## 🎮 Usage

### Run the GUI Application

```bash
python3 app.py
```

or if using specific Python version:

```bash
python3.9 app.py
```

### Using the Application

1. **Add a Password**:
   - Enter Website/Service name
   - Enter Username/Email
   - Enter Password
   - Click "🔒 SECURE & UPLOAD TO CLOUD"

2. **View Passwords**:
   - Click "🔓 FETCH & DECRYPT FROM CLOUD"
   - All passwords will be displayed in the text area

3. **Status Updates**:
   - Watch the status bar at the bottom for real-time feedback
   - Console shows detailed cryptographic operations

## 🧪 Testing Individual Modules

### Test Crypto Engine
```bash
python3 crypto_engine.py
```
Output: Tests encryption, decryption, key splitting, and reconstruction

### Test Cloud Manager
```bash
python3 cloud_manager.py
```
Output: Tests AWS and Google cloud upload/download (simulated)

### Test Vault Handler
```bash
python3 vault_handler.py
```
Output: Tests complete vault workflow with real data

## 📊 Technical Details

### Encryption
- **Algorithm**: AES-256 in CBC mode with HMAC
- **Library**: `cryptography.fernet` (industry standard)
- **Key Size**: 256 bits (32 bytes)

### Secret Sharing
- **Algorithm**: Shamir's Secret Sharing Scheme
- **Configuration**: (2, 3) threshold scheme
- **Shares**: 3 total, 2 required for reconstruction

### Cloud Storage
- **AWS S3**: Production-ready cloud storage
- **Google Drive**: Simulated (can be extended with Google Drive API)
- **Local**: Redundant backup on local filesystem

## 🔒 Security Best Practices

### For Production Use:

1. **Never Hardcode Credentials**:
   ```python
   # Use environment variables
   import os
   aws_key = os.environ.get('AWS_ACCESS_KEY')
   aws_secret = os.environ.get('AWS_SECRET_KEY')
   ```

2. **Use IAM Roles**: Instead of access keys, use AWS IAM roles

3. **Enable MFA**: Multi-factor authentication for cloud accounts

4. **Regular Backups**: Keep encrypted backups of your vault

5. **Secure Local Storage**: Encrypt your local share with OS-level encryption

## 🎯 Demonstration Points

When presenting to your mentor, highlight:

1. **Zero-Knowledge Architecture**:
   - Show how key is generated, used, and immediately deleted
   - Explain why the key never exists in full form

2. **Shamir's Secret Sharing**:
   - Demonstrate threshold cryptography (2 of 3)
   - Show what happens if one share is lost

3. **Multi-Cloud Redundancy**:
   - Show shares distributed across multiple locations
   - Explain disaster recovery scenarios

4. **Cryptographic Operations**:
   - Run individual module tests to show encryption in action
   - Display key splitting in console output

5. **Real-World Application**:
   - This is how enterprise password managers work
   - Similar to 1Password, LastPass architecture

## 🐛 Troubleshooting

### Issue: "NameError: name 'long' is not defined"
**Solution**: Use Python 3.9-3.13 instead of 3.14+
```bash
python3.9 app.py
```

### Issue: "ModuleNotFoundError: No module named 'secretsharing'"
**Solution**: Install with the correct Python version
```bash
python3.9 -m pip install secretsharing
```

### Issue: AWS credentials error
**Solution**: Application works in demo mode without AWS credentials. For production, configure AWS properly.

## 📚 Learning Resources

- [Cryptography Documentation](https://cryptography.io/)
- [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Zero-Knowledge Architecture](https://en.wikipedia.org/wiki/Zero-knowledge_proof)

## 🎓 Educational Value

This project demonstrates:
- Applied Cryptography
- Distributed Systems
- Cloud Computing
- Software Engineering Best Practices
- Security Architecture

## 📝 License

MIT License - Feel free to use this for educational purposes.

## 👨‍💻 Author

Created as an advanced security project demonstrating:
- Modern cryptographic techniques
- Multi-cloud architecture
- Zero-knowledge security principles

---

**Remember**: This is a demonstration project. For production use, consult with security professionals and conduct thorough security audits.

🔐 **Stay Secure!**
