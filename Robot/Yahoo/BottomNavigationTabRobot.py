from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BottomNavigationTabRobot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def get_all_text_from_children(self):
        bottom_tab_bar = self.wait.until(
            ec.visibility_of_element_located((AppiumBy.ID, "com.yahoo.mobile.client.android.yahoo:id/bottomTabBar"))
        )

        # Find all the children nodes of the bottomTabBar
        tab_labels = bottom_tab_bar.find_elements(AppiumBy.XPATH, ".//android.widget.TextView")

        tab_texts = []
        for label in tab_labels:
            tab_texts.append(label.text)

        return tab_texts