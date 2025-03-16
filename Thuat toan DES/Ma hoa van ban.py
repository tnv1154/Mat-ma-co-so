import base64

# Các bảng hoán vị và thay thế cho thuật toán DES
# Bảng hoán vị ban đầu (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Bảng hoán vị cuối (IP^-1)
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Bảng mở rộng E
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Bảng hoán vị P
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S-boxes
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Bảng hoán vị PC-1 (Permuted Choice 1)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Bảng hoán vị PC-2 (Permuted Choice 2)
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Số lần dịch bit cho mỗi vòng
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def string_to_bit_array(text):
    """Chuyển đổi chuỗi thành mảng bit"""
    array = []
    for char in text:
        #Hàm bin() trả về dãy bit có dạng 0b***, zfill điền thêm số 0 vào trước cho đủ 8 ký tự
        binVal = bin(ord(char))[2:].zfill(8)
        for bit in binVal:
            array.append(int(bit))
    return array

def bit_array_to_string(array):
    """Chyển mảng bit thành chuỗi ký tự"""
    result = ""
    for i in range(0, len(array), 8):
        byte = array[i:i + 8]
        #Kết hợp các bit trong danh sách byte thành một chuỗi nhị phân
        binary_string = "".join([str(bit) for bit in byte])
        #chuyển chuỗi nhị phân thành mã assii
        decimal_val = int(binary_string, 2)
        #chuyển số thành ký tự
        result += chr(decimal_val)
    return result

def permute(block, table):
    """Hoán vị block theo table"""
    permutated_block = []
    for i in range(len(table)):
       permutated_block.append(block[table[i] - 1])
    return permutated_block

def rotate_left_shift(block, n):
    """Dịch trái block n lần"""
    return block[n:] + block[:n]

def xor(a, b):
    """Thực hiện phép XOR từng bit"""
    ans = []
    for i in range(len(a)):
        ans.append(a[i] ^ b[i])
    return ans

def generate_subkey(key):
    """Sinh 16 khóa con"""
    #Chuyển key thành mảng bit
    key_bit = string_to_bit_array(key)
    #Đảm bảo key có 64 bit
    if len(key_bit) < 64:
        key_bit = key_bit + [0] * (64 - len(key_bit))
    elif len(key_bit) > 64:
        key_bit = key_bit[:64]

    #Tính hoán vị key theo PC1 : 64bit -> 56bit
    key_pc1 = permute(key_bit, PC1)
    #Chia thành 2 nửa 28bit
    left = key_pc1[:28]
    right = key_pc1[28:]

    #Tạo 16 khóa con
    subkey = []
    for i in range(16):
        #Xoay trái 2 nửa n lần theo SHIFT_SCHEDULE
        left_shift = rotate_left_shift(left, SHIFT_SCHEDULE[i])
        right_shift = rotate_left_shift(right, SHIFT_SCHEDULE[i])
        #Hợp nhất 2 nửa
        shift_subkey = left_shift + right_shift
        #Tính hoán vị theo pc2
        subkey_pc2 = permute(shift_subkey, PC2)
        subkey.append(subkey_pc2)
    return subkey

def s_box_substitution(block):
    """Thay thế s_box cho block 48bit -> 32 bit"""
    ans = []
    for i in range(8):
        #Lần lượt lấy ra 6 bit trong block
        small_block = block[i * 6:(i + 1) * 6]
        #Lấy vị trí hàng, cột trong s_box
        row = int(str(small_block[0]) + str(small_block[5]), 2)
        column = int(''.join([str(bit) for bit in small_block[1:5]]), 2)
        #Lấy giá trị từ s_box thứ i
        val = S_BOXES[i][row][column]
        #Đổi giá trị thành 4 bit nhị phân
        bin_val = bin(val)[2:].zfill(4)
        for bit in bin_val:
            ans.append(int(bit))
    return ans


def f_function(block, subkey):
    """Hàm F trong DES"""
    #block 32bit
    #Bước 1: mở rộng 32bit -> 48bit (hoán vị theo bảng E)
    expanded_block = permute(block, E)
    #Bước 2: block XOR subkey
    xored_block = xor(expanded_block, subkey)
    #Bước 3: S_box
    substituted_block = s_box_substitution(xored_block)
    #Bước 4: hoán vị P
    permuted_block = permute(substituted_block, P)
    return permuted_block


