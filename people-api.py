import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class PeopleClient():
    def __init__(self):
        """Client for google People API.
        """
        self.credentials_path = os.path.join('credentials', 'credentials.json')
        self.token_dir = 'token'
        self.token_path = os.path.join(self.token_dir, 'token.pickle')
        # If modifying these scopes, delete the file token.pickle.
        self.scopes = ['https://www.googleapis.com/auth/contacts']
        self.creds = self.get_auth_token()
        self.service = build('people', 'v1', credentials=self.creds)

    def get_auth_token(self):
        """Shows basic usage of the People API.
        Prints the name of the first 10 connections.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def main(self):
        self.service = build('people', 'v1', credentials=self.creds)

        # Call the People API
        print('List 10 connection names')
        results = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
        connections = results.get('connections', [])

        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                # print(name)
                print(self.creds)


if __name__ == '__main__':
    client = PeopleClient()
    client.main()
