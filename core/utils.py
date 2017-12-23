def generate_hash(email):
    """
    Generate unreadable hash based on email
    """
    # TODO: Can be used some crypt
    
    return email.replace("@", "-").replace('.', '=')


def get_encrypted_email(email):
    """
    Return email from unreadable hash
    """
    return email.replace("-", "@").replace('=', '.')
