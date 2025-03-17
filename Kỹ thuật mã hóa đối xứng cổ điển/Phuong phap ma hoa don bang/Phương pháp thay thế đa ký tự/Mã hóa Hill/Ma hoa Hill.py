import numpy as np
from sympy import Matrix
import string

def matrix_mod_inverse(matrix, modulus):
    """Tính ma trận nghịch đảo theo modulo"""
    # Sử dụng thư viện sympy để tính ma trận nghịch đảo
    det = int(round(np.linalg.det(matrix))) % modulus
    
    # Kiểm tra xem ma trận có nghịch đảo hay không
    if np.gcd(det, modulus) != 1:
        raise ValueError("Ma trận khóa không khả nghịch. Vui lòng chọn khóa khác.")
    
    # Tính ma trận nghịch đảo
    matrix_sympy = Matrix(matrix)
    matrix_inverse = matrix_sympy.inv_mod(modulus)
    
    # Chuyển đổi về numpy array
    result = np.array(matrix_inverse).astype(int)

    return result

def hill_encrypt(plaintext, key_matrix):
    """Mã hóa văn bản sử dụng mã Hill"""
    n = key_matrix.shape[0]  # Kích thước ma trận khóa
    
    # Chuẩn bị plaintext
    plaintext = ''.join(c for c in plaintext.upper() if c in string.ascii_uppercase)
    
    # Thêm padding nếu cần
    padding = n - (len(plaintext) % n) if len(plaintext) % n != 0 else 0
    plaintext += 'X' * padding
    
    # Chuyển đổi plaintext thành các vector số
    plaintext_nums = [ord(c) - ord('A') for c in plaintext]
    
    # Mã hóa từng khối n ký tự
    ciphertext = ""
    for i in range(0, len(plaintext_nums), n):
        block = plaintext_nums[i:i+n]
        # Nhân vector với ma trận khóa
        encrypted_block = np.dot(key_matrix, block) % 26
        # Chuyển đổi lại thành ký tự
        for num in encrypted_block:
            ciphertext += chr(num + ord('A'))
    
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    """Giải mã văn bản đã mã hóa bằng Hill"""
    n = key_matrix.shape[0]  # Kích thước ma trận khóa
    
    # Tính ma trận nghịch đảo
    try:
        inverse_key = matrix_mod_inverse(key_matrix, 26)
    except ValueError as e:
        return str(e)
    
    # Chuẩn bị ciphertext
    ciphertext = ''.join(c for c in ciphertext.upper() if c in string.ascii_uppercase)
    
    # Đảm bảo độ dài ciphertext là bội số của n
    if len(ciphertext) % n != 0:
        return "Độ dài văn bản mã hóa không hợp lệ."
    
    # Chuyển đổi ciphertext thành các vector số
    ciphertext_nums = [ord(c) - ord('A') for c in ciphertext]
    
    # Giải mã từng khối n ký tự
    plaintext = ""
    for i in range(0, len(ciphertext_nums), n):
        block = ciphertext_nums[i:i+n]
        # Nhân vector với ma trận khóa nghịch đảo
        decrypted_block = np.dot(inverse_key, block) % 26
        # Chuyển đổi lại thành ký tự
        for num in decrypted_block:
            plaintext += chr(int(round(num)) % 26 + ord('A'))
    
    return plaintext

def print_matrix(matrix):
    """In ma trận khóa"""
    print("Ma trận khóa:")
    for row in matrix:
        print(" ".join(str(num) for num in row))
    print()

def input_key_matrix(n):
    """Nhập ma trận khóa từ người dùng"""
    print(f"Nhập ma trận khóa {n}x{n} (các số từ 0-25):")
    matrix = np.zeros((n, n), dtype=int)
    
    for i in range(n):
        row = list(map(int, input().split()))
        matrix[i] = row

    return matrix

def is_invertible(matrix, modulus=26):
    """Kiểm tra ma trận có khả nghịch theo modulo hay không"""
    try:
        matrix_mod_inverse(matrix, modulus)
        return True
    except ValueError:
        return False

def main():
    print("CHƯƠNG TRÌNH MÃ HÓA VÀ GIẢI MÃ HILL")

    # Nhập kích thước ma trận
    n = int(input("Nhập kích thước ma trận khóa (2 hoặc 3): "))

    # Nhập ma trận khóa
    key_matrix = input_key_matrix(n)
    print_matrix(key_matrix)

    # Kiểm tra tính khả nghịch của ma trận khóa
    if not is_invertible(key_matrix):
        print("Ma trận khóa không khả nghịch. Vui lòng chọn ma trận khác.")
        return

    # Nhập văn bản cần mã hóa
    plaintext = input("Nhập văn bản cần mã hóa: ")

    # Mã hóa văn bản
    ciphertext = hill_encrypt(plaintext, key_matrix)
    print("Văn bản sau khi mã hóa:", ciphertext)

    # Giải mã văn bản
    decrypted_text = hill_decrypt(ciphertext, key_matrix)
    print("Văn bản sau khi giải mã:", decrypted_text)

if __name__ == "__main__":
    main()
