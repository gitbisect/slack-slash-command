import requests
import json
import datetime

class WebAPI(object):

    def __init__(self, token=None):

        self.users = Users(token=token)

        self.token = token
        self.headers = {'Host': 'api.slack.com',
                        'Accept': 'application/json',
                        'Authorization': 'Bearer %s' % self.token}
        self.base_url = 'https://slack.com/api/'
        self.params = {"token": token}

    def request(self, method, url, headers, params):

        if method == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'post':
            response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        r = json.loads(response.content)
        if not r['ok']:
            print("Error: {0}".format(response.content))
            return
        response = json.loads(response.content)
        return response

    def get(self, url, headers, params):

        return self.request('get', url, headers, params)

    def post(self, url, headers, params):

        return self.request('post', url, headers, params)

class Users(WebAPI):

    def __init__(self, token):
        self.token = token
        self.headers = {'Host': 'api.slack.com',
                        'Accept': 'application/json',
                        'Authorization': 'Bearer %s' % self.token,
                        'Content-Type': 'application/json; charset=utf-8'}
        self.base_url = 'https://slack.com/api/users'
        self.params = {"token": self.token}

    def info(self, user):

        params = self.params
        params['user'] = user
        return self.get(self.base_url + '.info', headers=self.headers, params=params)


    def list(self, presence=None, desired_fields=None):
        """
        Returns list of users with desired fields (all fields if not specified)
        :param desired_fields: List of desired fields in returned list, example:
            desired_fields = ['id', 'name', 'created', 'num_members']
        :return:
        """
        users = []
        params = self.params
        params['presence'] = presence
        r = self.get(self.base_url + '.list', headers=self.headers, params=params)
        for user in r['members']:
            if desired_fields:
                u = {}
                for field in desired_fields:
                    try:
                        u[field] = user[field]
                    except KeyError:
                        print("Could not get field " + field)
                        continue
                user = u
            users.append(user)
        return users

if __name__  == "__main__":
    with open('secure.json') as secure:
        api_token = json.load(secure)['slack-api-token']
    w = WebAPI(api_token)

    users = w.users.list(desired_fields=['profile', 'id'])
    users = [{'email': u['profile']['email'], 'id': u['id']} for u in users if 'email' in u['profile']]
    with open('slack_user_list.json', 'w') as outfile:
        json.dump(users, outfile, indent=4)