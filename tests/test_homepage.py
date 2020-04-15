import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import secrets
import pagemodels.homepage
import pagemodels.showtoolspage
import tests.test_loginpage
import tests.pickledlogin

# # - ROWS: Queue, genre , continue watching , trending now, similars, because you added,\
# # new release, top ten, netflix originals, popular titles, big row, most watched

# IMPORTANT VOCABULARY:
# Jawbone-
# Bob-container- AKA SHOW_PREVIEW
# show_element-
# row_element

# TEST CATEGORIES (CTRL + K + CTRL + 0 TO COLLAPSE ALL)
# 1.) ROW TESTS (e.g. row left row right)
# 2.) SHOW TESTS (e.g. upvote show, add show to my list)
# 2a- PLAY TESTS
# 2b- MY LIST TESTS
# 2c- UPVOTE/DOWNVOTE TESTS
# 2d- GENERAL DATA INTEGRITY TODO(show_preview maturity rating agrees with jawbone maturity rating)


# # # # DELETE ME
# chromedriver_path = secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)
# tests.pickledlogin.pickled_login(driver)

# driver.get('https://www.netflix.com/watch/60023071?trackId=14170286&tctx=2%2C1%2C\
#     fc2cbd3b-8737-4f69-9a21-570f1a21a1a3-42400306%2C3f5aa22b-d569-486c-b94d-a8503e6725\
#     ae_22068878X3XX1586569622702%2C3f5aa22b-d569-486c-b94d-a8503e6725ae_ROOT')

