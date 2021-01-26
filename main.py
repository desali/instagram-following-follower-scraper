from igramscraper.instagram import Instagram
from time import sleep

import config


def start_parsing(file_name):
    print("Creating instagram instance")
    instagram = Instagram()

    print(f"Logging in with username {config.USERNAME}")
    instagram.with_credentials(config.USERNAME, config.PASSWORD)
    instagram.login()

    sleep(4)

    print(f"Opening {file_name} to read usernames")
    f = open(file_name, "r")
    usernames = f.readlines()
    print(f"Loaded {len(usernames)} usernames")

    username_index = 1
    for username in usernames:
        print(f"Starting parsing {username_index} index out of {len(usernames)}. Username: {username.strip()}")
        parse_user(instagram, username.strip())

        username_index += 1
        sleep(10)


def parse_user(instagram, username):
    print(f"Getting instagram account of username {username}")
    account = instagram.get_account(username)
    sleep(2)

    print(f"Creating file - {'export/' + username + '_following.txt'}")
    f_following = open("export/" + username + "_following.txt", "w+")
    print(f"Getting followings of {username} with page size 50")
    following = instagram.get_following(account.identifier, account.follows_count, 50, delayed=True)
    print(f"Followers loaded {len(following['accounts'])}. And starting to write to file")
    for following_user in following['accounts']:
        f_following.write(following_user.username + "__" + following_user.full_name + "\n")

    print("Closing following file")
    f_following.close()

    print(f"Creating file - {'export/' + username + '_followers.txt'}")
    f_followers = open("export/" + username + "_followers.txt", "w+")
    print(f"Getting followers of {username} with page size 50")
    followers = instagram.get_followers(account.identifier, account.followed_by_count, 50, delayed=True)
    print(f"Followers loaded {len(followers['accounts'])}. And starting to write to file")
    for followed_user in followers['accounts']:
        f_followers.write(followed_user.username + "__" + followed_user.full_name + "\n")

    print("Closing followers file")
    f_followers.close()

    print(f"Ended parsing of user {username}\n")


if __name__ == '__main__':
    usernames_file = 'data.txt'

    print(f"Scraper started. Loading file {usernames_file}")
    start_parsing(usernames_file)
