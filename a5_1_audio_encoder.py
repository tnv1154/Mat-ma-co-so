import numpy as np
from scipy.io import wavfile


class A51Cipher:
    def __init__(self, key):
        """Initialize the A5/1 cipher with a 23-bit key."""
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
        """Load the 23-bit key into registers."""
        # Convert key to binary and ensure it's 23 bits
        key_bits = [int(bit) for bit in bin(key)[2:].zfill(23)]

        # Mix the key into all three registers
        for i in range(23):
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


def process_audio(input_file, output_file, key):
    """Process an audio file using A5/1 cipher."""
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

    # Process the audio data
    processed_bytes = cipher.encrypt_decrypt(audio_bytes)

    # Convert back to numpy array
    processed_audio = np.frombuffer(processed_bytes, dtype=np.uint8)

    # Reshape if original was multi-channel
    if len(audio_data.shape) > 1:
        processed_audio = processed_audio.reshape(audio_data.shape)

    # Save the processed audio
    wavfile.write(output_file, sample_rate, processed_audio)

    print(f"Audio file processed and saved to {output_file}")


def main():
    # Fixed input and output file names
    input_file = "input.wav"
    ciphertext_file = "ciphertext.wav"
    plaintext_file = "plaintext.wav"

    # Default key (23-bit)
    default_key = 0b10101010101010101010101

    # Ask user for a key
    try:
        key_input = input("Enter a 23-bit key (decimal number) or press Enter for default key: ")

        if key_input.strip():
            key = int(key_input)
            # Ensure key is 23 bits by masking
            key = key & 0x7FFFFF  # 23 bits mask (2^23 - 1)
        else:
            key = default_key
            print(f"Using default key: {bin(default_key)[2:].zfill(23)}")
    except ValueError:
        key = default_key
        print(f"Invalid input. Using default key: {bin(default_key)[2:].zfill(23)}")

    # Display the actual key being used in binary
    print(f"Using key (binary): {bin(key)[2:].zfill(23)}")

    try:
        # Step 1: Encrypt input.wav to ciphertext.wav
        print("\nStep 1: Encrypting input.wav to ciphertext.wav")
        process_audio(input_file, ciphertext_file, key)

        # Step 2: Decrypt ciphertext.wav to plaintext.wav
        print("\nStep 2: Decrypting ciphertext.wav to plaintext.wav")
        process_audio(ciphertext_file, plaintext_file, key)

        print("\nProcess completed successfully!")
        print(f"Original file: {input_file}")
        print(f"Encrypted file: {ciphertext_file}")
        print(f"Decrypted file: {plaintext_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure input.wav exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()