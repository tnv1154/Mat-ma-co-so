import numpy as np
from scipy.io import wavfile
import hashlib


class A51Cipher:
    def __init__(self, key):
        # Khởi tạo mã hóa A5/1 bằng khóa 23 bit
        # khởi tạo các thanh ghi có kích thước 19, 22, 23
        self.R1_SIZE = 19
        self.R2_SIZE = 22
        self.R3_SIZE = 23

        # Vị trí bit xung nhịp (tính từ 0)
        self.R1_CLOCK = 8
        self.R2_CLOCK = 10
        self.R3_CLOCK = 10

        # Feedback taps Các vị trí bit xor tạo thành t
        self.R1_TAPS = [13, 16, 17, 18]
        self.R2_TAPS = [20, 21]
        self.R3_TAPS = [7, 20, 21, 22]

        # gán giá trị 0 cho các thanh ghi
        self.R1 = [0] * self.R1_SIZE
        self.R2 = [0] * self.R2_SIZE
        self.R3 = [0] * self.R3_SIZE

        # Đưa key vào thanh ghi bằng hàm key_setup
        self._key_setup(key)

    def _key_setup(self, key):
        """Đưa key 23 bit vào thanh ghi"""
        # Chuyển key về dạng nhị phân 23 bit
        key_bits = [int(bit) for bit in bin(key)[2:].zfill(23)]

        # Trộn khóa vào 3 thanh ghi
        for i in range(23):
            feedback_bit = key_bits[i]

            # XOR the feedback bit with the feedback taps
            r1_fb = feedback_bit ^ self.R1[0]
            r2_fb = feedback_bit ^ self.R2[0]
            r3_fb = feedback_bit ^ self.R3[0]

            # Dịch thanh ghi
            self.R1 = self.R1[1:] + [r1_fb]
            self.R2 = self.R2[1:] + [r2_fb]
            self.R3 = self.R3[1:] + [r3_fb]

    def _majority(self, a, b, c):
        """Hàm đa số: trả về giá trị xuất hiện nhiều nhất.."""
        return 1 if a + b + c >= 2 else 0

    def _get_feedback(self, register, taps):
        """Tính feedback bit cho thanh ghi"""
        fb = register[0]
        for tap in taps:
            fb ^= register[tap]
        return fb

    def _clock_registers(self):
        """Đánh dấu thanh ghi theo hàm _majority nguyên tắc đa số"""
        # Get clocking bits
        r1_clock = self.R1[self.R1_CLOCK]
        r2_clock = self.R2[self.R2_CLOCK]
        r3_clock = self.R3[self.R3_CLOCK]

        # Xác định đa số
        maj = self._majority(r1_clock, r2_clock, r3_clock)

        # Xung thanh ghi theo quy tắc đa số
        if r1_clock == maj:
            fb = self._get_feedback(self.R1, self.R1_TAPS)
            self.R1 = self.R1[1:] + [fb]

        if r2_clock == maj:
            fb = self._get_feedback(self.R2, self.R2_TAPS)
            self.R2 = self.R2[1:] + [fb]

        if r3_clock == maj:
            fb = self._get_feedback(self.R3, self.R3_TAPS)
            self.R3 = self.R3[1:] + [fb]

    def generate_keystream_byte(self):
        """Tạo ra 1 byte của khóa từ 3 thanh ghi"""
        keystream_byte = 0

        for i in range(8):
            # Clock the registers
            self._clock_registers()

            # Bit đầu ra là XOR của cả ba đầu ra thanh ghi
            output_bit = self.R1[-1] ^ self.R2[-1] ^ self.R3[-1]

            # dịch trái keystream_byte một bit và sau đó gán giá trị output_bit vào bit thấp nhất của keystream_byte
            keystream_byte = (keystream_byte << 1) | output_bit

        return keystream_byte

    def encrypt_decrypt(self, data):
        """Mã hóa hoặc giải mã dữ liệu (XOR với keystream)."""
        # tạo ra một mảng byte có độ dài bằng với độ dài của data
        result = bytearray(len(data))

        for i in range(len(data)):
            keystream_byte = self.generate_keystream_byte()
            result[i] = data[i] ^ keystream_byte

        return result


