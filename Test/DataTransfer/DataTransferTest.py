import pytest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from Util.Android.adb_commands import adb_action

CAPABILITIES = {
    "platformName": "Android",
    "appium:deviceName": "Android",
    "appium:platformVersion": "14",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.yahoo.mobile.client.android.yahoo",
    "appium:appActivity": "com.yahoo.doubleplay.stream.presentation.view.activity.MainNavigationActivity"
}

@pytest.fixture()
def driver_setup():
    print("Setting up Appium driver...")
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    print("Quitting Appium driver...")
    driver.quit()

class TestDataTransfer:
    def test_capture_data_paste_in_notes(self, driver_setup):
        """
        Given the user opens the Yahoo News app
        When the user see's the bottom navigation bar
        Then record the text of each tab and paste it a notes app

        Assumptions: The notes app has only 0 notes at initial start
        """
        expected_tab_count = 4
        expected_tab_texts = ["Home", "Top stories", "Notifications", "Profile"]
        expected_note_count = 1
        expected_note_text = "Yahoo News Bottom Tab Text. Home, Top stories, Notifications, Profile. "
        driver = driver_setup
        wait = WebDriverWait(driver, 5)

        bottom_tab_bar = wait.until(
            ec.visibility_of_element_located((AppiumBy.ID, "com.yahoo.mobile.client.android.yahoo:id/bottomTabBar"))
        )

        # Find all the children nodes of the bottomTabBar
        all_children_in_bar = bottom_tab_bar.find_elements(AppiumBy.XPATH, ".//android.widget.TextView")

        # Assertion 1: Verify the correct number of tabs found (which should be 4)
        assert len(
            all_children_in_bar) == expected_tab_count, f"Expected {expected_tab_count} tabs, but found {len(all_children_in_bar)}"

        found_text_bottom_tab_bar: list = []
        for child in all_children_in_bar:
            print(f"Child element text: {child.text}")
            found_text_bottom_tab_bar.append(child.text)

        # Assertion 2: Verify the text of each tab
        assert sorted(found_text_bottom_tab_bar) == sorted(expected_tab_texts)

        # Change how the spaces because the Google Note's App doesn't like spaces and needs to use escape characters
        for index, text in enumerate(found_text_bottom_tab_bar):
            if text.__contains__(" "):
                found_text_bottom_tab_bar[index] = text.replace(" ", '\ ')

        # Switch to Google Note App
        print("Terminating the current app (Yahoo News)...")
        driver.terminate_app("com.yahoo.mobile.client.android.yahoo")
        time.sleep(1)  # Not my proudest moment of using this kind of wait
        print("Opening Google Note's app...")
        driver.activate_app("com.google.android.keep")

        wait.until(ec.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/speed_dial_create_close_button"))).click()
        wait.until(ec.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/new_note_button"))).click()

        # Wait for and interact with the title field
        wait.until(ec.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/editable_title")))
        title_edittext = driver.find_element(AppiumBy.ID, "com.google.android.keep:id/editable_title")
        title_edittext.click()
        wait.until(
            lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/editable_title").get_attribute("focused") == "true"
        )
        title_edittext.send_keys("Yahoo News Bottom Tab Text")

        # Wait for and interact with the note field
        note_edittext = driver.find_element(AppiumBy.ID, "com.google.android.keep:id/edit_note_text")
        note_edittext.click()
        wait.until(
            lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/edit_note_text").get_attribute("focused") == "true"
        )

        # Format and paste the captured text using ADB
        format_found_text: str = ',\\ '.join(found_text_bottom_tab_bar)
        adb_action(["input", "text", format_found_text])
        # note_edittext.send_keys(format_found_text)  # try out a different alternative as this line doesn't send the keys

        # Click the "Navigate up" button to save the note
        wait.until(ec.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Navigate up"))).click()

        # Wait for the Note's card views to appear
        grid_layout_view = wait.until(lambda x: x.find_element(AppiumBy.ID, "com.google.android.keep:id/notes"))
        all_children_in_card_grid_view = grid_layout_view.find_elements(AppiumBy.XPATH, ".//androidx.cardview.widget.CardView")

        # Assertion 3: Check if there is only a singular card in the note's grid view
        assert len(all_children_in_card_grid_view) == expected_note_count

        # Assertion 4: Check if the card's text has the correct text
        assert all_children_in_card_grid_view[0].tag_name == expected_note_text