def des_encrypt_block(block, subkey):
    """Mã hóa từng khối 64bit"""
    #Hoán vị khởi tạo
    block_ip = permute(block, IP) #64bit
    left = block_ip[:32]
    right = block_ip[32:]

    #16 vòng lặp của des
    for i in range(16):
        #Thực hiện hàm f với nửa phải
        f_result = f_function(right, subkey[i])
        old_right = right
        #XOR với nửa trái
        right = xor(f_result, left)
        left = old_right
    #Kết hợp
    combined = right + left
    #hoán vị kết thúc
    permuted_combine = permute(combined, IP_INV)
    return permuted_combine

def des_decrypt_block(block, subkey):
    """Giải mã từng khối 64bit"""
    #Hoán vị khởi tạo
    block_ip = permute(block, IP) #64bit
    left = block_ip[:32]
    right = block_ip[32:]

    #16 vòng lặp của des
    for i in range(15, -1, -1):
        #Thực hiện hàm f với nửa phải
        f_result = f_function(right, subkey[i])
        old_right = right
        #XOR với nửa trái
        right = xor(f_result, left)
        left = old_right
    #Kết hợp
    combined = right + left
    #hoán vị kết thúc
    permuted_combine = permute(combined, IP_INV)
    return permuted_combine

def pad(text):
    """Thêm padding"""
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding

def unpad(text):
    """Bỏ padding"""
    padding_length = ord(text[-1])
    return text[:-padding_length]

def encrypt_des(text, key):
    """Mã hóa văn bản"""
    #Thêm ký tự đảm bảo văn bản là bội số của 8byte
    padded_text = pad(text)
    #Tạo khóa con
    subkey = generate_subkey(key)
    #Mã hóa từng khối 64 bit
    result = ""
    for i in range(0, len(padded_text), 8):
        block = padded_text[i:i + 8]
        bit_block = string_to_bit_array(block)
        #mã hóa khối
        encrypted_bit_block = des_encrypt_block(bit_block, subkey)
        #chuyển dãy bit được mã hóa thành ký tự
        encrypted_block = bit_array_to_string(encrypted_bit_block)
        result += encrypted_block
    #mã hóa base 64 để dễ hiển thị
    return base64.b64encode(result.encode('latin-1')).decode('ascii')

def decrypt_des(encrypted_text, key):
    """Giải văn bản"""
    # Giải mã base64
    encrypted_bytes = base64.b64decode(encrypted_text)
    encrypted_text = encrypted_bytes.decode('latin-1')
    #Tạo khóa con
    subkey = generate_subkey(key)
    #Giải mã từng khối 64 bit
    plain_text = ""
    for i in range(0, len(encrypted_text), 8):
        block = encrypted_text[i:i + 8]
        bit_block = string_to_bit_array(block)
        #mã hóa khối
        decrypted_bit_block = des_decrypt_block(bit_block, subkey)
        #chuyển dãy bit được mã hóa thành ký tự
        decrypted_block = bit_array_to_string(decrypted_bit_block)
        plain_text += decrypted_block
    result = unpad(plain_text)
    return result

def main():
    print("CHƯƠNG TRÌNH MÃ HÓA VÀ GIẢI MÃ VĂN BẢN BẰNG DES")
    # Nhập văn bản từ bàn phím
    plaintext = input("Nhập văn bản cần mã hóa: ")

    # Nhập khóa
    key = input("Nhập khóa (8 ký tự): ")

    # Đảm bảo khóa có đủ 8 ký tự nếu thiếu thêm 0 vào cuối
    if len(key) < 8:
        key = key + "0" * (8 - len(key))
    elif len(key) > 8:
        key = key[:8]

    # Mã hóa văn bản
    encrypted_text = encrypt_des(plaintext, key)
    print("\nVăn bản sau khi mã hóa:")
    print(encrypted_text)

    # Giải mã văn bản
    decrypted_text = decrypt_des(encrypted_text, key)
    print("\nVăn bản sau khi giải mã:")
    print(decrypted_text)

if __name__ == "__main__":
    main()
