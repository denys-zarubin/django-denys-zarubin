import base64


def encode_email(email):
    """
    Generate unreadable hash based on email
    """
    return base64.b64encode(email.encode('utf-8'))


def decode_email(email):
    """
    Return email from unreadable hash
    """
    return base64.b64decode(email).decode('utf-8')
