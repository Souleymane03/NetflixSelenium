import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from login import driver, user_login
import secrets
import mylisttools
import showtools
import genrepagetools

# NETFLIX CALLS THE PLAYER THE nfp AkiraPlayer. netflix player AkiraPlayer?



############################################################################################
############################################################################################
############################################################################################
############################################################################################
# PHASES:

# ACTIVE
# FIRST IDLE PHASE: UI DISAPPARS, ONLY VIDEO REMAINS
# SECOND IDLE PHASE: TITLE APPEARS, EVERYTHING GETS DARKER AS OVERLAY APPEARS

# IDLE PHASE 1.5????- diplays just the rating. Seems to only happen when the video is first played

# TOTALLY IDLE, YOU HAVE TO CLICK A SPECIFIC BUTTON IN THE CENTER OF THE PAGE TO

# VIDEO IS PLAYING, BUTTONS ARE STILL BEING DISPLAYED
# VIDEO IS PLAYING, BUTTONS ARE GONE (BACK TO IDLE BUT VIDEO IS PLAYING)


# REDITS ARE ROLLING, VIDEO PLAYER IS MADE SMALL, RECOMMENDATIONS ARE DISPLAYED
# TODO- I DID NOT ACCOUNT FOR THIS!!!! TODO- NEED TO FACTOR THIS IN AS WELL
# HAPPENS AFTER change_time_using_slidebar(driver, .99)
############################################################################################
############################################################################################
############################################################################################
############################################################################################

### ALL FUCNTIONS:
player_is_idle
wake_up_idle_player
wake_up_if_idle
player_is_paused
unpause_player
get_remaining_time
player_is_fullscreen


def player_is_idle(driver):
    """ change to full screen, add subtitles, max volume, and any other options user wants"""
    pass
    """ return bool is player is idle"""
    """ if player is playing, it is considered idle"""
    """ IDLE IF AND ONLY IF BUTTONS ARE BEING DISPLAYED"""
    # TODO- change the definition of idle? maybe player_is_showing_buttons ? palyer_is_showing_UI ?
    seek_forward_button = driver.find_element_by_css_selector('button[aria-label="Seek Forward"]')
    if seek_forward_button.is_displayed():
        print(" player is NOT idle")
        return(False)  # VIDEO PLAYER IS NOT IDLE
    else:
        print("player is idle")
        return(True)   # VIDEO PLAY IS IDLE


def wake_up_idle_player(driver):
    """buttons are gone with idle"""
    """ TODO- BUG- if player is TOTALLY idle, no activity in several minutes, this wont wake"""
    video_player_container = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
    video_player_container.click()  # Click the center of the screen to wake it up
    # WAIT FOR THE PAGE TO COMPLETELY WAKE UP
    wait = WebDriverWait(driver,10)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'button[aria-label="Seek Forward"]')))


def wake_up_if_idle(driver):
    """ ADD THIS TO EVERY FUNCTION THE SAME WAY I HAVE "OPEN JAWBONE IF NOT OPEN" WITH SHOWTOOLS"""
    if player_is_idle(driver):
        wake_up_idle_player(driver)


def player_is_paused(driver):
    """PAUSED IS IRREGARDLESS OF IDLE. IDLE DOES NOT IMPLY PAUSED
    A PLAYER IS ALWAYS PAUSED OR NOT PAUSED. THUS NOT NOT PAUSED IMPLIES PAUSED """
    wake_up_if_idle(driver)
    try:
        small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
        return True
    except NoSuchElementException:
        pass
        # print("could not find small play button during player_is_paused")
    try:
        small_pause_button = driver.find_element_by_css_selector('button[aria-label="Pause"]')
        return False
    except:
        print("player_is_paused couldnt find either play nor pause button, SOMETHING IS WRONG")


def unpause_player(driver):
    """ unpause player if paused. if not paused, do nothing """
    wake_up_if_idle(driver)
    if player_is_paused(driver):
        print("PAUSED")
        small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
        small_play_button.click()
    else:
        print("player is not paused, unpause_player is not executing")


