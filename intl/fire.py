import pyrebase, sys, requests, json, time


config = {
    'apiKey': "AIzaSyBpC9JIOlNziFTkRsmPQ6t3ODE68dirh9s",
    'authDomain': "intl-521af.firebaseapp.com",
    'databaseURL': "https://intl-521af.firebaseio.com",
    'projectId': "intl-521af",
    'storageBucket': "intl-521af.appspot.com",
    'messagingSenderId': "786163992412"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.sign_in_with_email_and_password(
    email='gorky0123@yahoo.com',
    password='Google123!')


class Fire:
    def __init__(self):
        self.db = firebase.database()
        self.urls = json.loads(requests.get('https://intl-521af.firebaseio.com/urls.json').text)


    def urls_stripped(self):
        return self.urls.values()
    

    def clear_urls(self):
        while True:
            yn = raw_input('Are you sure you want to clear all URLs? (Y/n) ')
            if yn.lower() == 'y' or yn.lower() == 'yes':
                r = requests.delete('https://intl-521af.firebaseio.com/urls.json')
                print 'URLs cleared.'
                break
            elif yn.lower() == 'n' or yn.lower() == 'no':
                break
            else:
                pass


    def add_url(self, *new_urls):
        if type(new_urls) == tuple:
            new_urls = list(*new_urls)
        else:
            new_urls = list(new_urls)
        
        amt_added = 0

        for u in new_urls:
            if not u.startswith('https://quotes.wsj.com/'):
                if not u.startswith('http://quotes.wsj.com/'):
                    print '"{}" isn\'t properly formatted for WSJ. Should look like "https://quotes.wsj.com/".'.format(u)
                    continue

            try:
                if u in self.urls.values():
                    print '"{}" already exists.'.format(u)
                    continue

            except TypeError:
                pass

            d = {'.value': u}
            d = json.dumps(d)
            r = requests.post('https://intl-521af.firebaseio.com/urls.json', data=d)
            amt_added += 1
        
        if amt_added != 0:
            if amt_added == 1:
                print '1 URL added.'
            else:
                print '{} URLs added.'.format(amt_added)
    

    def remove_url(self, *del_urls):
        amt_removed = 0
        removed = []

        for y in del_urls:
            for full_url_key, full_url in self.urls.iteritems():
                s = full_url.split('/')[-1]
                if y[0].lower() == s.lower():
                    r = requests.delete('https://intl-521af.firebaseio.com/urls/{}.json'.format(full_url_key))
                    amt_removed += 1
                    removed.append(full_url)

        if amt_removed == 0:
            print 'No URLs were removed.'
        else:
            print 'URLs removed: {}'.format(', '.join([x for x in removed]))

