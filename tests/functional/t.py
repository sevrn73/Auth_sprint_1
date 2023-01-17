import base64
login = "not_user"
password = "not_password"
my_str = ":".join((login, password)).encode("utf-8")
credentials = base64.b64encode(my_str).decode("utf-8")
print(credentials)