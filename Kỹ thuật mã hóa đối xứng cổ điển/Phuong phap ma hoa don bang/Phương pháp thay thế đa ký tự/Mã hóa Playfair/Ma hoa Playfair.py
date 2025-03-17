def create_playfair_matrix(key):
    # Tạo ma trận Playfair từ khóa
    key = key.upper().replace("J", "I")  # Thay thế J bằng I (quy ước phổ biến)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Bảng chữ cái không có J
    
    # Loại bỏ các ký tự trùng lặp trong khóa
    key_chars = []
    for char in key:
        if char.isalpha() and char not in key_chars:
            key_chars.append(char)
    
    # Thêm các ký tự còn lại của bảng chữ cái
    for char in alphabet:
        if char not in key_chars:
            key_chars.append(char)
    
    # Tạo ma trận 5x5
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(key_chars[i:i+5])
    
    return matrix

def find_position(matrix, char):
    # Tìm vị trí của ký tự trong ma trận
    char = char.upper()
    if char == 'J':
        char = 'I'
    
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return -1, -1

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    plaintext = plaintext.upper().replace("J", "I")
    
    # Chuẩn bị cặp ký tự
    i = 0
    pairs = []
    while i < len(plaintext):
        if i == len(plaintext) - 1:
            # Nếu còn một ký tự cuối cùng, thêm 'X'
            pairs.append(plaintext[i] + 'X')
            i += 1
        elif plaintext[i] == plaintext[i+1]:
            # Nếu hai ký tự giống nhau, thêm 'X' vào giữa
            pairs.append(plaintext[i] + 'X')
            i += 1
        else:
            # Tạo cặp bình thường
            pairs.append(plaintext[i:i+2])
            i += 2
    
    # Mã hóa từng cặp
    ciphertext = ""
    for pair in pairs:
        if len(pair) == 2 and pair[0].isalpha() and pair[1].isalpha():
            row1, col1 = find_position(matrix, pair[0])
            row2, col2 = find_position(matrix, pair[1])
            
            if row1 == row2:  # Cùng hàng
                ciphertext += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Cùng cột
                ciphertext += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Tạo hình chữ nhật
                ciphertext += matrix[row1][col2] + matrix[row2][col1]
        else:
            ciphertext += pair
    
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    ciphertext = ciphertext.upper()
    
    # Tách ciphertext thành các cặp
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    
    # Giải mã từng cặp
    plaintext = ""
    for pair in pairs:
        if len(pair) == 2 and pair[0].isalpha() and pair[1].isalpha():
            row1, col1 = find_position(matrix, pair[0])
            row2, col2 = find_position(matrix, pair[1])
            
            if row1 == row2:  # Cùng hàng
                plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Cùng cột
                plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  # Tạo hình chữ nhật
                plaintext += matrix[row1][col2] + matrix[row2][col1]
        else:
            plaintext += pair
    
    # Xử lý loại bỏ các ký tự 'X' được thêm vào trong quá trình mã hóa
    result = ""
    i = 0
    while i < len(plaintext):
        if i < len(plaintext) - 1 and plaintext[i+1] == 'X' and (i+2 < len(plaintext) and plaintext[i] == plaintext[i+2]):
            # Nếu có mẫu "aXa", loại bỏ 'X'
            result += plaintext[i]
            i += 2  # Bỏ qua 'X'
        elif i == len(plaintext) - 2 and plaintext[i+1] == 'X':
            # Nếu 'X' là ký tự cuối cùng của cặp cuối cùng, loại bỏ nó
            result += plaintext[i]
            i += 2
        else:
            result += plaintext[i]
            i += 1
    
    return result

def print_matrix(matrix):
    # In ma trận Playfair để kiểm tra
    print("Ma trận Playfair:")
    for row in matrix:
        print(" ".join(row))
    print()

def main():
    print("CHƯƠNG TRÌNH MÃ HÓA VÀ GIẢI MÃ PLAYFAIR")
    
    plaintext = input("Nhập văn bản cần mã hóa: ")
    key = input("Nhập khóa: ")
    
    # Loại bỏ khoảng trắng và ký tự đặc biệt
    plaintext = ''.join(c for c in plaintext if c.isalpha())
    
    # Tạo và hiển thị ma trận Playfair
    matrix = create_playfair_matrix(key)
    print_matrix(matrix)
    
    # Mã hóa văn bản
    ciphertext = playfair_encrypt(plaintext, key)
    print("Văn bản sau khi mã hóa:", ciphertext)
    
    # Giải mã văn bản
    decrypted_text = playfair_decrypt(ciphertext, key)
    print("Văn bản sau khi giải mã:", decrypted_text)

if __name__ == "__main__":
    main()
