import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
                flow = InstalledAppFlow.from_client_secrets_file('path/to/creds/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        with open('token.pickle','wb') as token:
                pickle.dump(creds, token)
    return build ('gmail', 'v1', credentials=creds)
    
def bulk_delete_messages(user_query):
    service = get_service()
    message_ids = []
    next_page_token = None

    print(f"Searching for all messages matching: '{user_query}'...")

    #pagination loop to move through all 19k emails matching the query
    while True:
         result = service.users().messages().list(
              userId='me',
              q=user_query,
              pageToken=next_page_token
         ).execute()

         messages = result.get('messages',[])
         if messages:
              message_ids.extend([msg['id'] for msg in messages])
              #print progess update everytime we find more emails
              print(f"Collected {len(message_ids)} IDs so far")
         next_page_token = result.get('nextPageToken')
         if not next_page_token:
              break
         
    if not message_ids:
         print("No messages found matching that query.")
         return
    
    print(f"\nSUCCESS: Found {len(message_ids)} total messages.")
    confirm = input("Are you sure you want to PERMANENTLY delete them? (yes/no): ")

    if confirm.lower() != 'yes':
         print("Deletion cancelled.")
         return
    
    #Batch Deletion loop
    #Gmail API allows batching up to 1000 IDs at a time
    for i in range(0, len(message_ids), 1000):
        batch = message_ids[i:i+1000]
        service.users().messages().batchDelete(
            userId='me',
            body={'ids' : batch}
        ).execute()
        print(f"Deleted {i + len(batch)} of {len(message_ids)}...")

    print("\nTask complete. Your inbox should be much lighter!")

if __name__ == '__main__':
        user_query = 'label:inbox {category:promotions category:social category:updates} older_than:1y -is:starred'
        bulk_delete_messages(user_query)