def string_to_23bit_key(key_string):
    """Chuyển đổi bất kỳ chuỗi nào thành khóa số nguyên 23 bit"""
    # Sử dụng SHA-256 để băm chuỗi
    # Tạo đối tượng băm SHA-256 từ chuỗi key_string sau khi mã hóa nó thành bytes.
    hash_obj = hashlib.sha256(key_string.encode())
    # Lấy giá trị băm (hash) dưới dạng chuỗi hexa (hexadecimal string). Giá trị băm này sẽ dài 64 ký tự hexa (256 bits).
    hash_hex = hash_obj.hexdigest()

    # Lấy 6 ký tự hexa đầu tiên (24 bits) và chuyển đổi thành số nguyên
    key_int = int(hash_hex[:6], 16)

    # Áp dụng mặt nạ để lấy khóa 23 bit
    key_23bit = key_int & 0x7FFFFF # Áp dụng phép AND bitwise để giữ lại 23 bit thấp nhất của key_int. Nếu key_int có hơn 23 bit, các bit cao hơn sẽ bị loại bỏ.
    #0x7FFFFF là mặt nạ 23 bit (2^23 - 1), dưới dạng hexa.
    return key_23bit


def process_audio(input_file, output_file, key):
    """Xử lý tệp âm thanh bằng mã hóa A5/1 trong khi vẫn giữ nguyên định dạng gốc."""
    # Đọc file wav
    sample_rate, audio_data = wavfile.read(input_file)

    # Lưu trữ kiểu dữ liệu gốc để phục hồi sau
    original_dtype = audio_data.dtype

    # Chuyển đổi dữ liệu âm thanh thành byte trực tiếp mà không cần thay đổi định dạng
    audio_bytes = audio_data.tobytes()

    # Khởi tạo mã hóa
    cipher = A51Cipher(key)

    # Xử lý dữ liệu âm thanh
    processed_bytes = cipher.encrypt_decrypt(audio_bytes)

    # Chuyển đổi trở lại mảng numpy với kiểu dữ liệu ban đầuv
    processed_audio = np.frombuffer(processed_bytes, dtype=original_dtype)

    # Định hình lại nếu bản gốc là đa kênh
    if len(audio_data.shape) > 1:
        channels = audio_data.shape[1]
        processed_audio = processed_audio.reshape(-1, channels)

    # lưu âm thanh đã xử lý với kiểu dữ liệu gốc
    wavfile.write(output_file, sample_rate, processed_audio)

    print(f"Tệp âm thanh được xử lý và lưu vào {output_file}")


def main():
    # Khởi tạo file
    input_file = "input.wav"
    ciphertext_file = "ciphertext.wav"
    plaintext_file = "plaintext.wav"

    # Key mặc định
    default_key_string = "default_key"
    default_key = string_to_23bit_key(default_key_string)

    # Nhập key tùy chọn
    key_input = input("Nhập key (xâu bất kỳ) hoặc enter để dùng key mặc định: ")

    if key_input.strip():
        # Chuyển đổi chuỗi thành số nguyên 23 bit
        key = string_to_23bit_key(key_input)
        print(f"Key string: \"{key_input}\"")
    else:
        key = default_key
        print(f"Key mặc định: \"{default_key_string}\"")

    # Hiển thị key ở định dạng nhị phân
    key_binary = bin(key)[2:].zfill(23)
    print(f"Key dạng nhị phân 23 bit: {key_binary}")

    try:
        # Bước 1: Mã hóa input.wav thành ciphertext.wav
        print("\nBước 1: Mã hóa input.wav thành ciphertext.wav")
        process_audio(input_file, ciphertext_file, key)

        # Bước 2: Giải mã ciphertext.wav thành plaintext.wav
        print("\nBước 2: Giải mã ciphertext.wav thành plaintext.wav")
        process_audio(ciphertext_file, plaintext_file, key)

        print("\nProcess completed successfully!")
        print(f"File gốc: {input_file}")
        print(f"File mã hóa: {ciphertext_file}")
        print(f"File giải mã: {plaintext_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Đảm bảo input.wav tồn tại trong thư mục hiện tại.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()