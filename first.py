import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

count = 0

path = 'D:\Python\Selenium\FirstDemo\chromedriver.exe'
cwd = os.path.join(os.getcwd(), 'chromedriver.exe')

account = 'user name'
passw = "password"

driver = webdriver.Chrome(cwd)
driver.implicitly_wait(30)
driver.maximize_window()
driver.get("https://www.instagram.com/")
assert "Instagram" in driver.title


def scrape_following():
    driver.get("https://www.instagram.com/{0}/".format(account))

    driver.find_element_by_partial_link_text("following").click()

    time.sleep(2)

    SCROLL_PAUSE = 2
    driver.execute_script("followersbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followersbox.scrollHeight;")

    # We need to scroll the followers modal to ensure that all followers are loaded
    while True:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

        time.sleep(SCROLL_PAUSE)

        new_height = driver.execute_script("return followersbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    following_list = []
    following_list_button = driver.find_elements_by_xpath("//a[@class='_2g7d5 notranslate _o5iw8 ']")
    i = 0
    for _ in following_list_button:
        i = i + 1
        print(i, _.text)
        following_list.append(_.text)

    return following_list


def scrape_followers():
    driver.get("https://www.instagram.com/{0}/".format(account))

    driver.find_element_by_partial_link_text("follower").click()

    time.sleep(2)

    SCROLL_PAUSE = 2
    driver.execute_script("followersbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followersbox.scrollHeight;")

    while True:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

        # Wait for page to load
        time.sleep(SCROLL_PAUSE)

        # Calculate new scrollHeight and compare with the previous
        new_height = driver.execute_script("return followersbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    followers_list = []
    followers_list_button = driver.find_elements_by_xpath("//a[@class='_2g7d5 notranslate _o5iw8 ']")
    i = 0
    for _ in followers_list_button:
        i = i + 1
        print(i, _.text)
        followers_list.append(_.text)

    return followers_list


def main():
    login = driver.find_element_by_link_text('Log in')
    print(login)
    login.click()
    time.sleep(3)

    username = driver.find_element_by_name("username")
    username.send_keys(account)
    password = driver.find_element_by_name("password")
    password.send_keys(passw)
    password.send_keys(Keys.ENTER)

    # In case if you have two-factor authentication
    # Uncomment if two-factor authentication is on and enter code in terminal
    # otp = input("Enter two step verification code")
    # time.sleep(5)
    #
    # verificationCode = driver.find_element_by_name("verificationCode")
    # verificationCode.send_keys(otp)
    # time.sleep(3)
    # verificationCode.send_keys(Keys.ENTER)

    # # End of two-factor authentication
    time.sleep(2)

    followers = scrape_followers()
    following = scrape_following()
    print(len(followers))
    print(len(following))
    followers.sort()
    following.sort()
    print("Followers\n", followers)
    print("Following\n", following)
    l3 = [x for x in following if x not in followers]
    print('Not following')
    print(l3)


main()
