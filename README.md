# Gmail-Cleanup-Tool
<img width="192" height="145" alt="image" src="https://github.com/user-attachments/assets/9537b084-829a-4a64-b7e1-937f3d98e91c" />

## I wrote a Python script to automate the process of deleting 18k emails using the Gmail API.
#### This project was my introduction to managing large datasets via APIs.
## How I Built This
* **Language:** Python
* **API:** Google Gmail API (REST)
* **Auth:** Google Cloud Console & OAuth 2.0
* **Goal:** Efficiently find and permanently delete 18k + targeted emails

## What I Learned
#### Building this script taught me several "real-world" coding skills that I didn't get from tutorials:
* **API Credentials & Security:** I learned how to set up a project in the Google Cloud Console, enable specific API scopes, and handle sensitive files like credentials.json and token.pickle using .gitignore.
* **The OAuth2 Flow:** I implemented the logic to open a browser for login, generate a token, and refresh that token so the script stays authenticated.
* **Testing:** I started off with sending myself some test emails and running the script to first delete those then proceeded to edit the script to bulk delete rest of the emails
* **Batch Processing:** I researched and implemented a method to process messages in chunks to make the script more efficient.
* **Error Handling:** I had to reconfigure the script multiple times especially when it came to the script query to ensure it did not delete any of my sent or starred emails.

## Logic Behind the Script
#### The script follows a simple but effective logic:
* **Authenticate:** Establish a secure connection to my Gmail account.
* **Query:** Search for specific messages (e.g., label:inbox or category:promotions).
* **Loop & Delete:** Collect IDs of the matching emails and send a "Batch Delete" request to delete them permanently.
* **Verify:** Print a confirmation of how many emails were successfully processed.

## Security measures
#### Since this script deletes data, I built it to:
* Print the count of emails found before starting the deletion.
* Add a yes/no verification question before any of the emails could be deleted.
* Included a .gitignore file to ensure my private API keys never get uploaded to GitHub.


# Python Script to bulk delete emails from gmail account
## This is a python script I created to delete over 18k emails from a gmail account. I used a method which interacts with the Gmail API via Google Cloud Console.

