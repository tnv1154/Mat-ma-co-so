import numpy as np
from scipy.io import wavfile
import argparse


class A51Cipher:
    def __init__(self, key):
        """Initialize the A5/1 cipher with a 64-bit key."""
        # Register sizes for A5/1
        self.R1_SIZE = 19
        self.R2_SIZE = 22
        self.R3_SIZE = 23

        # Clocking bit positions (zero-indexed)
        self.R1_CLOCK = 8
        self.R2_CLOCK = 10
        self.R3_CLOCK = 10

        # Feedback taps
        self.R1_TAPS = [13, 16, 17, 18]
        self.R2_TAPS = [20, 21]
        self.R3_TAPS = [7, 20, 21, 22]

        # Initialize registers (all zeros)
        self.R1 = [0] * self.R1_SIZE
        self.R2 = [0] * self.R2_SIZE
        self.R3 = [0] * self.R3_SIZE

        # Load the key into the registers
        self._key_setup(key)

    def _key_setup(self, key):
        """Load the key into registers."""
        # Convert key to binary
        key_bits = [int(bit) for bit in bin(key)[2:].zfill(64)]

        # Mix the key into all three registers
        for i in range(64):
            feedback_bit = key_bits[i]

            # XOR the feedback bit with the feedback taps
            r1_fb = feedback_bit ^ self.R1[0]
            r2_fb = feedback_bit ^ self.R2[0]
            r3_fb = feedback_bit ^ self.R3[0]

            # Shift registers
            self.R1 = self.R1[1:] + [r1_fb]
            self.R2 = self.R2[1:] + [r2_fb]
            self.R3 = self.R3[1:] + [r3_fb]

    def _majority(self, a, b, c):
        """Majority function: returns the value that occurs most."""
        return 1 if a + b + c >= 2 else 0

    def _get_feedback(self, register, taps):
        """Calculate feedback bit for a register."""
        fb = register[0]
        for tap in taps:
            fb ^= register[tap]
        return fb

    def _clock_registers(self):
        """Clock the registers according to majority rule."""
        # Get clocking bits
        r1_clock = self.R1[self.R1_CLOCK]
        r2_clock = self.R2[self.R2_CLOCK]
        r3_clock = self.R3[self.R3_CLOCK]

        # Determine majority
        maj = self._majority(r1_clock, r2_clock, r3_clock)

        # Clock registers according to majority rule
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
        """Generate one byte of keystream."""
        keystream_byte = 0

        for i in range(8):
            # Clock the registers
            self._clock_registers()

            # Output bit is XOR of all three register outputs
            output_bit = self.R1[-1] ^ self.R2[-1] ^ self.R3[-1]

            # Add to our keystream byte
            keystream_byte = (keystream_byte << 1) | output_bit

        return keystream_byte

    def encrypt_decrypt(self, data):
        """Encrypt or decrypt the data (XOR with keystream)."""
        result = bytearray(len(data))

        for i in range(len(data)):
            keystream_byte = self.generate_keystream_byte()
            result[i] = data[i] ^ keystream_byte

        return result


def encode_audio(input_file, output_file, key):
    """Encode an audio file using A5/1 cipher."""
    # Read the WAV file
    sample_rate, audio_data = wavfile.read(input_file)

    # Convert to bytes if needed
    if audio_data.dtype != np.uint8:
        # Normalize to 0-255 range if not already 8-bit
        if audio_data.dtype == np.int16:
            # Scale from int16 to uint8
            audio_data = ((audio_data.astype(np.float32) + 32768) / 256).astype(np.uint8)
        elif audio_data.dtype == np.float32 or audio_data.dtype == np.float64:
            # Scale from -1.0...1.0 to 0...255
            audio_data = ((audio_data + 1.0) * 127.5).astype(np.uint8)

    # Initialize A5/1 cipher
    cipher = A51Cipher(key)

    # Convert audio data to bytes
    audio_bytes = audio_data.tobytes()

    # Encrypt the audio data
    encrypted_bytes = cipher.encrypt_decrypt(audio_bytes)

    # Convert back to numpy array
    encrypted_audio = np.frombuffer(encrypted_bytes, dtype=np.uint8)

    # Reshape if original was multi-channel
    if len(audio_data.shape) > 1:
        encrypted_audio = encrypted_audio.reshape(audio_data.shape)

    # Save the encrypted audio
    wavfile.write(output_file, sample_rate, encrypted_audio)

    print(f"Audio file encrypted and saved to {output_file}")


def decode_audio(input_file, output_file, key):
    """Decode an A5/1 encoded audio file."""
    # The encryption and decryption process is symmetric (XOR with keystream)
    # So we can use the same function
    encode_audio(input_file, output_file, key)
    print(f"Audio file decrypted and saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A5/1 Audio Encoder/Decoder")
    parser.add_argument('action', choices=['encode', 'decode'], help='Action to perform')
    parser.add_argument('input_file', help='Input audio file (.wav)')
    parser.add_argument('output_file', help='Output audio file (.wav)')
    parser.add_argument('--key', type=int, default=0x0123456789ABCDEF,
                        help='64-bit key in hexadecimal (default: 0x0123456789ABCDEF)')

    args = parser.parse_args()

    if args.action == 'encode':
        encode_audio(args.input_file, args.output_file, args.key)
    else:  # decode
        decode_audio(args.input_file, args.output_file, args.key)