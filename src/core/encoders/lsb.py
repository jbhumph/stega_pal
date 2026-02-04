from PIL import Image

class LSBEncoder:
    def encode(self, file_path, payload, settings, output_path) -> None:
        # Implementation of LSB encoding
        bit_planes = settings.get_setting("bit_planes", 1)
        print(f"Bit planes: {bit_planes}")

        # Add delimiter and text payload to bits
        delimiter_type = settings.get_setting("delimiter", "NULL")
        print(delimiter_type)
        binary_output = self.text_to_binary(payload + "<END>")

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

        # Load image and get pixel access
        img, pixels = self.load_image(settings, file_path)
        print("Image loaded")

        # Encode message in image
        self.encode_message(img, pixels, binary_output, bit_planes)
        print("Message encoded")

        # Save modified image
        img.save(output_path)
        print(f"Image saved to {output_path}")
        return output_path


    # Embed the binary message into the image pixels
    def encode_message(self, img: Image, pixels, binary_output: str, bit_planes: int) -> None:
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
