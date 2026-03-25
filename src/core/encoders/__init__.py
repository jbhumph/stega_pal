from .lsb import LSBEncoder

ENCODERS = {
    ("image", "LSB"): LSBEncoder,
    ("audio", "LSB"): LSBEncoder,
}

def get_encoder(media_type: str, algorithm: str):
    print(f"Getting encoder for media type: {media_type}, algorithm: {algorithm}")
    key = (media_type, algorithm)
    encoder_class = ENCODERS.get(key)
    if not encoder_class:
        raise ValueError(f"No encoder for {media_type}/{algorithm}")
    return encoder_class()
