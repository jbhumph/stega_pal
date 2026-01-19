from .lsb import LSBEncoder

ENCODERS = {
    ("image", "LSB"): LSBEncoder,
}

def get_encoder(media_type: str, algorithm: str):
    key = (media_type, algorithm)
    encoder_class = ENCODERS.get(key)
    if not encoder_class:
        raise ValueError(f"No encoder for {media_type}/{algorithm}")
    return encoder_class()
