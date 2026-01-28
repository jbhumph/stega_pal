from .lsb import LSBDecoder

DECODERS = {
    ("image", "LSB"): LSBDecoder,
}   

def get_decoder(media_type: str, algorithm: str):
    key = (media_type, algorithm)
    decoder_class = DECODERS.get(key)
    if not decoder_class:
        raise ValueError(f"No decoder for {media_type}/{algorithm}")
    return decoder_class()