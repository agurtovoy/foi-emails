import sys
from service import create_service

scope = { 'userId': 'me' }


def messages(service, labels, format):
    messages = service.users().messages()
    pageToken = None
    while True:
        result = messages.list(labelIds=labels, pageToken=pageToken, **scope).execute()
        for m in result.get('messages', []):
            yield messages.get(id=m.get('id'), format=format, **scope).execute()

        pageToken = result.get('nextPageToken', None)
        if not pageToken:
            break


def main(label):
    service = create_service()

    result = service.users().labels().list(**scope).execute()
    labels = [l.get('id') for l in result.get('labels', []) if l.get('name') == label]
    if not labels:
        print('Could not find label {}'.format(label))
        return

    for m in messages(service, labels, format='full'):
        print(m.get('payload'))
        


if __name__ == '__main__':
    main(*sys.argv[1:])
