import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('creds/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle','wb') as token:
                pickle.dump(creds, token)
        return build ('gmail', v1, credentials=creds)
    
def bulk_delete_messages(query):
    service = get_service()

    # 1. Search for messages that match the query
    result = service.users().messages().list(userID='me', q=query).execute()
    messages = result.get('messages',[])

    if not messages:
        print("No messages found matching that query.")
        return
    
    print(f"Found {len(messages)} messages. Starting deletion...")

    # 2. Exctract IDs for batch deletion
    message_ids = [msg['id'] for msg in messages]

    #Gmail API allows batching up to 1000 IDs at a time
    for i in range(0, len(message_ids), 1000):
        batch = message_ids[i:i+1000]
        service.users().messages().batchDelete(
            userId='me',
            body={'ids' : batch}
        ).execute()
        print(f"Deleted{len(batch)} messages...")

    print("Task complete.")

    if __name__ == '__main__':
        user_query = 'from:twin.tebz@gmail.com subject:TEST1'
        bulk_delete_messages(user_query)


