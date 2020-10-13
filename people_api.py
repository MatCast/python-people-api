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
        """Get Credientials and authorization token.
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
                    self.credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def __request_connections(self, page_size, fields, page_token):
        fields = ','.join(fields)
        return self.service.people().connections().list(
            resourceName='people/me',
            pageSize=page_size,
            personFields='names,emailAddresses',
            pageToken=page_token).execute()

    # def __get_next_page_token(self, results):
    #     results.

    def get_all_connections(self, page_size=10, fields=['emailAddresses']):
        """Get all the contacts from a person contacts."""
        next_page_token = None
        connections = []
        while True:
            results = self.__request_connections(page_size=page_size,
                                                 fields=fields,
                                                 page_token=next_page_token)
            next_page_token = results.get('nextPageToken')
            connections.extend(results.get('connections', []))
            if not next_page_token:
                return connections

    def print_connections(self):
        connections = self.get_all_connections(page_size=200)
        print(len(connections))
        for person in connections[:10]:
            emails = person.get('emailAddresses', [])
            if emails:
                email = (emails[0].get('displayName') + ':' +
                         emails[0].get('value'))
                print(email)
        return connections

    def main(self):
        body = {
            "emailAddresses": [{
                "displayName": "work",
                "value": "nuovo@work.com"
            }, {}]
        }
        results = self.service.people().createContact(body=body).execute()
        return results


if __name__ == '__main__':
    client = PeopleClient()
    connections = client.print_connections()
