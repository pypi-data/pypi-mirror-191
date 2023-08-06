import base64

def b64_encryption(filepath):
    filepath = filepath.replace("'", "")
    with open(filepath, 'rb') as f:
        contents = f.read()
        encryption = str(base64.b64encode(contents))
        encryption = encryption[2:(len(encryption)-1)]
        pass
    return encryption
