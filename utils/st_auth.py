import streamlit as st
import streamlit_authenticator as stauth
import re

ADMINS = [st.secrets["ADMIN"],]
USERNAMES = ["admin", "user", st.secrets["ADMIN"]]
PASSWORDS = ["admin", "user", st.secrets["PASSWORD"]]


class SysColors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def get_users_and_passwords():
    return USERNAMES, PASSWORDS


def get_config(usernames, passwords, expiration=30):
    hashes = stauth.Hasher(passwords).generate()
    users = {u[0]: {'email': f'{u[0].lower()}@verified-ai.com',
                    'name': u[0].title(),
                    'password': u[1]} for u in zip(usernames, hashes)}
    creds = {'usernames': users}
    cookie = {'expiry_days': expiration,
              'key': 'verified-ai',
              'name': 'verified-ai'}
    preauth = {'emails': ['maria@verified-ai.com', ]}
    config = {'credentials': creds,
              'cookie': cookie,
              'preauthorized': preauth}
    return config


def check_valid(user, password):
    if user in USERNAMES and password in PASSWORDS:
        return True
    else:
        return False


def auth_basic(func):
    def wrapper():
        # # authentication
        auth_config = get_config(usernames=USERNAMES, passwords=PASSWORDS)
        authenticator = stauth.Authenticate(auth_config['credentials'],
                                            auth_config['cookie']['name'],
                                            auth_config['cookie']['key'],
                                            auth_config['cookie']['expiry_days'],
                                            auth_config['preauthorized']['emails'])

        name, authentication_status, username = authenticator.login('Login', location='main')
        print(SysColors.YELLOW, name, authentication_status, SysColors.RESET)
        if authentication_status:
            st.write(f'Welcome *{name.title()}*')
            authenticator.logout('Logout', location='sidebar')
            st.session_state.update({"username": name.lower()})
            func()
        elif not authentication_status:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')

    return wrapper


def reset_login():
    for key in st.session_state.keys():
        if key == "username":
            del st.session_state[key]


def login():
    placeholder = st.empty()
    with placeholder:
        with st.form("login"):
            user = st.text_input("Name", max_chars=100)
            password = st.text_input("Password", type="password", label_visibility="collapsed")
            submit = st.form_submit_button("Log in")
    if submit:
        valid = check_valid(user, password)
        if valid:
            st.session_state["username"] = user
            with placeholder:
                st.success(f"Welcome {_get_user()}!")
        else:
            st.warning("Your email should be valid")


def _get_user():
    if 'username' in st.session_state.keys():
        user = st.session_state["username"].split("@")[0]
        return user


def auth_simple(func):
    OK = '\033[92m'  # GREEN
    INFO = '\033[90m'  # GRAY
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET

    def wrapper(*args, **kwargs):
        admin = kwargs.get("admin", False)
        print(INFO, f"Authenticating {'ADMIN' if admin else 'USER'}...", end=" ")
        auth_user = _get_user()
        if auth_user in ADMINS:
            func()
            print(OK, "OK", RESET)
        elif auth_user in USERNAMES and not admin:
            func()
            print(OK, "OK", RESET)
        elif auth_user is None:
            st.warning("You should log in first. Please go to the main page.")
        else:
            st.warning(f"Access denied for user {auth_user}")
            print(FAIL, "FAILED", RESET)

    return wrapper
