import numpy as np
import wave
import struct


class A51:
    def __init__(self, key):
        """
        Khởi tạo A5/1 cipher với khóa cho trước

        :param key: Khóa bí mật (64 bit)
        """
        if len(key) != 8:  # 8 bytes = 64 bits
            raise ValueError("Khóa phải có độ dài 8 bytes (64 bits)")

        self.R1 = [0] * 19
        self.R2 = [0] * 22
        self.R3 = [0] * 23

        # Điểm tap (vị trí lấy bit để tính toán)
        self.R1_taps = [13, 16, 17, 18]
        self.R2_taps = [20, 21]
        self.R3_taps = [7, 20, 21, 22]

        # Điểm kiểm soát (lấy bit để quyết định việc shift)
        self.R1_clock = 8
        self.R2_clock = 10
        self.R3_clock = 10

        # Khởi tạo các thanh ghi với khóa bí mật
        self._initialize(key)

    def _initialize(self, key):
        """
        Khởi tạo các thanh ghi với khóa bí mật

        :param key: Khóa bí mật (64 bit)
        """
        # Chuyển khóa thành bit
        key_bits = []
        for byte in key:
            if isinstance(byte, str):
                byte = ord(byte)
            for i in range(8):
                key_bits.append((byte >> i) & 1)

        # Nạp bit vào các thanh ghi
        for i in range(64):
            self._clock_all()  # Shift tất cả các thanh ghi

            self.R1[0] ^= key_bits[i]
            self.R2[0] ^= key_bits[i]
            self.R3[0] ^= key_bits[i]

    def _clock_R1(self):
        """Shift thanh ghi R1 và tính toán bit mới"""
        out = self.R1[-1]
        feedback = self.R1[self.R1_taps[0]] ^ self.R1[self.R1_taps[1]] ^ self.R1[self.R1_taps[2]] ^ self.R1[
            self.R1_taps[3]]
        self.R1 = [feedback] + self.R1[:-1]
        return out

    def _clock_R2(self):
        """Shift thanh ghi R2 và tính toán bit mới"""
        out = self.R2[-1]
        feedback = self.R2[self.R2_taps[0]] ^ self.R2[self.R2_taps[1]]
        self.R2 = [feedback] + self.R2[:-1]
        return out

    def _clock_R3(self):
        """Shift thanh ghi R3 và tính toán bit mới"""
        out = self.R3[-1]
        feedback = self.R3[self.R3_taps[0]] ^ self.R3[self.R3_taps[1]] ^ self.R3[self.R3_taps[2]] ^ self.R3[
            self.R3_taps[3]]
        self.R3 = [feedback] + self.R3[:-1]
        return out

    def _clock_all(self):

        majority = (self.R1[self.R1_clock] + self.R2[self.R2_clock] + self.R3[self.R3_clock]) // 2

        # Shift các thanh ghi phù hợp
        if self.R1[self.R1_clock] == majority:
            self._clock_R1()
        if self.R2[self.R2_clock] == majority:
            self._clock_R2()
        if self.R3[self.R3_clock] == majority:
            self._clock_R3()

    def get_keystream_byte(self):
        """
        Tạo 8 bit của keystream

        :return: Một byte của keystream
        """
        ks = 0
        for i in range(8):
            self._clock_all()
            bit = self._clock_R1() ^ self._clock_R2() ^ self._clock_R3()
            ks |= (bit << i)
        return ks

    def encrypt_byte(self, byte):
        """
        Mã hóa một byte bằng XOR với keystream

        :param byte: Byte cần mã hóa
        :return: Byte đã mã hóa
        """
        if isinstance(byte, str):
            byte = ord(byte)
        return byte ^ self.get_keystream_byte()


def encrypt_audio(input_file, output_file, key):
    """
    Mã hóa file âm thanh sử dụng thuật toán A5/1

    :param input_file: Đường dẫn đến file âm thanh gốc (.wav)
    :param output_file: Đường dẫn đến file âm thanh đã mã hóa (.wav)
    :param key: Khóa bí mật (8 bytes)
    """
    # Đọc file âm thanh gốc
    with wave.open(input_file, 'rb') as wav_in:
        # Lấy thông tin của file âm thanh
        params = wav_in.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]

        # Đọc tất cả dữ liệu âm thanh
        frames = wav_in.readframes(nframes)

        # Khởi tạo A5/1 cipher
        cipher = A51(key)

        # Mã hóa dữ liệu âm thanh
        encrypted_frames = bytearray()
        for i in range(0, len(frames), sampwidth):
            # Xử lý theo sampwidth (thường là 2 bytes cho mỗi mẫu)
            for j in range(sampwidth):
                if i + j < len(frames):
                    encrypted_byte = cipher.encrypt_byte(frames[i + j])
                    encrypted_frames.append(encrypted_byte)

        # Ghi dữ liệu đã mã hóa vào file đầu ra
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(encrypted_frames)


def decrypt_audio(input_file, output_file, key):
    """
    Giải mã file âm thanh đã mã hóa bằng A5/1

    :param input_file: Đường dẫn đến file âm thanh đã mã hóa (.wav)
    :param output_file: Đường dẫn đến file âm thanh giải mã (.wav)
    :param key: Khóa bí mật (8 bytes, phải giống với khóa mã hóa)
    """
    # Vì A5/1 là cipher dòng sử dụng XOR, nên quá trình giải mã
    # giống hệt với quá trình mã hóa
    encrypt_audio(input_file, output_file, key)


# Hàm demo
def demo():
    """
    Hàm demo mã hóa và giải mã file âm thanh
    """
    import os

    input_file = "Ma hoa am thanh su dung a5-1/input.wav"  # File âm thanh gốc
    encrypted_file = "encrypted.wav"  # File âm thanh đã mã hóa
    decrypted_file = "decrypted.wav"  # File âm thanh giải mã

    # Tạo khóa 64-bit (8 bytes)
    key = b"SecretK1"

    # Mã hóa
    print(f"Đang mã hóa file {input_file}...")
    encrypt_audio(input_file, encrypted_file, key)
    print(f"Đã mã hóa xong! File kết quả: {encrypted_file}")

    # Giải mã
    print(f"Đang giải mã file {encrypted_file}...")
    decrypt_audio(encrypted_file, decrypted_file, key)
    print(f"Đã giải mã xong! File kết quả: {decrypted_file}")

    # Kiểm tra kích thước file
    original_size = os.path.getsize(input_file)
    encrypted_size = os.path.getsize(encrypted_file)
    decrypted_size = os.path.getsize(decrypted_file)

    print(f"\nKích thước file gốc: {original_size} bytes")
    print(f"Kích thước file mã hóa: {encrypted_size} bytes")
    print(f"Kích thước file giải mã: {decrypted_size} bytes")


if __name__ == "__main__":
    demo()