def player_is_fullscreen(driver):
    """ this requires 'waking up' the player. TODO- See if its possible to not wake up"""
    """ A PLAYER IS ALWAYS EITHER FULL SCREEN OR NORMAL SCREEN. THUS NOT FULL SCREEN IMPLIES NORMAL
    """
    wake_up_if_idle(driver)
    # CASE 1- I CAN FIND THE FULL SCREEN BUTTON
    try:
        full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
        return(False)
    except NoSuchElementException:
        print("couldnt find the full screen button")
    # CASE 2- I CAN FIND THE SMALLSCREEN BUTTON
    try:
        normal_screen = driver.find_element_by_css_selector('button[aria-label="Exit full screen"]')
        return(True)
    except NoSuchElementException:
        print("player_is_fullscreen couldnt find either buttons, SOMETHING IS WRONG")


def make_fullscreen(driver):
    """ make fullscreen if not fullscreen. if fullscreen, do nothing"""
    wake_up_if_idle(driver)  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIING THIS
    if player_is_fullscreen(driver):
        print("player is already fullscreen! not executing make_fullscreen")
    else:
        full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
        full_screen_button.click()


def make_normal_screen(driver):
    """ make normal_screen if player is fullscreen. if normal screen already, do nothing"""
    wake_up_if_idle(driver)  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIING THIS
    if not player_is_fullscreen(driver):
        print("player is already normal screen, make_normal_screen not executing")
    else:
        normal_screen = driver.find_element_by_css_selector('button[aria-label="Exit full screen"]')
        normal_screen.click()


def player_is_muted(driver):
    """ return true if muted, false if else"""
    wake_up_if_idle(driver)
    try:
        muted_button = driver.find_element_by_css_selector('button[aria-label="Muted"]')
        return(True)
    except NoSuchElementException:
        pass
    try:
        volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
        return(False)
    except NoSuchElementException:
        pass
    print("player_is_muted couldnt find either the muted or volume button. SOMETHING IS WRONG")


def mute_player(driver):
    """ mute if unmuted. if already muted, do nothing"""
    wake_up_if_idle(driver)
    if player_is_muted(driver):
        print("player is already muted, mute_player not executing")
    else:
        volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
        volume_button.click()
        # small problem appeared. Muted the player causes the volume bar to stay open for
        # TODO- CLEAN THIS UP


def unmute_player(driver):
    """ unmute player if muted. If alraedy unmuted, do nothing"""
    wake_up_if_idle(driver)
    if player_is_muted(driver):
        muted_button = driver.find_element_by_css_selector('button[aria-label="Muted"]')
        muted_button.click()
        # small problem appeared. Muted the player causes the volume bar to stay open for
        # TODO- CLEAN THIS UP
    else:
        print("player is already unmuted, unmute_player not executing")

def volume_slider_is_open(driver):
    """ returns true if the slider is open, false if else"""
    # intentionally not waking up idle player. Idle player implies slider is not open
    try:
        volume_percentage = driver.find_element_by_css_selector('div.slider-bar-percentage')
        return(True)
    except NoSuchElementException:
        print("volume_slider_is_open couldnt find the volume slider, returning false")
        return(False)

