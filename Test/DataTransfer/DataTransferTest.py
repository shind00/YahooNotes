import pytest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options

from Robot.Note.NoteRobot import NoteRobot
from Robot.Yahoo.BottomNavigationTabRobot import BottomNavigationTabRobot
from Util.Android.adb_commands import adb_action
from Util.Android.setup import android_capabilities


@pytest.fixture()
def driver_setup():
    options = UiAutomator2Options().load_capabilities(android_capabilities)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
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
        bottom_nav_robot = BottomNavigationTabRobot(driver)
        note_robot = NoteRobot(driver)

        found_text_bottom_tab_bar = bottom_nav_robot.get_all_text_from_children()

        # Assertion 1: Verify the correct number of tabs found (which should be 4)
        assert len(found_text_bottom_tab_bar) == expected_tab_count

        # Assertion 2: Verify the text of each tab
        assert sorted(found_text_bottom_tab_bar) == sorted(expected_tab_texts)

        # Change how the spaces because the Google Note's App doesn't like spaces and needs to use escape characters
        for index, text in enumerate(found_text_bottom_tab_bar):
            if text.__contains__(" "):
                found_text_bottom_tab_bar[index] = text.replace(" ", '\ ')

        # Switch to Google Note App
        driver.terminate_app("com.yahoo.mobile.client.android.yahoo")
        time.sleep(1)  # wait for app to close
        driver.activate_app("com.google.android.keep")

        note_robot.click_fab_button()
        note_robot.click_text_button()
        note_robot.enter_title("Yahoo News Bottom Tab Text")

        # Wait for and interact with the note field
        note_robot.enter_body()
        # Format and paste the captured text using ADB
        format_found_text: str = ',\\ '.join(found_text_bottom_tab_bar)
        adb_action(["input", "text", format_found_text])
        # note_edittext.send_keys(format_found_text)  # try out a different alternative as this line doesn't send the keys

        note_robot.nav_back()

        all_children_in_card_grid_view = note_robot.get_all_elements_of_card_grid_view()

        # Assertion 3: Check if there is only a singular card in the note's grid view
        assert len(all_children_in_card_grid_view) == expected_note_count

        # Assertion 4: Check if the card's text has the correct text
        assert all_children_in_card_grid_view[0].tag_name == expected_note_text
