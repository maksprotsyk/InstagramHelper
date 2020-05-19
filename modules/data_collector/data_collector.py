"""
Module for collecting data with Processor class
"""
import time
from selenium.common.exceptions import JavascriptException
from modules.data_collector.processor import Processor


# phase1.txt
def find_following(login: str, password: str,
                   user: str, filename: str) -> None:
    '''
    Collects user followings and writes them into a file
    '''
    processor = Processor()
    processor.login(login, password)
    processor.get_following(user, filename)
    processor.quit()


# phase3.txt
def filter_users(filename: str, new_file: str,
                 key) -> None:
    """
    Filters users from the first file
    and writes them into the second one
    """
    in_file = open(filename)
    output = open(new_file, 'a')
    processor = Processor()
    for line in in_file.readlines():
        user = line.strip()
        print(user, end=' ')
        if key(processor, user):
            output.write(f'{user}\n')
            print('True')
        else:
            print('False')
    in_file.close()
    output.close()


# phase2.txt
def delete_duplicates(filename: str, new_file: str) -> None:
    """
    Checks file for duplicates and deleted them
    """
    users = set()
    with open(filename) as in_file:
        for line in in_file.readlines():
            users.add(line)
    with open(new_file, 'a') as output:
        for user in users:
            output.write(user)


# phase4.csv
def write_followings(login: str, password: str,
                     filename: str, new_file: str) -> None:
    """
    Writes followings of the users from the first file
    to the second file in format
    username, subscriptions separated by comma
    """
    processor = Processor()
    processor.login(login, password)

    with open(filename) as in_file:
        for user in in_file.readlines():
            user = user.strip().replace(',', '')

            with open(new_file, 'a') as output:
                output.write(f'\n{user},')
            print(f"User: {user}")

            try:
                processor.get_following(user, new_file)
            except (AttributeError, JavascriptException) as err:
                print(err)
                time.sleep(120)

            time.sleep(15)

            print('ended')
    processor.quit()


def get_first_posts(num: int, username: str,
                    processor: str) -> None:
    """
    Gets captions of the first n post for the given user
    """
    posts = 0
    row = 1
    col = 1
    text = ''
    while posts < num:
        text += processor.get_post_description(username, row, col) + ' '
        posts += 1
        if row % 3:
            row += 1
        else:
            row = 1
            col += 1
    return text


# phase5.txt
def collect_users(filename: str, new_file: str) -> None:
    """
    Collects the follows from the first file
    (in format user, follows) and writes
    them in the second one
    without duplicates
    """
    users = set()
    with open(filename) as in_file:
        for line in in_file.readlines():
            line = line.strip()
            profiles = line.split(',')[1].split()
            users |= set(profiles)
    with open(new_file, 'a') as output:
        for user in users:
            output.write(f'{user}\n')


def get_first_users(filename: str, new_file: str, num=100) -> None:
    """
    Gets only first num follows of the user from the first file
    and writes into the second
    """
    with open(filename) as in_file:
        for line in in_file.readlines():
            with open(new_file, 'a') as output:
                line = line.strip().split(',')
                profiles = line[1].split()[:num]
                user = line[0]
                output.write(f'{user},{" ".join(profiles)}\n')


# filter for small accounts
FILTER1 = lambda x, y: (x.followers_num(y) < 1000 and
                        50 < x.following_num(y) < 1000 and
                        not x.is_private())

# filter for big accounts
FILTER2 = lambda x, y: x.following_num() < 1000 < x.followers_num()


def get_posts(filename: str, new_file: str,
              processor: Processor, key) -> None:
    """
    Gets posts of the users from the
    given files and saves them to anothe
    (filters them with the key function)
    """

    with open(filename) as in_file:
        with open(new_file, 'a') as output:
            for line in in_file.readlines():
                user = line.strip()
                if key(processor, user):
                    output.write(user
                                 + ' '
                                 + get_first_posts(5, user, processor)
                                 .replace('\n', ' ')
                                 .replace(',', ' ')
                                 + '\n')


if __name__ == '__main__':
    pass
