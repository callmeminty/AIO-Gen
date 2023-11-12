import random
import smtplib
import string
import sys
from colorama import Fore, Style
import os
import requests
from bs4 import BeautifulSoup

class bcolors:
    PURPLE = '\033[38;2;144;238;144m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    print(bcolors.PURPLE + '''
    ███╗   ███╗██╗███╗   ██╗████████╗██╗   ██╗
    ████╗ ████║██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝
    ██╔████╔██║██║██╔██╗ ██║   ██║    ╚████╔╝ 
    ██║╚██╔╝██║██║██║╚██╗██║   ██║     ╚██╔╝  
    ██║ ╚═╝ ██║██║██║ ╚████║   ██║      ██║   
    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   
''' + bcolors.RESET)

def generator():
    banner()
    print(bcolors.PURPLE + "    ")
    print(bcolors.PURPLE + "    [1] Nitro")
    print(bcolors.PURPLE + "    [2] Minecraft")
    print(bcolors.PURPLE + "    [3] Spotify")
    print(bcolors.PURPLE + "    [4] NordVpn")
    print(bcolors.PURPLE + "    [5] Back")
    print(bcolors.PURPLE + "    ")

    choice = input("    > ")

    if choice == '1':
        banner()
        print(bcolors.PURPLE + "    ")
        num = input(bcolors.PURPLE + "> Number of Codes to Generate: ")
        generate_nitro_codes(int(num))
        print(bcolors.PURPLE + f"> Generated {num} Nitro codes. Check nitrocodes.txt")
        input("Press Enter to continue...")

    elif choice == '2':
        banner()
        print(bcolors.PURPLE + "    Minecraft Account Generator selected.")
        print(bcolors.PURPLE, "  ")
        num_accounts = input(bcolors.PURPLE + "> Number of Minecraft Accounts to Generate: ")
        print(bcolors.PURPLE, "  ")
        generate_minecraft_accounts(int(num_accounts))
        print(bcolors.PURPLE + f"> Generated {num_accounts} Minecraft accounts. Check minecraft_accounts.txt")
        print(bcolors.PURPLE, "  ")
        input("Press Enter to continue...")

def generate_nitro_codes(num):
    with open("nitrocodes.txt", "w") as f:
        for _ in range(num):
            code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
            f.write('https://discord.gift/')
            f.write(code)
            f.write("\n")

def generate_minecraft_accounts(num_accounts):
    # Example pastes.io URL containing emails and passwords
    pastes_url = 'https://pastes.io/raw/ppcqa573r8'

    try:
        response = requests.get(pastes_url)
        if response.status_code == 200:
            accounts_data = response.text.split('\n')[:num_accounts]

            with open("minecraft_accounts.txt", "w") as f:
                for account in accounts_data:
                    email, password = account.split(":")
                    username = email.split("@")[0]
                    f.write(f"{email}:{password}")
                    f.write("\n")
                    print(bcolors.PURPLE, "[!] Minecraft Account Generated:", f"{email}:{password}")
                    print("  ")
    except Exception as e:
        print("  ")
        print(bcolors.PURPLE, "[.] An error occurred:", e)

def generate_nordvpn_link():
    try:
        # NordVPN account generation URL
        nordvpn_url = 'https://bluealts.net/nordvpn/'

        # Send a GET request to the NordVPN account generation URL
        response = requests.get(nordvpn_url)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the generate button and extract the link
            generate_button = soup.find('button', {'id': 'createaccount'})
            link = generate_button['data-clipboard-text']

            print(bcolors.PURPLE, f"[+] Generated NordVPN link: {link}")
            print(bcolors.PURPLE, "  ")
        else:
            print(bcolors.PURPLE, "[.] Unable to fetch NordVPN link. Status code:", response.status_code)
            print(bcolors.PURPLE, "  ")

    except Exception as e:
        print(bcolors.PURPLE, "[.] An error occurred while generating NordVPN link:", e)
        print(bcolors.PURPLE, "  ")

def check_nitro_codes():
    found_nitro = None
    try:
        with open("nitrocodes.txt") as f:
            for line in f:
                nitro = line.strip("\n")
                url = f"https://discord.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
                r = requests.get(url)

                if r.status_code == 200:
                    print(bcolors.GREEN, "[GOOD]", nitro)
                    found_nitro = nitro
                    break
                else:
                    print(bcolors.PURPLE, "[BAD]", nitro)
    except FileNotFoundError:
        print("  ")
        print("nitrocodes.txt not found. Please generate Nitro codes first.")

    if found_nitro:
        with open("foundnitro.txt", "w") as found_file:
            found_file.write(found_nitro)

def check_minecraft_accounts():
    try:
        with open("minecraft_accounts.txt") as f:
            with open("goodminecraft.txt", "w") as good_file:
                for account in f:
                    account = account.strip("\n")
                    
                    # Check if the line contains the expected separator ":"
                    if ":" in account:
                        email, password = account.split(":")
                        result = verify_minecraft_account(email, password)
                        status = bcolors.GREEN + "[GOOD]" if result else bcolors.PURPLE + "[BAD]"
                        print(f"{status} (acc {email}:{password})" + bcolors.RESET)
                        if result:
                            good_file.write(f"[GOOD] (acc {email}:{password})\n")
    except FileNotFoundError:
        print("minecraft_accounts.txt not found. Please generate Minecraft accounts first.")

def verify_minecraft_account(email, password):
    # Minecraft API endpoint for checking account validity
    api_url = 'https://api.mojang.com/users/profiles/minecraft/' + email.split("@")[0]
    
    # Making a GET request to the Minecraft API
    response = requests.get(api_url, auth=(email, password))
    
    # If the status code is 200, the account is valid; otherwise, it's not valid
    return response.status_code == 200

def checker():
    banner()
    print(bcolors.PURPLE + "    ")
    print(bcolors.PURPLE + "    [1] Nitro Checker")
    print(bcolors.PURPLE + "    [2] Minecraft Checker")
    print(bcolors.PURPLE + "    [3] Spotify Checker")
    print(bcolors.PURPLE + "    [4] NordVPN Checker")
    print(bcolors.PURPLE + "    [5] Back")
    print(bcolors.PURPLE + "    ")

    choice = input("    > ")

    if choice == '1':
        banner()
        print(bcolors.PURPLE + "    Nitro Checker selected.")
        check_nitro_codes()
        input("Press Enter to continue...")

    elif choice == '2':
        banner()
        print(bcolors.PURPLE + "    Minecraft Checker selected.")
        check_minecraft_accounts()
        input("Press Enter to continue...")

    # Add other checker options here
    elif choice == '3':
        print("Spotify Checker selected.")
        # Implement Spotify checker logic
    elif choice == '4':
        banner()
        print(bcolors.PURPLE + "    NordVPN option selected.")
        generate_nordvpn_link()

    elif choice == '5':
        pass  # Back option
    else:
        print("Invalid choice. Please select a valid option.")

def main():
    while True:
        banner()
        print(bcolors.PURPLE + "    ")
        print(bcolors.PURPLE + "    [1] Generator")
        print(bcolors.PURPLE + "    [2] Checker")
        print(bcolors.PURPLE + "    [3] Exit")
        print("")
        choice = input("    > ")

        if choice == '1':
            generator()
        elif choice == '2':
            checker()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
