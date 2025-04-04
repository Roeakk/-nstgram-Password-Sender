import os, uuid, string, random
try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests
import pyfiglet
import json
import time  

R = "\033[1;31m"
G = "\033[1;32m"
B = "\033[0;94m"
Y = "\033[1;33m"

br = pyfiglet.figlet_format("Simple Tool")
print(R + br)

class InstagramPasswordReset:
    def __init__(self):
        self.menu()

    def menu(self):
        print("[1] Send Password Reset (İnstgram)")
        print("[2] Get Obfuscated Email by Username (İnstgram)")
        print("[3] Get IP Information")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.password_reset_option()
        elif choice == "2":
            self.get_obfuscated_email_option()
        elif choice == "3":
            self.ip_lookup_option()
        else:
            print(R + "[ - ] Invalid choice!")
            self.menu()

    def password_reset_option(self):
        self.target = input("[ + ]  Email / Username : ").strip()
        if self.target.startswith("@"):
            print("[ - ] Enter User Without '@' ")
            input()
            exit()

        self.data = {
            "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }

        if "@" in self.target:
            self.data["user_email"] = self.target
        else:
            self.data["username"] = self.target

        self.send_password_reset()

    def send_password_reset(self):
        headers = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        }

        # Send the password reset request
        response = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers,
            data=self.data
        )

        # Check if obfuscated email is in the response
        if "obfuscated_email" in response.text:
            email_start = response.text.find('"obfuscated_email":"') + len('"obfuscated_email":"')
            email_end = response.text.find('"', email_start)
            obfuscated_email = response.text[email_start:email_end]

            print(G + f"[ + ] Obfuscated Email: {obfuscated_email}")
        else:
            print(R + f"[ - ] No obfuscated email found or error in response: {response.text}")

        input()
        exit()

    def get_obfuscated_email_option(self):
        self.target = input("[ + ]  Instagram Username: ").strip()

        if self.target.startswith("@"):
            self.target = self.target[1:]  # Strip '@' if included by mistake.

        self.get_obfuscated_email(self.target)

    def get_obfuscated_email(self, username):
        headers = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                          f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
        }

        # Instagram doesn't directly expose the obfuscated email unless you trigger the password reset process
        print("[ - ] Obfuscated email can only be retrieved via password reset. Please select option 1.")
        input()
        exit()

    def ip_lookup_option(self):
        ip_address = input("[ + ] Enter IP Address: ").strip()

        # Make the API call to ip-api.com to fetch information about the IP address
        self.get_ip_info(ip_address)

    def get_ip_info(self, ip):
        try:
            # Requesting data from the IP API
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url)
            data = response.json()  # Parsing the JSON response

            # Check if the response is successful
            if data['status'] == 'fail':
                print(R + "[ - ] Error: Could not retrieve information for the given IP.")
            else:
                # Print the JSON response neatly
                print(G + "[ + ] IP Information:")
                print(json.dumps(data, indent=4))

                # Ask if the user wants to save the information
                save_option = input("[ + ] Do you want to save this location data? (yes/no): ").strip().lower()

                if save_option == "yes":
                    self.save_ip_info(data)  # Save the IP info if user wants to

                # Wait for 3 seconds before clearing the screen and going back to the menu
                time.sleep(3)
                self.clear_screen_and_menu()  # Clear the screen and return to the main menu
                return
        except Exception as e:
            print(R + f"[ - ] Error occurred: {str(e)}")

        input()
        exit()

    def save_ip_info(self, data):
        # Get the user's desktop path
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # For Windows
        # For Linux/Mac, you can use this line instead:
        # desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        file_path = os.path.join(desktop_path, "IP_Info.txt")

        try:
            with open(file_path, 'w') as file:
                file.write(json.dumps(data, indent=4))  # Writing the data to a text file

            print(G + f"[ + ] IP Information has been saved to: {file_path}")
        except Exception as e:
            print(R + f"[ - ] Failed to save the file: {str(e)}")

    def clear_screen_and_menu(self):
        # Print a blank line to "clear" the output part of the screen
        print("\n" * 50)

        # Now reprint the header and menu again
        print(R + br)  # Reprint the header (Roeak Sifre Gonderici)
        self.menu()  # Show the menu again

InstagramPasswordReset()
