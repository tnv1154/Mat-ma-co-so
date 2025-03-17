import random
import string

def generate_key():
    # Tạo bảng chữ cái gốc
    alphabet = string.ascii_lowercase
    # Tạo bảng chữ cái đã bị xáo trộn
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    shuffled = ''.join(shuffled)
    # Tạo từ điển ánh xạ
    key = {}
    for i in range(len(alphabet)):
        key[alphabet[i]] = shuffled[i]
    return key

def encrypt_text(plain_text, key):
    cipher_text = ""
    for character in plain_text:
        if character.isalpha():
            # Xác định chữ cái là in hoa hay in thường
            if character.isupper():
                cipher_text += key[character.lower()].upper()
            else:
                cipher_text += key[character]
        else:
            cipher_text += character
    return cipher_text

def decrypt_text(cipher_text, key):
    # Tạo bảng ánh xạ ngược
    reverse_key = {v: k for k, v in key.items()}
    plain_text = ""
    for character in cipher_text:
        if character.isalpha():
            # Xác định chữ cái là in hoa hay in thường
            if character.isupper():
                plain_text += reverse_key[character.lower()].upper()
            else:
                plain_text += reverse_key[character]
        else:
            plain_text += character
    return plain_text

def display_key(key):
    alphabet = string.ascii_lowercase
    print("Bảng chữ cái:  ", alphabet)
    cipher_alphabet = ''.join([key[c] for c in alphabet])
    print("Bảng hoán vị:  ", cipher_alphabet)

print("Phương pháp mã hóa thay thế đơn bảng (Monoalphabetic Substitution Cipher)")
plain_text = input("Nhập vào plain text: ")

# Tạo khóa ngẫu nhiên
key = generate_key()
display_key(key)

# Mã hóa và giải mã
cipher_text = encrypt_text(plain_text, key)
decrypted_text = decrypt_text(cipher_text, key)

print(f"Bản mã : {cipher_text}")
print(f"Bản rõ : {decrypted_text}")
