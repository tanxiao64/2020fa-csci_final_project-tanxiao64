import hashlib


def get_salt(file):  # pragma: no cover
    """Created a hash salt based on the content of the file.
    Use buffer to avoid memory overflow
    """
    BUF_SIZE = 65536
    sha = hashlib.sha256()

    with open(file, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()[-8:]
