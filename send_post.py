from selenium import webdriver


def login():
    driver = webdriver.PhantomJS('/Users/yangzhixiao/Documents/Tools/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get('https://vip.anjuke.com/login/')
    print(driver.title)


if __name__ == '__main__':
    login()


