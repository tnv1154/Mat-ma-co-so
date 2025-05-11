import string


def vigenere_encrypt(plaintext, key):
    """Mã hóa văn bản sử dụng mã Vigenère"""
    # Chuẩn bị plaintext và key, chỉ giữ lại các chữ cái
    plaintext = ''.join(c for c in plaintext.upper() if c in string.ascii_uppercase)
    key = ''.join(c for c in key.upper() if c in string.ascii_uppercase)

    if not key:
        raise ValueError("Khóa không thể trống")

    ciphertext = ""
    key_length = len(key)

    # Mã hóa từng ký tự
    for i, char in enumerate(plaintext):
        # Lấy ký tự khóa tương ứng
        key_char = key[i % key_length]

        # Chuyển đổi thành số
        plain_num = ord(char) - ord('A')
        key_num = ord(key_char) - ord('A')

        # Mã hóa: (plaintext + key) mod 26
        encrypted_num = (plain_num + key_num) % 26

        # Chuyển đổi lại thành ký tự
        ciphertext += chr(encrypted_num + ord('A'))

    return ciphertext


def vigenere_decrypt(ciphertext, key):
    """Giải mã văn bản đã mã hóa bằng Vigenère"""
    # Chuẩn bị ciphertext và key, chỉ giữ lại các chữ cái
    ciphertext = ''.join(c for c in ciphertext.upper() if c in string.ascii_uppercase)
    key = ''.join(c for c in key.upper() if c in string.ascii_uppercase)

    if not key:
        raise ValueError("Khóa không thể trống")

    plaintext = ""
    key_length = len(key)

    # Giải mã từng ký tự
    for i, char in enumerate(ciphertext):
        # Lấy ký tự khóa tương ứng
        key_char = key[i % key_length]

        # Chuyển đổi thành số
        cipher_num = ord(char) - ord('A')
        key_num = ord(key_char) - ord('A')

        # Giải mã: (ciphertext - key + 26) mod 26
        decrypted_num = (cipher_num - key_num) % 26

        # Chuyển đổi lại thành ký tự
        plaintext += chr(decrypted_num + ord('A'))

    return plaintext


def validate_key(key):
    """Kiểm tra tính hợp lệ của khóa"""
    key = ''.join(c for c in key.upper() if c in string.ascii_uppercase)

    if not key:
        return False, "Khóa không được trống hoặc không chứa ký tự hợp lệ"

    return True, key


def main():
    print("CHƯƠNG TRÌNH MÃ HÓA VÀ GIẢI MÃ VIGENÈRE")
    print("----------------------------------------")

    # Nhập từ khóa
    key = input("Nhập từ khóa (chỉ sử dụng chữ cái): ")

    # Kiểm tra tính hợp lệ của khóa
    valid, processed_key = validate_key(key)
    if not valid:
        print(processed_key)  # Hiển thị thông báo lỗi
        return

    print(f"Từ khóa đã xử lý: {processed_key}\n")

    # Nhập văn bản cần mã hóa
    plaintext = input("Nhập văn bản cần mã hóa: ")

    # Loại bỏ các ký tự không phải chữ cái
    processed_plaintext = ''.join(c for c in plaintext.upper() if c in string.ascii_uppercase)
    print(f"Văn bản đã xử lý: {processed_plaintext}\n")

    # Mã hóa văn bản
    try:
        ciphertext = vigenere_encrypt(plaintext, processed_key)
        print("Văn bản sau khi mã hóa:", ciphertext)

        # Giải mã văn bản
        decrypted_text = vigenere_decrypt(ciphertext, processed_key)
        print("Văn bản sau khi giải mã:", decrypted_text)

        # Kiểm tra xem giải mã có khớp với văn bản gốc không
        if processed_plaintext == decrypted_text:
            print("\nKiểm tra: Giải mã thành công - kết quả khớp với văn bản gốc")
        else:
            print("\nKiểm tra: Giải mã không khớp với văn bản gốc")

    except ValueError as e:
        print(f"Lỗi: {e}")


if __name__ == "__main__":
    main()