def open_volume_slider(driver):
    """ hover over the volume button causing the volume slider to open"""
    """ since we are hovering, calling open_volume_slider when the slider is already open does 
    nothing, thus its safe to use open_volume_slider as a open_volume_slider_if_not_open function,
    but the user should NOTE that open_volume_slider_if_not_open is a defined function
    """
    """ TODO- TEST NEED TO TEST ALL VOLUME STATES (low,medium,high, muted) """
    wake_up_if_idle(driver)
    volume_container = driver.find_element_by_css_selector('div[data-uia="volume-container"]')
    # volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
    action = ActionChains(driver)
    action.move_to_element(volume_container).perform()
    # wait for the slider to appear
    wait = WebDriverWait(driver,10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.slider-bar-percentage')))

def open_volume_slider_if_not_open(driver):
    """ opens slider if not open, if open do nothing"""
    if volume_slider_is_open(driver):
        print("volume slider is already open, open_volume_slider_if_not_open not executing")
    else:
        open_volume_slider(driver)


def change_volume_using_percentage(driver, volume_percentage: float):
    """ change the volume to a percentage
    e.g. volume_percentage =.5 means 50% volume, .25 = 25% volume etc.
    """
    """ NETFLIX NAMES:
    POPUP VOLUME CONTROLLER/ SLIDER/ SCRUBER TARGET
    """
wake_up_if_idle(driver)
# I need to force the volume container open. MOUSING OVER should do fine
volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
action = ActionChains(driver)
action.move_to_element(volume_button).perform()
volume_bar = driver.find_element_by_css_selector('div.slider-bar-percentage')
action_2 = ActionChains(driver)
action.move_to_element_with_offset(volume_bar,0,volume_bar.size['height']*.5).click().perform()

def get_current_volume(driver):
    """ TODO"""
    # wake_up_if_idle(driver)
    volume_percentage = driver.find_element_by_css_selector('div.slider-bar-percentage')
    return(volume_percentage.text)



def skip_backward(driver):
    """ rewind the player 10 seconds using the seek back button. SHOULD WORK PAUSED OR UNPAUSED"""
    wake_up_if_idle(driver)
    #
    seek_back_button = driver.find_element_by_css_selector('button[aria-label="Seek Back"]')
    seek_back_button.click()


def skip_forward(driver):
    """ skip forward 10 seconds using the seek forward button. SHOULD WORK PAUSED OR UNPAUSED"""
    wake_up_if_idle(driver)
    #
    seek_forward_button = driver.find_element_by_css_selector('button[aria-label="Seek Forward"]')
    seek_forward_button.click()


def get_remaining_time(driver):
    """ returns the amount of time left in this specific show AS DISPLAYED IN THE BOTTOM RIGHT
    CORNER. NOTE- see get_show_duration . This could be refactored to use seek_time_scrubber"""
    """ NOT TESTED, TODO- Test"""
    wake_up_if_idle(driver)
    time_remaining = driver.find_element_by_css_selector('time.time-remaining__time')
    if time_remaining.text == '':
        print("GET_REMAINING_TIME FAILED, MAYBE THE PLAYER WAS IDLE???")
        return(time_remaining.text)
    else:
        return(time_remaining.text)


def get_current_time(driver):
    """ TODO"""
    pass


def get_show_duration(driver) -> str:
    """ return a str  'HH:MM:SS' """
    # no need to wake the
    seek_time_scrubber = driver.find_element_by_css_selector(
        'div[aria-label="Seek time scrubber"]')
    scrubber_value = seek_time_scrubber.get_attribute('aria-valuetext').split(" ")
    assert len(scrubber_value) == 3, "get_show_duration SCRUBBER_VALUE found extra values"
    return(scrubber_value[2])


def change_to_percentage_time(driver, percentage_of_movie_left: float):
    """
    INPUT:
    percentage_of_movie_left: float     e.g. .5 for 50%, .25 for 25%, .1 for 10%
    NOTE- NETFLIX CALLS THIS THE SCRUBBER?
    THIS IS THE BIG ONE. THE HARD PROBLEM.
    NOTE- Even If I could change the position by editing the html, thats not really testing the
    functionality of the slider. I need to use mouse locations to mimic user behavior
    """
    wake_up_if_idle(driver)
    scrubber_bar = driver.find_element_by_css_selector('div.scrubber-bar')
    action = ActionChains(driver)
    action.move_to_element_with_offset(
        scrubber_bar, scrubber_bar.size['width']*percentage_of_movie_left, 0).perform()
    action.click().perform()


def change_to_exact_time(driver, hours, minutes, seconds):
    """ User provides a time in the movie they want to navigate to
        e.g. 1 hour, 35 minutes, 20 seconds
        This function converts that to a percentage of the movie left, then uses
        change_to_percentage_time
    """
    """ TODO- Seems to be a +- 1 second difference. Im guessing its the fault of floating point
    arithemetic not representing the exact_time_as_percentage. COULD ALSO BE  PADDING/BORDER/MARGIN
    OF THE SCRUBBER ELEMENT BY THE BROWSER. 1 second difference BUG categorized as low priority
    """
    show_duration = get_show_duration(driver)  # returns a str 'HH:MM:SS'
    show_duration_list = show_duration.split(":")
    show_duration_in_seconds = (int(show_duration_list[0])*3600
                                + int(show_duration_list[1])*60
                                + int(show_duration_list[2])
    )
    exact_time_in_seconds = int(hours)*3600 + int(minutes)*60 + int(seconds)
    print(exact_time_in_seconds, show_duration_in_seconds)
    exact_time_as_percentage = exact_time_in_seconds / show_duration_in_seconds
    print(exact_time_as_percentage)
    change_to_percentage_time(driver, exact_time_as_percentage)


# def report_issue(driver):
#     """ It was once considered to add the ability to automate the process of reporting issues.
#     After consideration, the possibility of it being used for nefarious acts against Netflix led
#     to this function being scrapped """

def subtitle_menu_is_open(driver):
    """ return true if the subtitle menu is open, false if else"""
    """ TODO- CLEAN THIS UP"""
    # INTENTIONALLY NOT WAKING UP PLAYER. IDLE PLAYER MEANS MENU IS NOT OEPN
    try:
        english = driver.find_element_by_css_selector('li[data-uia="track-subtitle-English"]')
        return(True)  #  not all shows will have english subtitles
    except NoSuchElementException:
        return(False)   # SLOPPY CODE. OTHER CASES EXIST, BAD TRY EXCEPT


def open_subtitle_menu_if_not_open(driver):
    """ open subtitle menu if it is not already open. If it is open, do nothing"""
    wake_up_if_idle(driver)
    if subtitle_menu_is_open(driver):
        print("subtitle menu is already open, open_subtitle_menu_if_not_open isnt executing")
    else:
        subtitles_button = driver.find_element_by_css_selector('button[aria-label="Audio & Subtitles"]')
        subtitles_button.click()
        # wait until the menu is open
        wait = WebDriverWait(driver,10)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.track-list.structural.track-list-subtitles')))


def has_subtitles(driver):
    """ return true if the player already has subtitles enabled (OF ANY LANGUAGE). False if else"""
    wake_up_if_idle(driver)
    open_subtitle_menu_if_not_open(driver)
    #
    subtitles_languages_list = driver.find_element_by_css_selector(
        'div.track-list.structural.track-list-subtitles')
    # TODO- THIS IS LOOKS HORRIBLE. CLEAN THIS UP.
    actual_list = subtitles_languages_list.find_element_by_tag_name('ul')
    languages = actual_list.find_elements_by_tag_name('li')
    print(len(languages))
    #
    for language in languages:
        if 'selected' in language.get_attribute('class'):
            if language.text == 'Off':
                print("subtitles are turned off")
                return(False)
            else:
                print(f"found subtitle with language {language.text}")
                return(True)


def add_english_subtitles(driver):
    # TODO- IT WORKS BUT SEEMS SKETCHY. NEEDS TO BE TESTED. I THOUGHT SINCE THE SUBTITLE MODAL
    # WAS ALREADY OPENT THA OPENING IT AGAIN WITH SUBTITLES_BUTTON.CLICK() WAS GOING TO CAUSE A
    # PROBLEM. INVESTIGATE
    wake_up_if_idle(driver)
    open_subtitle_menu_if_not_open(driver)
    #
    # spanish = driver.find_element_by_css_selector('li[data-uia="track-subtitle-Spanish"]')
    english = driver.find_element_by_css_selector('li[data-uia="track-subtitle-English"]')
    english.click()


def change_audio_to_spanish(driver):
    """spoken language != subtitles. This function changes the verbal language to spanish"""
    """not fully tested, TODO-TEST"""
    wake_up_if_idle(driver)
    open_subtitle_menu_if_not_open(driver)
    #
    # spoken_language_container = driver.find_element_by_css_selector(
    #     'div.track-list structural track-list-audio')
    # spoken_language_list = spoken_language_container.find_element_by_tag_name('ul')
    spanish_audio = driver.find_element_by_css_selector('li[data-uia="track-audio-Spanish"]')
    spanish_audio.click()

# def change_spoken_language(driver , language):
#     """ going to add this to the "nice to have" category. Not pressing."""
#     """ TODO- GENERALIZATION FUCNTION takes in language: str and changes the spoken
#     language to that language"""
#     pass

# def change_all_settings(**KWARGS):
#     """ a super function that takes in a list of options and performs them"""






# ALL OF THE FOLLOWING BUTTONS WORK
# THIS IS A REFERENCE FOR DEVELOPMENT. TODO- DELETE THIS ONCE EVERYTHING IS FINISHED
back_arrow = driver.find_element_by_css_selector('button[data-uia="nfplayer-exit"]')
back_arrow.click

small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
small_play_button.click()

seek_back_button = driver.find_element_by_css_selector('button[aria-label="Seek Back"]')
seek_back_button.click()

seek_forward_button = driver.find_element_by_css_selector('button[aria-label="Seek Forward"]')
seek_forward_button.click()


volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
volume_button.click()  # Clicking the volume button mutes and unmutes the video, also adds slider

title = driver.find_element_by_css_selector('h4.ellipsize-text')
print(title.text)

subtitles_button = driver.find_element_by_css_selector('button[aria-label="Audio & Subtitles"]')
subtitles_button.click()  # clicking launches the subtitles modal, but clicking again doesnt close

full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
full_screen_button.click()  # Functions as both "make fullscreen" and "make small screen"