class HomePageTests(unittest.TestCase):
    """ tests for the homepage of netflix. AKA netflix.com/browse"""

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver and login. See tests.pickledlogin for more"""
        chromedriver_path = secrets.chromedriver_path
        cls.driver = webdriver.Chrome(executable_path=chromedriver_path)
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ TODO-"""
        cls.driver.quit()

    def setUp(self):
        """ load some random movie, Minority Report with Tom Cruise in this instance """
        self.driver.get("https://www.netflix.com/browse")

    # ROW FUNCTIONS/OPERATIONS
    # def test_scroll_right_queue_row(self):
    #     """ scroll right in the queue/mylist row and assert the shows have changed"""
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     queue_row = home_page.get_queue_row()

    #     current_shows = home_page.get_currently_displayed_in_row(queue_row)
    #     current_shows_titles = [show.text for show in current_shows]

    #     home_page.row_page_right(queue_row)

    #     time.sleep(3)
    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     intersection_titles = [title for title in new_show_titles if title in current_shows_titles]

    #     # ASSERT THAT THE LIST OF DISPLAYED SHOW HAS NOTHING IN COMMON
    #     self.assertTrue(intersection_titles == [])

    # def test_scroll_left_queue_row(self):
    #     """ scroll right then left in the queue/mylist row and assert the shows have changed"""
    #     # have to scroll right before scroll left is an option
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     queue_row = home_page.get_queue_row()

    #     # home_page.row_page_right(queue_row)
    #     home_page.row_page_right(queue_row)

    #     time.sleep(3)
    #     current_shows = home_page.get_currently_displayed_in_row(queue_row)
    #     current_shows_titles = [show.text for show in current_shows]

    #     home_page.row_page_left(queue_row)

    #     time.sleep(3)
    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     intersection_titles = [title for title in new_show_titles if title in current_shows_titles]

    #     # ASSERT THAT THE LIST OF DISPLAYED SHOW HAS CHANGED
    #     self.assertTrue(intersection_titles == [])

    # # def test_open_explore_all_first_genre_row(self):
    # #     """ some rows have an "Explore all" button next to the title of the row"""
    # #     """ TODO- ADD THIS FUCNTIONALITY TO homepage.py, then write this test"""
    # #     pass

    # # SHOW FUNCTIONS (see showtoolspage.py)
    # # PLAY TESTS
    # def test_play_first_show_in_my_list_from_jawbone(self):
    #     """ """
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     queue_row = home_page.get_queue_row()

    #     first_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.play_show_from_jawbone(first_show)

    #     time.sleep(3)
    #     # 'watch' is always in the url for the netflix AKIRA PLAYER
    #     self.assertIn('watch', self.driver.current_url)

    # def test_play_first_show_in_my_list_from_show_preview(self):
    #     """ """
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     queue_row = home_page.get_queue_row()

    #     first_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.play_show_from_show_preview(first_show)

    #     time.sleep(3)
    #     # 'watch' is always in the url for the netflix AKIRA PLAYER
    #     self.assertIn('watch', self.driver.current_url)

    # def test_play_first_show_in_continue_watching_row(self):

    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     cont_watching_row = home_page.get_continue_watching_row()

    #     first_show = home_page.get_first_show_in_row(cont_watching_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.play_show_from_jawbone(first_show)

    #     time.sleep(5)  # Have to wait for the url to change TODO- clean this up
    #     # 'watch' is always in the url for the netflix AKIRA PLAYER
    #     self.assertIn('watch', self.driver.current_url)
    #     # TODO- THIS ASSERTS THAT SOME SHOW IS BEING WATCHED. NOT THA first_show is being watched
    #     # SEE IF THERE IS A WAY TO ASSERT THE TITLE IS PRESENT SOMEWHERE

    # # def test_play_random_show(self):
    # #     """ not really a test but a cool function I want to have somewhere"""
    # #     pass

    # # ADD/REMOVE MY LIST TESTS
    # def test_add_show_to_my_list_from_jawbone(self):
    #     """ add show to my list and assert that the show is now in my-list row"""
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

    #     # WE NEED TO FIND A RANDOM SHOW THAT IS NOT IN MY LIST ALREADY
    #     time.sleep(5)  # FIRST PAINT DOESNT INCLUDE A GENRE ROW, NEED TO LET THE PAGE LOAD
    #     first_genre_row = home_page.get_genre_rows()[0]
    #     genre_shows = home_page.get_currently_displayed_in_row(first_genre_row)

    #     for show in genre_shows:
    #         if show_tools.is_in_my_list_from_jawbone(show):
    #             show_tools.close_jawbone()
    #             time.sleep(3)
    #             # continue
    #         else:
    #             saved_title_name = show.text
    #             print(f"attempting to add {saved_title_name} to my-list")
    #             show_tools.add_show_to_my_list_from_jawbone(show)
    #             time.sleep(5)
    #             break
    #     else:
    #         # improbable edge case where a random genre will show a bunch of shows
    #         # ALL OF WHICH ARE ALREADY IN MY LIST
    #         print("test_add_show_to_my_list_from_show_preview FAILED TO FIND A RANDOM SHOW")
    #         raise KeyError("test_add_show_to_my_list_from_show_preview WEIRD EDGE CASE")

    #     self.driver.get('https://netflix.com')

    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     self.assertIn(saved_title_name, new_show_titles)

    # def test_remove_show_from_my_list_from_jawbone(self):
    #     """ remove a show from my-list from the jawbone
    #     and assert that the show is not in my-list row"""
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     queue_row = home_page.get_queue_row()

    #     first_show_in_q = home_page.get_first_show_in_row(queue_row)
    #     first_show_in_q_title = first_show_in_q.text

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.remove_show_from_my_list_from_jawbone(first_show_in_q)

    #     self.driver.get('https://netflix.com')

    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     self.assertNotIn(first_show_in_q_title, new_show_titles)

    # def test_add_show_to_my_list_from_show_preview(self):
    #     """ add show to my list from the show preview
    #     and assert that the show is now in my-list row"""
    #     # WORKED LIKE A CHARM. PRETTY COMPLICATED TEST. NICE TO SHOW OFF
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

    #     # WE NEED TO FIND A RANDOM SHOW THAT IS NOT IN MY LIST ALREADY
    #     time.sleep(5)  # FIRST PAINT DOESNT INCLUDE A GENRE ROW, NEED TO LET THE PAGE LOAD
    #     first_genre_row = home_page.get_genre_rows()[0]
    #     genre_shows = home_page.get_currently_displayed_in_row(first_genre_row)

    #     for show in genre_shows:
    #         if show_tools.is_in_my_list_from_jawbone(show):
    #             show_tools.close_jawbone()
    #             time.sleep(3)
    #             # continue
    #         else:
    #             show_tools.close_jawbone()
    #             time.sleep(3)
    #             saved_title_name = show.text
    #             print(f"attempting to add {saved_title_name} to my-list")
    #             show_tools.add_show_to_my_list_from_show_preview(show)
    #             time.sleep(5)
    #             break
    #     else:
    #         # improbable edge case where a random genre will show a bunch of shows
    #         # ALL OF WHICH ARE ALREADY IN MY LIST
    #         print("test_add_show_to_my_list_from_show_preview FAILED TO FIND A RANDOM SHOW")
    #         raise KeyError("test_add_show_to_my_list_from_show_preview WEIRD EDGE CASE")

    #     self.driver.get('https://netflix.com')

    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     self.assertIn(saved_title_name, new_show_titles)

    # def test_remove_show_from_my_list_from_show_preview(self):
    #     """ remove a show from my list from the show_preview
    #     and assert that the show is not in my-list(queue) row"""
    #     home_page = pagemodels.homepage.HomePage(self.driver)
    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

    #     queue_row = home_page.get_queue_row()
    #     first_queue_show = home_page.get_first_show_in_row(queue_row)
    #     saved_title_name = first_queue_show.text

    #     show_tools.remove_show_from_my_list_from_show_preview(first_queue_show)

    #     # Relaunching the page to see if the show has been removed from my_list
    #     self.driver.get("https://netflix.com")

    #     new_queue_row = home_page.get_queue_row()
    #     new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
    #     new_show_titles = [show.text for show in new_shows]

    #     self.assertNotIn(saved_title_name, new_show_titles)



















