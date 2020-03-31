from InstagramAPI import InstagramAPI

username = ''  # insert your username here
password = ''  # insert your password here


# creating an instance of InstagramAPI class
api = InstagramAPI(username, password)


def get_followings_names(num, api=api):

    # logins into given account
    api.login()

    # gets followings of the given user in json format
    api.getSelfUsersFollowing()
    result = api.LastJson['users']

    # returns first 'num' usernames of the given list
    return [result[i]['username'] for i in range(num)]


for item in get_followings_names(10):
    print(item)
