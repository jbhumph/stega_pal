from PIL import Image

from core.crypto.encrypt import encrypt_message
import soundfile as sf
import numpy as np

class LSBEncoder:
    def encode(self, file_path, payload, settings, output_path, type) -> None:
        # Implementation of LSB encoding
        bit_planes = settings.get_setting("bit_planes", 1)
        print(f"Bit planes: {bit_planes}")

        # Encrypt payload if encryption is enabled
        if settings.get_setting("encryption") and settings.get_setting("encryption") != "None":
            payload = encrypt_message(payload, settings.get_setting("password", ""))
            print(payload)

        # Add delimiter and text payload to bits
        delimiter_type = settings.get_setting("delimiter", "NULL")
        print(delimiter_type)
        binary_output = self.text_to_binary(payload)

        if delimiter_type == 'NULL Terminator':
            binary_output = self.text_to_binary(payload + '\0')
            print("Using NULL terminator delimiter")
        elif delimiter_type == 'Magic Sequence':
            magic_seq = "1111111100000000"
            binary_output = self.text_to_binary(payload + magic_seq)
            print("Using Magic Sequence delimiter")
        else:
            binary_output = self.text_to_binary(payload)
            print("Using no delimiter")


        print("Converted to binary")

        if type == "image":
            # Load image and get pixel access
            img, pixels = self.load_image(settings, file_path)
            print("Image loaded")
            # Encode message in image
            self.encode_message(img, pixels, binary_output, bit_planes, settings)
            print("Message encoded")
            # Save modified image
            img.save(output_path)
            print(f"Image saved to {output_path}")
            return output_path
        elif type == "audio":
            # Load audio and get bit access
            data, samplerate = self.load_audio(settings, file_path)
            print("Audio loaded")
            # Encode message in audio
            self.encode_message_audio(data, binary_output, bit_planes, settings)
            print("Message encoded")
            # Save modified audio
            sf.write(output_path, data, samplerate)
            print(f"Audio saved to {output_path}")
            return output_path


    # Embed the binary message into the image pixels
    def encode_message(self, img: Image, pixels, binary_output: str, bit_planes: int, settings) -> None:
        bit_index = 0
        total_bits = len(binary_output)
        mask = ~((1 << bit_planes) - 1)

        for y in range(img.height):
            for x in range(img.width):
                if bit_index >= total_bits:
                    break

                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel_index in range(3):
                    if bit_index >= total_bits:
                        break

                    if "R" in settings.get_setting("color_channels", ["R", "G", "B"]) and channel_index == 0:
                        pass
                    elif "G" in settings.get_setting("color_channels", ["R", "G", "B"]) and channel_index == 1:
                        pass
                    elif "B" in settings.get_setting("color_channels", ["R", "G", "B"]) and channel_index == 2:
                        pass
                    else:
                        continue

                    message_bits = 0
                    for plane in range(bit_planes):
                        if bit_index < total_bits:
                            bit = int(binary_output[bit_index])
                            message_bits |= (bit << plane)  # Pack bit into correct position
                            bit_index += 1
                        else:
                            break

                    channels[channel_index] = (channels[channel_index] & mask) | message_bits

                pixels[x, y] = tuple(channels)

    def encode_message_audio(self, data, binary_output: str, bit_planes: int, settings) -> None:
        bit_index = 0
        total_bits = len(binary_output)
        mask = ~np.int16((1 << bit_planes) - 1)

        mono = data.ndim == 1
        if mono:
            data = data.reshape(-1, 1)

        n_samples = data.shape[0]
        audio_channels = settings.get_setting("audio_channels", ["L", "R"])

        for i in range(n_samples):
            if bit_index >= total_bits:
                break
            for ch in range(data.shape[1]):
                if bit_index >= total_bits:
                    break

                if ch == 0 and "L" not in audio_channels:
                    continue
                elif ch == 1 and "R" not in audio_channels:
                    continue

                message_bits = np.int16(0)
                for plane in range(bit_planes):
                    if bit_index < total_bits:
                        bit = int(binary_output[bit_index])
                        message_bits |= (bit << plane)
                        bit_index += 1
                    else:
                        break

                data[i, ch] = (data[i, ch] & mask) | message_bits

        if mono:
            data = data.reshape(-1)

        return data


    @staticmethod
    # Load image and get pixel access
    def load_image(config, path: str):
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
        return img, pixels
    
    @staticmethod
    # Load audio and get pixel access
    def load_audio(config, path: str):
        data, samplerate = sf.read(path, dtype='int16')
        return data, samplerate
    
    @staticmethod
    # Convert text to binary string
    def text_to_binary(text: str) -> str:
        binary_string = ''.join(bin(ord(char))[2:].zfill(8) for char in text)
        return binary_string
