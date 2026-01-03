"""
Decentralized Multi-Cloud Vault - GUI Application
------------------------------------------------
A secure password manager that uses:
- AES encryption for data security
- Shamir's Secret Sharing for key distribution
- Multi-cloud redundancy (AWS + Google + Local)

Zero-Knowledge Architecture:
Your master encryption key never exists in one place. It's split into 3 shares
distributed across multiple locations. Even if one location is compromised,
your vault remains secure.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from vault_handler import VaultController
import threading


class VaultGUI:
    """
    Graphical User Interface for the Multi-Cloud Vault.
    Features a cyberpunk/hacking aesthetic with dark theme.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The Tk root window
        """
        self.root = root
        self.vault_controller = VaultController()
        
        # Configure window
        self.root.title("🔐 Decentralized Multi-Cloud Vault")
        self.root.geometry("700x600")
        self.root.configure(bg='#0a0a0a')
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI elements
        self.create_header()
        self.create_add_password_section()
        self.create_view_passwords_section()
        self.create_status_bar()
        
        print("🚀 GUI Application Started")
    
    def setup_styles(self):
        """
        Configure the dark theme styling.
        """
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure colors for widgets
        style.configure('TLabel', background='#0a0a0a', foreground='#00ff00', font=('Courier', 11))
        style.configure('TButton', background='#1a1a1a', foreground='#00ff00', font=('Courier', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#1a1a1a', foreground='#00ff00')
        style.configure('Header.TLabel', font=('Courier', 18, 'bold'), foreground='#00ff00')
        style.configure('Section.TLabel', font=('Courier', 14, 'bold'), foreground='#00ff00')
    
    def create_header(self):
        """
        Create the application header.
        """
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(pady=20)
        
        title = ttk.Label(
            header_frame,
            text="🔐 DECENTRALIZED MULTI-CLOUD VAULT 🔐",
            style='Header.TLabel'
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Zero-Knowledge • Multi-Cloud • Military-Grade Encryption",
            font=('Courier', 9)
        )
        subtitle.pack()
    
    def create_add_password_section(self):
        """
        Create the section for adding new passwords.
        """
        # Section frame
        section_frame = tk.Frame(self.root, bg='#0a0a0a', highlightbackground='#00ff00', highlightthickness=2)
        section_frame.pack(pady=10, padx=20, fill='x')
        
        # Section title
        section_title = ttk.Label(
            section_frame,
            text="➕ ADD NEW PASSWORD",
            style='Section.TLabel'
        )
        section_title.pack(pady=10)
        
        # Input fields frame
        inputs_frame = tk.Frame(section_frame, bg='#0a0a0a')
        inputs_frame.pack(pady=10)
        
        # Website field
        ttk.Label(inputs_frame, text="Website/Service:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.site_entry = tk.Entry(inputs_frame, bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00', width=40)
        self.site_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Username field
        ttk.Label(inputs_frame, text="Username/Email:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.username_entry = tk.Entry(inputs_frame, bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00', width=40)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Password field
        ttk.Label(inputs_frame, text="Password:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.password_entry = tk.Entry(inputs_frame, bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00', width=40, show='*')
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Add button
        add_button = tk.Button(
            section_frame,
            text="🔒 SECURE & UPLOAD TO CLOUD",
            command=self.add_password_clicked,
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 12, 'bold'),
            activebackground='#00ff00',
            activeforeground='#0a0a0a',
            cursor='hand2'
        )
        add_button.pack(pady=10)
    
    def create_view_passwords_section(self):
        """
        Create the section for viewing stored passwords.
        """
        # Section frame
        section_frame = tk.Frame(self.root, bg='#0a0a0a', highlightbackground='#00ff00', highlightthickness=2)
        section_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Section title
        section_title = ttk.Label(
            section_frame,
            text="🔍 VIEW STORED PASSWORDS",
            style='Section.TLabel'
        )
        section_title.pack(pady=10)
        
        # Fetch button
        fetch_button = tk.Button(
            section_frame,
            text="🔓 FETCH & DECRYPT FROM CLOUD",
            command=self.fetch_passwords_clicked,
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 12, 'bold'),
            activebackground='#00ff00',
            activeforeground='#0a0a0a',
            cursor='hand2'
        )
        fetch_button.pack(pady=10)
        
        # Text area for displaying passwords
        self.password_display = scrolledtext.ScrolledText(
            section_frame,
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='#00ff00',
            font=('Courier', 10),
            height=12
        )
        self.password_display.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Initial message
        self.password_display.insert('1.0', "Click 'FETCH & DECRYPT' to load your passwords...\n\n")
        self.password_display.insert('end', "🔐 Your vault is protected by Shamir's Secret Sharing\n")
        self.password_display.insert('end', "☁️  Shares distributed across AWS, Google, and Local storage\n")
        self.password_display.insert('end', "🛡️  Zero-knowledge architecture - no single point of failure\n")
        self.password_display.config(state='disabled')
    
    def create_status_bar(self):
        """
        Create the status bar at the bottom.
        """
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 9),
            anchor='w',
            relief='sunken'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def update_status(self, message):
        """
        Update the status bar message.
        
        Args:
            message (str): Status message to display
        """
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def add_password_clicked(self):
        """
        Handle the 'Add Password' button click.
        """
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate inputs
        if not site or not username or not password:
            messagebox.showwarning("Input Required", "Please fill in all fields!")
            return
        
        # Run in separate thread to prevent GUI freezing
        def save_task():
            self.update_status("🔒 Encrypting data...")
            success = self.vault_controller.save_password(site, username, password)
            
            if success:
                self.update_status(f"✅ Password for {site} secured in multi-cloud vault!")
                
                # Clear input fields
                self.site_entry.delete(0, 'end')
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                
                messagebox.showinfo("Success", f"Password for {site} has been encrypted and distributed to the cloud!")
            else:
                self.update_status("❌ Failed to save password")
                messagebox.showerror("Error", "Failed to save password. Check console for details.")
        
        # Start background thread
        thread = threading.Thread(target=save_task, daemon=True)
        thread.start()
    
    def fetch_passwords_clicked(self):
        """
        Handle the 'Fetch Passwords' button click.
        """
        # Run in separate thread to prevent GUI freezing
        def fetch_task():
            self.update_status("☁️  Fetching shares from cloud...")
            passwords = self.vault_controller.retrieve_passwords()
            
            if passwords:
                self.update_status(f"✅ Successfully decrypted {len(passwords)} password(s)")
                
                # Display passwords
                self.password_display.config(state='normal')
                self.password_display.delete('1.0', 'end')
                
                self.password_display.insert('1.0', "═" * 70 + "\n")
                self.password_display.insert('end', "               🔓 DECRYPTED VAULT CONTENTS 🔓\n")
                self.password_display.insert('end', "═" * 70 + "\n\n")
                
                for site, creds in passwords.items():
                    self.password_display.insert('end', f"🌐 Website: {site}\n")
                    self.password_display.insert('end', f"   👤 Username: {creds['username']}\n")
                    self.password_display.insert('end', f"   🔑 Password: {creds['password']}\n")
                    self.password_display.insert('end', "─" * 70 + "\n\n")
                
                self.password_display.insert('end', "═" * 70 + "\n")
                self.password_display.insert('end', f"Total Entries: {len(passwords)}\n")
                self.password_display.insert('end', "🛡️  Secured by Zero-Knowledge Architecture\n")
                
                self.password_display.config(state='disabled')
            else:
                self.update_status("⚠️  No passwords found or failed to decrypt")
                
                self.password_display.config(state='normal')
                self.password_display.delete('1.0', 'end')
                self.password_display.insert('1.0', "No passwords found in vault.\n\n")
                self.password_display.insert('end', "Add your first password using the form above!\n")
                self.password_display.config(state='disabled')
        
        # Start background thread
        thread = threading.Thread(target=fetch_task, daemon=True)
        thread.start()


def main():
    """
    Main entry point for the application.
    """
    root = tk.Tk()
    app = VaultGUI(root)
    root.mainloop()


if __name__ == "__main__":
    print("=" * 70)
    print("🔐 DECENTRALIZED MULTI-CLOUD VAULT")
    print("=" * 70)
    print("Starting secure password manager...")
    print("Features:")
    print("  ✓ AES-256 Encryption")
    print("  ✓ Shamir's Secret Sharing (3 shares, 2 required)")
    print("  ✓ Multi-Cloud Distribution (AWS + Google + Local)")
    print("  ✓ Zero-Knowledge Architecture")
    print("=" * 70)
    print()
    
    main()
