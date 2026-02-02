from PIL import Image

class LSBDecoder:
    def decode(self, file_path, settings) -> str:
        # Implementation of LSB decoding
        bit_planes = settings.get_setting("Bit Planes", 1)
        print(f"Bit planes: {bit_planes}")
        
        # Load image and get pixel access
        img, pixels = self.load_image(settings, file_path)
        print("Image loaded")

        # Declare delimiter type
        delimiter_type = settings.get_setting('delimiter', 'NULL')
        print(delimiter_type)
        magic_seq = "1111111100000000"
        print(f"Delimiter type: {delimiter_type}")
        print(f"Magic sequence: {magic_seq}")

        # Extract bits from image
        extracted_bits = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel in channels:
                    for plane in range(bit_planes):
                        bit = (channel >> plane) & 1  # Extract bit at position 'plane'
                        extracted_bits.append(str(bit))
        binary_str = ''.join(extracted_bits)

        # Check for length prefix
        message_length = None
        if delimiter_type == "length_prefix":
            length_bits = binary_str[:8*8]  # First 64 bits for length (8 bits per char * 8 chars)
            print(int(length_bits))
            message_length = int(''.join(chr(int(length_bits[i:i+8], 2)) for i in range(0, len(length_bits), 8)))
            print(message_length)

        # Convert bits to characters
        message = ""
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            if len(byte) != 8:
                break
            code = int(byte, 2)
            if magic_seq in message and delimiter_type == "Magic Sequence":
                message = message[:-len(magic_seq)]
                break
            elif code == 0 and delimiter_type == "NULL Terminator":
                break
            elif message_length is not None and len(message) >= message_length + 8 and delimiter_type == "length_prefix":
                message = message[8:]
                break
            message += chr(code)
        binary_output = len(message) * 8


        # Return decoded message
        return message
    

    def load_image(self, settings, file_path):
        img = Image.open(file_path)
        pixels = img.load()
        return img, pixels