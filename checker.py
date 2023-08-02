import requests
import threading
import ctypes
import time
import math
import sys
import colorama
from colorama import Fore

Wonderland_Banner = f"""{Fore.MAGENTA}
      ▄▄▌ ▐ ▄▌       ▐ ▄ ·▄▄▄▄  ▄▄▄ .▄▄▄  ▄▄▌   ▄▄▄·  ▐ ▄ ·▄▄▄▄  
      ██· █▌▐█▪     •█▌▐███▪ ██ ▀▄.▀·▀▄ █·██•  ▐█ ▀█ •█▌▐███▪ ██ 
      ██▪▐█▐▐▌ ▄█▀▄ ▐█▐▐▌▐█· ▐█▌▐▀▀▪▄▐▀▀▄ ██▪  ▄█▀▀█ ▐█▐▐▌▐█· ▐█▌
      ▐█▌██▐█▌▐█▌.▐▌██▐█▌██. ██ ▐█▄▄▌▐█•█▌▐█▌▐▌▐█ ▪▐▌██▐█▌██. ██ 
       ▀▀▀▀ ▀▪ ▀█▄▀▪▀▀ █▪▀▀▀▀▀•  ▀▀▀ .▀  ▀.▀▀▀  ▀  ▀ ▀▀ █▪▀▀▀▀▀• 
       {Fore.RESET}
"""


class Checker:

  def __init__(self, telegram_bot_token):
    self.threads = 80
    self.hits = []
    self.fails = []
    self.start_time = 0
    self.fails_file = open('Wonderland/failed.txt', 'a')
    self.hits_file = open('Wonderland/hits.txt', 'a')
    self.is_running = False
    self.telegram_bot_token = telegram_bot_token
    self.telegram_chat_id = -1001769800447  # Replace with your channel chat ID
    self.wait_time = 3  # Wait time in seconds between messages
    self.requests_count = 0
    self.requests_per_second = 0

  def load_emails_from_file(self, filename):
    with open(filename, 'r') as file:
      return [line.strip() for line in file]

  def wait_for_enter(self):
    print(Wonderland_Banner)
    input(
      f"      ( {Fore.MAGENTA}!{Fore.RESET} ) Press Enter start the process.\n"
    )

  def start_threads(self):
    self.start_time = time.time()  # Record the start time
    for _ in range(self.threads):
      threading.Thread(target=self.check_emails).start()

  def check_emails(self):
    while self.is_running:
      try:
        email = self.emails.pop(0)  # Get the first email from the list
      except IndexError:
        return  # Stop the thread if there are no more emails to check

      r = requests.get(f"https://mail.google.com/mail/gxlu?email={email}")
      self.requests_count += 2.5

      try:
        if "Set-Cookie" in r.headers:
          self.fails.append(email)
          print(f"{email} - {Fore.RED}Taken{Fore.RESET}")
          print(email, file=self.fails_file)
          self.fails_file.flush()  # Flush output to the file
        else:
          self.hits.append(email)
          print(f"{email} {Fore.GREEN}- Available{Fore.RESET}")
          print(email, file=self.hits_file)
          self.hits_file.flush()  # Flush output to the file
      except Exception as e:
        self.fails.append(email)
        print(f"{email} - Error checking: {e}")
        print(email, file=self.fails_file)
        self.fails_file.flush()  # Flush output to the file

      self.update_console(email)

  def update_console(self, email):
    elapsed_time = time.time() - self.start_time
    if elapsed_time > 0:
      self.requests_per_second = self.requests_count / elapsed_time
      self.requests_per_second = math.ceil(self.requests_per_second)

    title = f"Wonderland✰ | R/S: {self.requests_per_second} | Checked: {len(self.hits) + len(self.fails)} | Hits: {len(self.hits)} | Taken: {len(self.fails)} | Current Email: {email}"
    ctypes.windll.kernel32.SetConsoleTitleW(title)

  def save_hits_to_file(self):
    with open('Wonderland/hits.txt', 'a') as hits_file:
      for email in self.hits:
        hits_file.write(f"{email}\n")

  def save_fails_to_file(self):
    with open('Wonderland/failed.txt', 'a') as fails_file:
      for email in self.fails:
        fails_file.write(f"{email}\n")

  def send_hits_to_telegram(self):
    if self.telegram_bot_token and self.telegram_chat_id:
      for email in self.hits:
        message = f"Wonderland - Available\nEmail: {email}\ndiscord.gg/wFQJ356WF9"
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        params = {"chat_id": self.telegram_chat_id, "text": message}
        response = requests.post(url, data=params)
        if response.status_code != 200:
          print(f"Failed to send message to Telegram channel: {response.text}")
        else:
          time.sleep(
            self.wait_time
          )  # Introduce a wait time between messages to avoid rate-limiting

  def run(self):
    self.is_running = True
    self.emails = self.load_emails_from_file('Wonderland/check_gmail.txt')
    ctypes.windll.kernel32.SetConsoleTitleW("Wonderland✰ - Gmail Checker ")

    # Wait for the user to press Enter before starting the threads
    self.wait_for_enter()

    self.start_threads()

    # Wait for threads to finish before exiting
    for t in threading.enumerate():
      if t != threading.current_thread():
        t.join()

    self.is_running = False
    elapsed_time = time.time() - self.start_time
    print(f"{Fore.GREEN}\nTotal Hits:{Fore.RESET} {len(self.hits)}")
    print(f"{Fore.RED}Total Fails:{Fore.RESET} {len(self.fails)}")
    print(f"{Fore.MAGENTA}Elapsed Time:{Fore.RESET} {elapsed_time:.2f} seconds")
    print(f"{Fore.MAGENTA}R/S:{Fore.RESET} {self.requests_per_second}")
    print(f"{Fore.GREEN}Uploading{Fore.RESET} hits.txt to {Fore.BLUE}Telegram{Fore.RESET} ({self.telegram_chat_id}).. Be patient.{Fore.RESET}")

    # Save the hits and fails to the respective files
    self.save_hits_to_file()
    self.save_fails_to_file()

    # Send the hits to the Telegram channel
    self.send_hits_to_telegram()

    # Close files after writing
    self.fails_file.close()
    self.hits_file.close()


# Replace 'your_bot_token' with your actual bot token obtained from the BotFather
checker = Checker(
  telegram_bot_token='your_bot_token')
checker.run()