# THIS IS WHERE I LEFT OFF
# THE TESTS BELOW HAVE NOT BEEN TESTED







    # # UPVOTE/DOWNVOTE TESTS
    # def test_upvote_show_from_jawbone(self, show_element):
    #     """ upvote from the jawbone and assert upvoted"""

    #     home_page = pagemodels.homepage.HomePage(self.driver)

    #     queue_row = home_page.get_queue_row()
    #     first_queue_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.upvote_show_from_jawbone(first_queue_show)

    #     self.assertTrue(show_tools.is_upvoted_from_jawbone(first_queue_show))

    # def test_downvote_show_from_jawbone(self, show_element):
    #     """ """
    #     home_page = pagemodels.homepage.HomePage(self.driver)

    #     queue_row = home_page.get_queue_row()
    #     first_queue_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.downvote_show_from_jawbone(first_queue_show)

    #     self.assertTrue(show_tools.is_downvoted_from_jawbone(first_queue_show))

    # def test_upvote_show_from_show_preview(self, show_element):
    #     """ """
    #     home_page = pagemodels.homepage.HomePage(self.driver)

    #     queue_row = home_page.get_queue_row()
    #     first_queue_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.upvote_from_show_preview(first_queue_show)

    #     self.assertTrue(show_tools.is_upvoted_from_show_preview(first_queue_show))

    # def test_downvote_show_from_show_preview(self, show_element):
    #     """ """
    #     home_page = pagemodels.homepage.HomePage(self.driver)

    #     queue_row = home_page.get_queue_row()
    #     first_queue_show = home_page.get_first_show_in_row(queue_row)

    #     show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
    #     show_tools.upvote_from_show_preview(first_queue_show)

    #     self.assertTrue(show_tools.is_downvoted_from_show_preview(first_queue_show))

    #     # CLEANUP
