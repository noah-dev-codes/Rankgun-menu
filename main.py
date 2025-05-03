import requests
import asyncio
import os
import time
from colorama import Fore, Style

# pip install requests asyncio colorama rankgun
BaseUrl = "https://api.rankgun.works"
RequestsSession = requests.Session()


def request(method, endpoint, data=None):
    try:
        response = RequestsSession.request(method,
                                           f"{BaseUrl}{endpoint}",
                                           json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class RankGun:  # PROMOTE API

    def __init__(self, api_token, workspace_id):
        self.api_key = api_token
        self.workspace_id = workspace_id
        RequestsSession.headers.update({
            "api-token": self.api_key,
            "Content-Type": "application/json"
        })

    async def promote(self, username=None, user_id=None):
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be a valid integer")

        url = f"{BaseUrl}/roblox/promote"
        json_data = {
            "user_id": user_id,
            "workspace_id": self.workspace_id
        }
        print(f"[DEBUG] Promote Payload: {json_data}")
        response = RequestsSession.post(url, json=json_data)
        return response.text

    async def demote(self, username=None, user_id=None):  # DEMOTE API
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be a valid integer")

        url = f"{BaseUrl}/roblox/demote"
        json_data = {
            "user_id": user_id,
            "workspace_id": self.workspace_id
        }
        print(f"[DEBUG] Demote Payload: {json_data}")
        response = RequestsSession.post(url, json=json_data)
        return response.text

    async def set_rank(self, rank, username=None, user_id=None):
        data = {"workspace_id": self.workspace_id, "rank": rank}
        if username:
            data["username"] = username
        elif user_id:
            data["user_id"] = user_id
        else:
            return "Username or user_id is required."

        response = request("POST", "/roblox/set-rank", data)
        if response and "error" not in response:
            return f"Successfully set rank to {rank} for user: {username or user_id}"
        return "Failed to set rank."


def menu():
    clear_console()
    print(Fore.GREEN + "Select an action:" + Style.RESET_ALL)
    print("1. Promote")
    print("2. Demote")
    print("3. Set Rank")
    print("0. Exit")


def run():
    api_token = input("Enter your API token: ")
    workspace_id = input("Enter your workspace ID: ")
    client = RankGun(api_token, workspace_id)

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '0':
            print(Fore.YELLOW + "Exiting the menu." + Style.RESET_ALL)
            break

        clear_console()

        if choice == '1':
            try:
                user_id = int(input("Enter the user ID to promote: "))
                response = asyncio.run(client.promote(user_id=user_id))
                print(Fore.CYAN + f"{response}" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid user ID. Must be an integer." + Style.RESET_ALL)

        elif choice == '2':
            try:
                user_id = int(input("Enter the user ID to demote: "))
                response = asyncio.run(client.demote(user_id=user_id))
                print(Fore.CYAN + f"{response}" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid user ID. Must be an integer." + Style.RESET_ALL)

        elif choice == '3':
            try:
                rank = int(input("Enter the rank to set: "))
                user_id = int(input("Enter the user ID: "))
                response = asyncio.run(client.set_rank(rank, user_id=user_id))
                print(Fore.CYAN + f"{response}" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Rank and user ID must be integers." + Style.RESET_ALL)

        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

        time.sleep(3)
        clear_console()


if __name__ == "__main__":
    run()
