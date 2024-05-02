#!/usr/bin/env python3
import requests
import os
from questionary import prompt
import time
import sys
import random
from termcolor import colored
from colorama import Fore, Back, Style, init

init(autoreset=True)  
def print_mixed_colors_spider(twinkling_duration=8):
    spider = [
        '    / _ \\ ',
        '  \\_\\(_)/_/',
        '   _//""\\_',
        '    /   \\  '
    ]

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.WHITE, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX]

    start_time = time.time()

    while time.time() - start_time < twinkling_duration:
        for line in spider:
            colored_line = ''
            for char in line:
                colored_line += random.choice(colors) + char + Style.RESET_ALL + Back.RESET
            print(colored_line)
        sys.stdout.flush()
        time.sleep(0.1)
        print("\033c")

def twinkling_text(text, twinkling_duration=2):

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Back.LIGHTGREEN_EX, Fore.WHITE, Back.LIGHTBLUE_EX, Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX,  Fore.LIGHTYELLOW_EX, Back.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Back.LIGHTRED_EX, Fore.LIGHTBLACK_EX,  Back.LIGHTWHITE_EX, Back.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTWHITE_EX, Fore.LIGHTBLACK_EX, Back.WHITE]

    start_time = time.time()

    while time.time() - start_time < twinkling_duration:
        colored_text = [random.choice(colors) + char + Style.RESET_ALL + Back.RESET for char in text]
        sys.stdout.write(''.join(colored_text) + "\r")
        sys.stdout.flush()
        time.sleep(0.1)

    print('')

# Exemple d'utilisation
# print_mixed_colors_spider(twinkling_duration=10)

def fun_prompt():
    print(colored("Bienvenue sur l'outil d'osint sur telegram interactif dev par TRHACKNON ", 'cyan'))

    twinkling_text("osint telegram par TRHACKNON", twinkling_duration=4)
    print_mixed_colors_spider(twinkling_duration=5)

# fun_prompt()



def main():
    fun_prompt()

    questions = [
        {
            'type': 'input',
            'name': 'telegram_token',
            'message': 'Telegram Token (bot1xxx):',
        },
        {
            'type': 'input',
            'name': 'telegram_chat_id',
            'message': 'Telegram Chat ID (-100xxx):',
        }
    ]

    answers = prompt(questions)

    telegram_token = answers['telegram_token'].strip()
    telegram_chat_id = answers['telegram_chat_id'].strip()

    # Make sure to add this import statement at the beginning of your file
    if telegram_token.startswith('bot'):
        telegram_token = telegram_token[3:]

    print(f"\n{Fore.GREEN}Analysis of token: {telegram_token} and chat id: {telegram_chat_id}\n{Fore.RESET}")

    # Get Bot Info

    url = f"https://api.telegram.org/bot{telegram_token}/getMe"
    response = requests.get(url)
    telegram_get_me = response.json().get('result')

    if telegram_get_me:

        print(f"Bot First Name: {telegram_get_me['first_name']}")
        print(f"Bot Username: {telegram_get_me['username']}")
        print(f"Bot User ID: {telegram_get_me['id']}")
        print(f"Bot Can Read Group Messages: {telegram_get_me['can_read_all_group_messages']}")

        # Get Bot Status - Member or Admin

        url = f"https://api.telegram.org/bot{telegram_token}/getChatMember?chat_id={telegram_chat_id}&user_id={telegram_get_me['id']}"
        response = requests.get(url)
        if response.json().get('result'):
            telegram_get_chat_member = response.json().get('result')
            print(f"Bot In The Chat Is An: {telegram_get_chat_member['status']}")
        elif response.json().get('description'):
            if response.json().get('parameters') and 'migrate_to_chat_id' in response.json().get('parameters'): 
                print(f"{Fore.YELLOW}ATTENTION {response.json().get('description')} - Migrated to: {response.json().get('parameters')['migrate_to_chat_id']}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}ATTENTION {response.json().get('description')}{Fore.RESET}")

        # Get Chat Info

        url = f"https://api.telegram.org/bot{telegram_token}/getChat?chat_id={telegram_chat_id}"
        response = requests.get(url)
        telegram_get_chat = response.json().get('result')

        if 'title' in telegram_get_chat: print(f"Chat Title: {telegram_get_chat['title']}")
        print(f"Chat Type: {telegram_get_chat['type']}")
        print(f"Chat ID: {telegram_get_chat['id']}")
        if 'has_visible_history' in telegram_get_chat: print(f"Chat has Visible History: {telegram_get_chat['has_visible_history']}")
        if 'username' in telegram_get_chat: print(f"Chat Username: {telegram_get_chat['username']}")
        if 'invite_link' in telegram_get_chat: print(f"Chat Invite Link: {telegram_get_chat['invite_link']}")

        # Export Chat Invite Link

        url = f"https://api.telegram.org/bot{telegram_token}/exportChatInviteLink?chat_id={telegram_chat_id}"
        response = requests.get(url)
        telegram_chat_invite_link = response.json().get("result")

        print("Chat Invite Link (exported): " + str(telegram_chat_invite_link))

        # Create Chat Invite Link

        url = f"https://api.telegram.org/bot{telegram_token}/createChatInviteLink?chat_id={telegram_chat_id}"
        response = requests.get(url)
        telegram_chat_invite_link = response.json().get('result')

        if "invite_link" in telegram_get_chat: print(f"Chat Invite Link (created): {telegram_chat_invite_link['invite_link']}")

        # Get Chat Member Count

        url = f"https://api.telegram.org/bot{telegram_token}/getChatMemberCount?chat_id={telegram_chat_id}"
        response = requests.get(url)
        telegram_chat_members_count = response.json().get('result')

        print(f"Number of users in the chat: {telegram_chat_members_count}")

        # Get Administrators in chat

        url = f"https://api.telegram.org/bot{telegram_token}/getChatAdministrators?chat_id={telegram_chat_id}"
        response = requests.get(url)
        telegram_get_chat_administrators = response.json().get('result')

        if telegram_get_chat_administrators:
            print(f"Administrators in the chat:")
            for user in telegram_get_chat_administrators:
                print(user['user'])
    else:
        print(f'{Fore.RED}Telegram token is invalid or revoked.{Fore.RESET}')


if __name__ == '__main__':
    main()