from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class NoteRobot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_fab_button(self):
        self.wait.until(ec.element_to_be_clickable(
            (AppiumBy.ID, "com.google.android.keep:id/speed_dial_create_close_button"))).click()

    def click_text_button(self):
        self.wait.until(ec.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/new_note_button"))).click()

    def enter_title(self, msg):
        self.wait.until(ec.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/editable_title")))
        title_edittext = self.driver.find_element(AppiumBy.ID, "com.google.android.keep:id/editable_title")
        title_edittext.click()
        self.wait.until(
            lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/editable_title").get_attribute(
                "focused") == "true"
        )
        title_edittext.send_keys(msg)

    def enter_body(self):
        note_edittext = self.driver.find_element(AppiumBy.ID, "com.google.android.keep:id/edit_note_text")
        note_edittext.click()
        self.wait.until(
            lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/edit_note_text").get_attribute(
                "focused") == "true"
        )

    def nav_back(self):
        self.wait.until(ec.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Navigate up"))).click()

    def get_all_elements_of_card_grid_view(self):
        grid_layout_view = self.wait.until(lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/notes"))
        return grid_layout_view.find_elements(AppiumBy.XPATH, ".//androidx.cardview.widget.CardView")