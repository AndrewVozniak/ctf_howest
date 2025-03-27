import base64
import random
import string


def generate_password(length=31):

    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return 'admin:' + ''.join(random.choice(chars) for _ in range(length))


passwords = [base64.b64encode(generate_password().encode()).decode() for _ in range(350)]
passwords[56] = base64.b64encode("admin:itsaverystrongandsecretpassword".encode()).decode()  # admin password
print(passwords[56])

with open("../static/credentials.txt", "w") as file:
    file.write("\n".join(passwords))
