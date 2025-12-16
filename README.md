# Python Password Manager
A local python password manager which incorporates encryption.

# How it works
The application makes use of hashlib to store an encrypted version of the main password as a hash value. After inputting the correct password, the length of your password is copied into local memory and used within the ceasur cipher as a key to encrypt and decrypt any password data stored in the application.

# What is secure
The master password.
Values stored in the password manager depending on key and encryption implementation.

# Future steps
To make the local password manager truly secure, a more robust key and encryption method must be implemented. A method which incorporates wait times to slow down a brute force attack would also be a welcome addition.
