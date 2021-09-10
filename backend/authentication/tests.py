from django.test import TestCase

# Create your tests here.
import firebase_admin
from firebase_admin import credentials, auth
from getpass import getpass
import requests

action_code_settings = auth.ActionCodeSettings(
    url='https://www.example.com/checkout?cartId=1234',
    handle_code_in_app=True,
    ios_bundle_id='com.example.ios',
    android_package_name='com.example.android',
    android_install_app=True,
    android_minimum_version='12',
    dynamic_link_domain='coolapp.page.link',
)

cred = credentials.Certificate("hello-world-e9c1c-firebase-adminsdk-ifpd6-3c008d733a.json")
firebase_admin.initialize_app(cred)

# login
def sign_in(e, p, u):
    print("Wait a moment\n")

    try:
        u[0] = auth.sign_in_with_email_and_password(e, p)

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)["error"]
        # print(e) # 에러내용 전체 표시 위한 코드
        print(error["message"] + "\n")

        return -1

    return 1

# registration
def sign_up(**kwargs):
    print("Wait a moment\n")
    
    try:
        user = auth.create_user(**kwargs)

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)["error"]
        
        print(error["message"] + "\n")

    return 1


# password reset
def forgot_pw(email):
    print("Wait a moment\n")

    try:
        auth.get_user_by_email(email)

    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)["error"]
        # print(e)
        print(error["message"] + "\n")

        return -1

    return 1


if __name__ == "__main__":
    print("1. Sing in")
    print("2. Sing up")
    print("3. Forgot Password")

    choice = int(input("Input: "))
    print()

    user = [0]

    if choice == 1:
        print("Sing in")

        while True:
            email = input("Email: ")
            pw = getpass("Password: ")

            if sign_in(email, pw, user) == 1:
                break

        print("Successfully signed in to TossSync!")

    elif choice == 2:
        print("Sign up")

        while True:
            email = input("Email: ")
            pw = getpass("Password: ")

            user_info = {'email': email, 'password': pw}
            
            if sign_up(**user_info) == 1:
                break

        print("Successfully signed up to TossSync!")
        print("Check your e-mail")

        link = firebase_admin.auth.generate_email_verification_link(email)        
        
        # TODO: email
        # Construct email from a template embedding the link, and send using a custom SMTP server.
        send_custom_email(email, link)
        #########################

    elif choice == 3:
        print("Forgot password")

        while True:
            email = input("Email: ")

            if forgot_pw(email) == 1:
                break

        link = auth.generate_password_reset_link(email)
        print("Password reset address has been sent by email.")

        # TODO: email
        send_custom_email(email, link)