from selenium import webdriver
import time
import os
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

username = os.environ.get('wellnessliving_username')
password = os.environ.get('wellnessliving_password')

driver = webdriver.Chrome(".\\webdriver\\chromedriver.exe")
driver.get("https://www.wellnessliving.com/login/essentials_of_athletics")

username_textbox = driver.find_element_by_id("template-passport-login")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("template-passport-password")
password_textbox.send_keys(password)

login_button = driver.find_element_by_xpath("//input[@name='b_submit' and @value='Log in']")
login_button.submit()

time.sleep(10)

element = driver.find_elements_by_class_name("js-item")[-1]
element.click()

time.sleep(5)

drop_down_menus = driver.find_elements_by_class_name("css-duration-drop-down-list")

time.sleep(3)

date_1 = datetime.datetime.now()
month_1 = date_1.strftime("%B")
day_1 = int(date_1.strftime("%d"))
year_1 = date_1.strftime("%Y")
time_1 = date_1.strftime("%X")

#edit
date_plus_2 = month_1 + " " + str(day_1 + 2) + " " + year_1

html_str = """
<!DOCTYPE html>
<html>
<head>
  <title> Gym Schedule </title>
</head>
<body>

<h1> {day_plus_2} </h1>

<h2> Gym Schedule ran at: {time_1} </h2>

</body>
</html>

""".format(day_plus_2=date_plus_2, time_1=time_1)

with open("index.html","a") as fp:
    #fp.write(str(weight_rack_num))
    fp.write(html_str)

count = 0
total_rows = len(drop_down_menus)
while total_rows > count:
    drop_down_menus = driver.find_elements_by_class_name("css-duration-drop-down-list")
    drop_down_menu = drop_down_menus[count]

    driver.execute_script("return arguments[0].scrollIntoView(true);", drop_down_menu)
    time.sleep(3)
    drop_down_menu.click()

    weight_rack_nums = driver.find_elements_by_class_name("service-name")
    weight_rack_num = driver.find_elements_by_class_name("service-name")[count].get_attribute('innerHTML')
    count += 1

    html_str = """

    <h3> {weight_rack_num} </h3>

    """.format(weight_rack_num=weight_rack_num)

    with open("index.html","a") as fp:
        #fp.write(str(weight_rack_num))
        fp.write(html_str)

    time.sleep(3)
    drop_down_one_15 = drop_down_menu.find_element_by_css_selector("li[data-option-array-index='2']").click()

    time.sleep(2)
    driver.find_element_by_css_selector('.js-button-next.button-next').click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    time_now = datetime.datetime.now()
    
    #edit
    time_day = time_now.day + 2

    try:
        driver.find_element_by_css_selector("a[data-index='" + str(time_day) + "']").click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        available_times = driver.find_elements_by_class_name("js-appointment-time-item")
        count1 = 0
        for a_time in available_times:
           
            with open("index.html","a") as fp:
                fp.write(str(available_times[count1].get_attribute('innerHTML')))
                count1 += 1

    except NoSuchElementException:
        print("No such element")

    time.sleep(3)

    driver.back()
    
    time.sleep(5)

    target = driver.find_elements_by_class_name("js-item")[-1]
    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    time.sleep(3)
    target.click()
    time.sleep(3)
