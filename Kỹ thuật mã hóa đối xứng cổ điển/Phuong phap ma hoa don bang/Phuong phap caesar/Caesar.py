def encrypt_text(plain_text, key):
    cipher_text = ""
    for character in plain_text:
        if character.isalpha():
            # Xác định chữ cái là in hoa hay in thường
            base = ord('A') if character.isupper() else ord('a')
            cipher_character = chr((ord(character) - base + key) % 26 + base)
            cipher_text += cipher_character
        else:
            cipher_text += character
    return cipher_text

def decrypt_text(cipher_text, key):
    plain_text = ""
    for character in cipher_text:
        if character.isalpha():
            # Xác định chữ cái là in hoa hay in thường
            base = ord('A') if character.isupper() else ord('a')
            plain_character = chr((ord(character) - base - key) % 26 + base)
            plain_text += plain_character
        else:
            plain_text += character
    return plain_text

print("Phương pháp mã hóa caesar")
plain_text = input("Nhập vào plain text: ")
key = int(input("Nhập vào key: "))
cipher_text = encrypt_text(plain_text, key)
decrypted_text = decrypt_text(cipher_text, key)
print(f"Bản mã : {cipher_text}")
print(f"Bản rõ : {decrypted_text}")

