import base64


def file_to_base64(path):
    with open(path, "rb") as file:
        my_string = str(base64.b64encode(file.read()).decode('UTF-8'))
    return str(my_string)


def base64_to_file(b64, filename):
    data = base64.b64decode(b64, validate=True)
    f = open(filename, 'wb')
    f.write(data)
    f.close()
