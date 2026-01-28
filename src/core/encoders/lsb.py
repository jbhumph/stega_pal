from PIL import Image

class LSBEncoder:
    def encode(self, file_path, payload, settings, output_path) -> None:
        # Implementation of LSB encoding
        
        # Add delimiter to payload

        # text payload to bits
        binary_output = self.text_to_binary(payload + "<END>")
        print("Converted to binary")

        # Load image and get pixel access
        img, pixels = self.load_image(settings, file_path)
        print("Image loaded")

        # Encode message in image
        self.encode_message(img, pixels, binary_output)
        print("Message encoded")

        # Save modified image
        img.save(output_path)
        print(f"Image saved to {output_path}")
        return output_path


    # Embed the binary message into the image pixels
    def encode_message(self, img: Image, pixels, binary_output: str) -> None:
        bit_index = 0
        total_bits = len(binary_output)

        for y in range(img.height):
            for x in range(img.width):
                if bit_index >= total_bits:
                    break

                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel_index in range(3):
                    if bit_index >= total_bits:
                        break

                    message_bit = int(binary_output[bit_index])
                    channels[channel_index] = (channels[channel_index] & ~1) | message_bit
                    bit_index += 1

                pixels[x, y] = tuple(channels)


    @staticmethod
    # Load image and get pixel access
    def load_image(config, path: str):
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
        return img, pixels
    
    @staticmethod
    # Convert text to binary string
    def text_to_binary(text: str) -> str:
        binary_string = ''.join(bin(ord(char))[2:].zfill(8) for char in text)
        return binary_string
