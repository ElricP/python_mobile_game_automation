import random
import cv2
import numpy as np
import win32api
import win32con
from ppadb.client import Client
import time
import sys
from win32api import GetSystemMetrics
from matplotlib import pyplot as plt
from PIL import Image
import pyautogui
import keyboard

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
global_needle_path = 'images/needles/'
global_debug = False


def mouse_callback(event, x, y, flags, params):
    # right-click event value is 2
    if event == 1:
        print([x, y])
        # global right_clicks
        # #store the coordinates of the right-click event
        # right_clicks.append([x, y])
        # #this just verifies that the mouse data is being collected
        # #you probably want to remove this later
        # print right_clicks


def mouse_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def random_sleep(secs):
    time.sleep(secs + random.random())


def random_sleep_extra(secs):
    time.sleep(secs - 2 + random.randint(0, 4) + random.random())


# return grouped length, max_loc. Only use the result when grouped length == 1
def check_needle(template, needle, threshold):
    result = cv2.matchTemplate(template, needle, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)
    print('Needle check best match: ' + str(max_val))
    y_loc, x_loc = np.where(result >= threshold)
    w = needle.shape[1]
    h = needle.shape[0]
    rectangles = []
    for (x, y) in zip(x_loc, y_loc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(len(rectangles))
    for (x, y) in zip(x_loc, y_loc):
        cv2.rectangle(template, (x, y), (x + w, y + h), (0, 255, 255), 2)
    if global_debug:
        cv2.rectangle(template, max_loc, (max_loc[0]+w, max_loc[1] + h), (0, 255, 255), 2)
        resized = cv2.resize(template, (540, 800))
        cv2.imshow('Check', resized)
        cv2.waitKey()
        cv2.destroyAllWindows()
    return len(rectangles), max_loc


def check_needle_lowest_match(template, needle, threshold):
    result = cv2.matchTemplate(template, needle, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)
    print('Needle check best match: ' + str(max_val))
    y_loc, x_loc = np.where(result >= threshold)
    y_min = max_loc[0]
    x_min = max_loc[1]
    w = needle.shape[1]
    h = needle.shape[0]
    rectangles = []
    for (x, y) in zip(x_loc, y_loc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(len(rectangles))
    for (x, y) in zip(x_loc, y_loc):
        cv2.rectangle(template, (x, y), (x + w, y + h), (0, 255, 255), 2)
        if y > y_min:
            y_min = y
            x_min = x
    # cv2.rectangle(template, max_loc, (max_loc[0]+w, max_loc[1] + h), (0, 255, 255), 2)
    # resized = cv2.resize(template, (540, 800))
    # cv2.imshow('Check', resized)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return len(rectangles), (x_min, y_min)


def check_needle_highest_match(template, needle, threshold):
    result = cv2.matchTemplate(template, needle, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)
    print('Needle check best match: ' + str(max_val))
    y_loc, x_loc = np.where(result >= threshold)
    y_max = max_loc[0]
    x_max = max_loc[1]
    w = needle.shape[1]
    h = needle.shape[0]
    rectangles = []
    for (x, y) in zip(x_loc, y_loc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(len(rectangles))
    for (x, y) in zip(x_loc, y_loc):
        cv2.rectangle(template, (x, y), (x + w, y + h), (0, 255, 255), 2)
        if y < y_max:
            y_max = y
            x_max = x
    # cv2.rectangle(template, max_loc, (max_loc[0]+w, max_loc[1] + h), (0, 255, 255), 2)
    # resized = cv2.resize(template, (540, 800))
    # cv2.imshow('Check', resized)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return len(rectangles), (y_max, x_max)


# return grouped length, max_loc. Only use the result when grouped length == 1
def check_needle_tap_fast(template, needle, threshold):
    result = cv2.matchTemplate(template, needle, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)
    print(str(max_val))
    if max_val > threshold:
        device.shell('input touchscreen tap 536 1748')


# scroll takes argument 'up' or 'down'
def scroll(up):
    x1 = random.randint(20, 60)
    x2 = random.randint(20, 60)
    y1 = random.randint(900, 1100)
    y2 = random.randint(1300, 1500)
    duration = random.randint(500, 1000)
    if up == 'up':
        script = 'input touchscreen swipe ' + str(x1) + ' ' + str(y1) + ' ' \
                 + str(x2) + ' ' + str(y2) + ' ' + str(duration)
    else:
        script = 'input touchscreen swipe ' + str(x2) + ' ' + str(y2) + ' '\
                 + str(x1) + ' ' + str(y1) + ' ' + str(duration)
    device.shell(script)
    random_sleep(1)


def current_screen():
    # take current screenshot
    # tic = time.process_time()
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
    result = cv2.imread('screen.png', cv2.IMREAD_COLOR)
    # this is actually slower: result = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    # tok = time.process_time()
    # print(str(toc - tic))
    return result


def crop_image(image, x_start, x_end, y_start, y_end, file_name='crop_result.png'):
    # result = crop_picture(result, 480, 550, 950, 1700)
    crop = crop_helper(image, x_start, x_end, y_start, y_end)
    # with open('crop_result.png', 'wb') as f:
    #     f.write(result)
    # resized = cv2.resize(result, (540, 800))
    result = Image.fromarray(crop)
    # cv2.imshow('crop', result)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # with open('crop_result.png', 'wb') as f:
    #     f.write(result)
    result.save(file_name)
    return crop


def crop_helper(img, start_x, end_x, start_y, end_y):
    return img[start_y:end_y, start_x:end_x]


# return miss or hit
def scroll_to_find_multiple(image, name, scroll_down, scroll_up, threshold=0.8):
    print_and_log('scroll to find multiple ' + name)
    scroll_counter = 0
    match = image_check(image, name, threshold)
    while match == 0:
        if scroll_counter > scroll_down:
            break
        scroll('down')
        scroll_counter += 1
        match = image_check(image, name, threshold)
    scroll_counter = 0
    while match == 0:
        if scroll_counter > scroll_up:
            print('Cannot find ' + name + ' by scrolling')
            return 'miss'
        scroll('up')
        scroll_counter += 1
        match = image_check(image, name, threshold)
    print(name + ' is found')
    return 'hit'


# return miss or hit
def scroll_to_find_unique(image, name, scroll_down, scroll_up, threshold=0.8):
    print_and_log('scroll to find unique ' + name)
    scroll_counter = 0
    match = image_check(image, name, threshold)
    while match != 1:
        if match > 1:
            print_and_log('multiple matches')
            sys.exit('multiple matches ' + name)
        if scroll_counter > scroll_down:
            break
        scroll('down')
        scroll_counter += 1
        match = image_check(image, name, threshold)
    scroll_counter = 0
    while match != 1:
        if match > 1:
            print_and_log('multiple matches')
            sys.exit('multiple matches ' + name)
        if scroll_counter > scroll_up:
            print_and_log('Cannot find ' + name + ' by scrolling')
            return 'miss'
        scroll('up')
        scroll_counter += 1
        match = image_check(image, name, threshold)
    print_and_log(name + ' is found')
    return 'hit'


def reward_claim():
    # reward_banner = cv2.imread('images/needles/reward_banner.png', cv2.IMREAD_COLOR)
    close_button = cv2.imread('images/needles/close.PNG', cv2.IMREAD_COLOR)
    while optional_click_patient(close_button, 'close_button', 3, 0.85) == 'hit':
        random_sleep_extra(2)


#
def stratum_image(name):
    return cv2.imread('images/needles/stratums/' + name + '_stratum.PNG', cv2.IMREAD_COLOR)


def tempest_trial_image(level):
    return cv2.imread('images/needles/event/tempest_trials/level' + str(level) + '.PNG', cv2.IMREAD_COLOR)


def button_click(button, name, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, button, threshold)
    if match != 1:
        print_log_and_exit(name + ' button not found')
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(max_loc[0] + random.randint(0, w)) + ' '
                 + str(max_loc[1] + random.randint(0, h)))


def button_click_patient(button, name, wait_time, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, button, threshold)
    counter = 0
    while match != 1:
        if counter > wait_time:
            print_log_and_exit(name + ' button not found')
        random_sleep(1)
        counter += 1
        screen = current_screen()
        match, max_loc = check_needle(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(max_loc[0] + random.randint(0, w)) + ' '
                 + str(max_loc[1] + random.randint(0, h)))


def button_click_patient_accelerate(button, name, wait_time, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, button, threshold)
    counter = 0
    while match != 1:
        if counter > wait_time:
            print_log_and_exit(name + ' button not found')
        random_sleep(0)
        counter += 1
        screen = current_screen()
        match, max_loc = check_needle(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(max_loc[0] + random.randint(0, w)) + ' '
                 + str(max_loc[1] + random.randint(0, h)))


def optional_click_patient(button, name, wait_time, threshold=0.85):
    print('check and click button ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, button, threshold)
    counter = 0
    while match != 1:
        if counter > wait_time:
            print_and_log(name + ' button did not appear')
            return 'miss'
        random_sleep(1)
        counter += 1
        screen = current_screen()
        match, max_loc = check_needle(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(max_loc[0] + random.randint(0, w)) + ' '
                 + str(max_loc[1] + random.randint(0, h)))
    return 'hit'


# click lowest match when there are multiple matches
def multiple_button_click_patient(button, name, wait_time, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, lowest_loc = check_needle_lowest_match(screen, button, threshold)
    counter = 0
    while match == 0:
        if counter > wait_time:
            print_log_and_exit(name + ' button not found')
        random_sleep(1)
        counter += 1
        screen = current_screen()
        match, lowest_loc = check_needle_lowest_match(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(lowest_loc[0] + random.randint(0, w)) + ' '
                 + str(lowest_loc[1] + random.randint(0, h)))


def highest_button_click_patient(button, name, wait_time, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, highest = check_needle_highest_match(screen, button, threshold)
    counter = 0
    while match == 0:
        if counter > wait_time:
            print_log_and_exit(name + ' button not found')
        random_sleep(1)
        counter += 1
        screen = current_screen()
        match, highest = check_needle_highest_match(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(highest[0] + random.randint(0, w)) + ' '
                 + str(highest[1] + random.randint(0, h)))


def image_check(image, name, threshold=0.8):
    print('checking image ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, image, threshold)
    return match


def image_check_partial(image, name, x_start, x_end, y_start, y_end, threshold=0.8):
    print('checking image ' + name)
    screen = current_screen()
    screen = crop_image(screen, x_start, x_end, y_start, y_end, 'crop_result_screen.png')
    match, max_loc = check_needle(screen, image, threshold)
    return match


def back_arrow_helper(counter):
    back_arrow = cv2.imread('images/needles/back_arrow.png', cv2.IMREAD_COLOR)
    for i in range(counter):
        button_click_patient_accelerate(back_arrow, 'back_arrow', 15, 0.8)
        random_sleep(2)


def auto_battle_helper():
    auto_battle = cv2.imread('images/needles/auto_battle.PNG', cv2.IMREAD_COLOR)
    button_click_patient(auto_battle, 'auto_battle', 10, 0.75)
    auto_text = cv2.imread('images/needles/auto_battle_text.png', cv2.IMREAD_COLOR)
    optional_click_patient(auto_text, 'auto_battle_text', 5, 0.8)


def battle_watch_helper(can_lose=0):
    stage_clear = cv2.imread('images/needles/stage_clear.png', cv2.IMREAD_COLOR)
    game_over = cv2.imread('images/needles/game_over.png', cv2.IMREAD_COLOR)
    give_up = cv2.imread('images/needles/give_up.png', cv2.IMREAD_COLOR)
    give_up_old = cv2.imread('images/needles/give_up_old.png', cv2.IMREAD_COLOR)
    end = cv2.imread('images/needles/end.png', cv2.IMREAD_COLOR)
    skip = cv2.imread('images/needles/skip.png', cv2.IMREAD_COLOR)
    you_win = cv2.imread('images/needles/you_win.png', cv2.IMREAD_COLOR)
    you_lose = cv2.imread('images/needles/you_lose.png', cv2.IMREAD_COLOR)
    close = cv2.imread('images/needles/close.png', cv2.IMREAD_COLOR)
    battle_timer = 0
    # keep checking if stage is cleared
    while image_check(stage_clear, 'stage_clear', 0.9) != 1:
        random_sleep(5)
        battle_timer += 1
        # if can lose, take surrender (summoner duels)
        if image_check(close, 'close') == 1:
            button_click(close, 'close', 0.8)
            random_sleep(1)
            return 'clear'
        # if can lose (summoner duels)
        if can_lose == 1 and image_check(you_lose, 'you_lose') > 0:
            multiple_button_click_patient(you_lose, 'you_lose', 5)
            random_sleep(2)
            return 'defeat'
        # or you win (summoner duels)
        if image_check(you_win, 'you_win') == 1:
            button_click(you_win, 'you_win', 0.9)
            random_sleep(2)
            return 'clear'
        # or end. then there won't be a scene to skip
        if image_check_partial(end, 'end', 0, 1080, 880, 1040, 0.83) > 0:
            button_click_patient_accelerate(end, 'end', 20)
            random_sleep(2)
            return 'clear'
        # or game over
        if image_check(game_over, 'game_over') == 1:
            button_click(game_over, 'game_over', 0.7)
            random_sleep(2)
            optional_click_patient(give_up, 'give_up', 5, 0.8)
            optional_click_patient(give_up_old, 'give_up_old', 5, 0.8)
            random_sleep(5 + random.randint(0, 3))
            return 'defeat'
        if battle_timer > 170:
            # about half an hour
            print_log_and_exit('Battle lasts too long/ stage clear image not found')
    button_click(stage_clear, 'stage_clear', 0.8)
    if optional_click_patient(skip, 'skip', 5) == 'hit':
        random_sleep(5)
    random_sleep(5)
    return 'clear'


def close_notification():
    notification = cv2.imread('images/needles/notification.PNG', cv2.IMREAD_COLOR)
    if image_check(notification, 'notification', 0.7) > 0:
        close_notification_icon = cv2.imread('images/needles/close_notification.PNG', cv2.IMREAD_COLOR)
        button_click(close_notification_icon, 'close_notification', 0.9)


def close_pop_ups():
    random_sleep(random.randint(2, 3))
    close_button = cv2.imread('images/needles/close.PNG', cv2.IMREAD_COLOR)
    remind_me_later = cv2.imread('images/needles/remind_me_later.png', cv2.IMREAD_COLOR)
    while image_check(close_button, 'close_button', 0.85) > 0 or \
            image_check(remind_me_later, 'remind_me_later', 0.85) > 0:
        if image_check(close_button, 'close_button', 0.85) > 0:
            button_click(close_button, 'close_button', 0.85)
        else:
            button_click(remind_me_later, 'remind_me_later', 0.85)
        random_sleep(random.randint(2, 3))


def print_log_and_exit(message):
    print(message)
    sys.exit(message)


def print_and_log(message):
    print(message)


# return exhausted/clear/defeat
def start_training(level):
    tower_banner = cv2.imread('images/needles/training_tower_banner.PNG', cv2.IMREAD_COLOR)
    match = image_check(tower_banner, 'tower_banner', 0.7)
    if match != 1:
        print('Tower banner mismatch')
        return 1
    stratums = ['starting', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
                'seventh', 'eighth', 'ninth', 'tenth']
    # screen = current_screen()
    stratum = stratum_image(stratums[level])
    scroll_to_find_unique(stratum, 'stratum ' + str(level), 5, 7, 0.85)
    # exception will be thrown by button_click_patient if stratum is not found
    button_click_patient(stratum, 'stratum ' + str(level), 3, 0.85)
    random_sleep(random.randint(1, 2))
    # match, max_loc = check_needle(screen, stratum, 0.85)
    # scroll_counter = 0
    # while match != 1:
    #     if match > 1:
    #         print_log_and_exit('Stratum needle gets multiple matches')
    #     if scroll_counter > 5:
    #         break
    #     scroll('down')
    #     screen = current_screen()
    #     scroll_counter += 1
    #     match, max_loc = check_needle(screen, stratum, 0.85)
    # # try scroll the other way
    # scroll_counter = 0
    # while match != 1:
    #     if match > 1:
    #         print_log_and_exit('Stratum needle gets multiple matches')
    #     if scroll_counter > 7:
    #         print_log_and_exit('Cannot find stratum by scrolling')
    #     scroll('up')
    #     screen = current_screen()
    #     scroll_counter += 1
    #     match, max_loc = check_needle(screen, stratum, 0.85)
    # print('Stratum is found')
    # h = stratum.shape[0]
    # w = stratum.shape[1]
    # random_sleep(1)
    # device.shell('input touchscreen tap ' + str(max_loc[0] + w) + ' ' + str(max_loc[1] + h))
    # random_sleep(random.randint(1, 2))
    # check if stamina not enough (stamina screen)
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    fight_button = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    button_click(fight_button, 'fight')
    random_sleep(random.randint(10, 14))
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    auto_battle_helper()
    result = battle_watch_helper()
    return result


def training_grinder(level):
    tower_banner = cv2.imread('images/needles/training_tower_banner.PNG', cv2.IMREAD_COLOR)
    match = image_check(tower_banner, 'tower_banner', 0.7)
    # navigate to training tower if not already there
    if match != 1:
        battle_button = cv2.imread('images/needles/battle.PNG', cv2.IMREAD_COLOR)
        button_click_patient(battle_button, 'battle_button', 5)
        training_tower_icon = cv2.imread('images/needles/training_tower.PNG', cv2.IMREAD_COLOR)
        button_click_patient(training_tower_icon, 'training tower icon', 5)
    random_sleep(1)
    max_level = 10
    min_level = 0
    clear_counter = 0
    defeat_counter = 0
    current_level = level
    status = 'started'
    # first, keep challenging until first defeat
    while status != 'exhausted':
        status = start_training(current_level)
        if status == 'exhausted' or status == 'defeat':
            current_level -= 1
            break
        reward_claim()
        if current_level != max_level:
            current_level += 1
        print('challenge level ' + str(current_level))
    # after first defeat: settle for 4-6 clears before challenging, or settle at lower level upon 2 consecutive defeats
    auto_mode = 'settle'
    while status != 'exhausted':
        print(auto_mode + ' training level ' + str(current_level))
        status = start_training(current_level)
        if status == 'exhausted':
            break
        reward_claim()
        # in challenge mode, settle in new level if clear, settle in lower level if defeat
        if auto_mode == 'challenge':
            if status == 'defeat':
                current_level -= 1
            auto_mode = 'settle'
            continue
        if status == 'clear':
            clear_counter += 1
            defeat_counter = 0
        elif status == 'defeat':
            defeat_counter += 1
        if clear_counter >= random.randint(4, 6):
            auto_mode = 'challenge'
            clear_counter = 0
            defeat_counter = 0
            if current_level != max_level:
                current_level += 1
        elif defeat_counter > 1:
            clear_counter = 0
            defeat_counter = 0
            if current_level != min_level:
                current_level -= 1
    print('stamina depleted during training')
    return current_level


# return section cleared/exhausted/defeat/clear
# click on a story/event that's not cleared.
def start_clearable(clearable_type):
    # if clearable_type == 'story':
    #     main_story = cv2.imread('images/needles/main_story.png', cv2.IMREAD_COLOR)
    #     match = image_check(main_story, 'main story', 0.8)
    #     if match != 1:
    #         print_log_and_exit('main story banner mismatch')
    not_cleared = cv2.imread('images/needles/not_cleared.PNG', cv2.IMREAD_COLOR)
    scroll_to_find_multiple(not_cleared, 'Not Cleared', 5, 7, 0.7)  # should be 0.8
    scroll_counter = 0
    match = image_check(not_cleared, 'story not cleared', 0.7)
    while match == 0:
        if scroll_counter > 3:
            break
        scroll('down')
        scroll_counter += 1
        match = image_check(not_cleared, 'story not cleared')
    # try scroll the other way
    scroll_counter = 0
    while match == 0:
        if scroll_counter > 5:
            back_arrow_helper(1)
            scroll('up')
            print('Cannot find story not cleared by scrolling')
            return 'section cleared'
        scroll('up')
        scroll_counter += 1
        match = image_check(not_cleared, 'story not cleared')
    print('New story is found')
    # highest_button_click_patient(not_cleared, 'not cleared story', 3, 0.7)
    multiple_button_click_patient(not_cleared, 'not cleared story', 3, 0.7)
    random_sleep(random.randint(1, 2))
    # click on fight button if available, otherwise find clearable then click fight button
    fight_button = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    if optional_click_patient(fight_button, 'fight button optional', 3) == 'miss':
        if scroll_to_find_multiple(not_cleared, 'not cleared story maybe', 1, 3) == "hit":
            multiple_button_click_patient(not_cleared, 'not cleared story maybe', 3)
        random_sleep(random.randint(1, 2))
        button_click(fight_button, 'fight')
    random_sleep(random.randint(10, 14))
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    skip = cv2.imread('images/needles/skip.png', cv2.IMREAD_COLOR)
    auto_battle = cv2.imread('images/needles/auto_battle.PNG', cv2.IMREAD_COLOR)
    skip_green = cv2.imread('images/needles/skip_cinematic_green.png', cv2.IMREAD_COLOR)
    # there might be cinematic screen
    if image_check(auto_battle, 'auto_battle', 0.75) != 1 and image_check(skip, 'skip') != 1:
        device.shell('input touchscreen tap ' + str(random.randint(483, 595)) + ' ' +
                     str(random.randint(928, 963)))
        button_click_patient(skip_green, 'cinematic skip', 5)
        random_sleep(random.randint(4, 7))
    if image_check(skip, 'skip') == 1:
        button_click(skip, 'skip', 0.75)
        random_sleep(5)
    random_sleep(5)
    auto_battle_helper()
    battle_watch_helper()
    random_sleep(20)
    # might need to skip after ending
    if image_check(skip, 'skip') == 1:
        button_click(skip, 'skip', 0.75)
    random_sleep(10)
    return 'clear'


def clearable_section_grinder(clearable_type):
    defeat_counter = 0
    status = 'started'
    while defeat_counter < 2:
        status = start_clearable(clearable_type)
        if status == 'exhausted' or status == 'section cleared':
            print_and_log(clearable_type + ' ' + status + ', loop ended')
            return status
        if status == 'defeat':
            defeat_counter += 1
        if clearable_type == 'rival_domains':
            ok_button = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
            optional_click_patient(ok_button, 'ok button', 20)
            random_sleep(1)
        random_sleep(2)
        reward_claim()
        scroll('up')
        # scroll('up')
    print_and_log('defeated twice in ' + clearable_type)
    return 'defeat'


def clearable_book_grinder():
    status = clearable_section_grinder('story')
    while status == 'section cleared':
        status = clearable_section_grinder('story')
    print_and_log(status + ' end of book grinder')


# auto start, end and auto start
def consecutive_battle_single():
    auto_battle = cv2.imread('images/needles/auto_battle.PNG', cv2.IMREAD_COLOR)
    if image_check(auto_battle, 'auto_battle', 0.75) == 0:
        return 'complete'
    button_click(auto_battle, 'auto_battle', 0.75)
    random_sleep(2)
    auto_text = cv2.imread('images/needles/auto_battle_text.png', cv2.IMREAD_COLOR)
    button_click(auto_text, 'auto_battle_text', 0.8)
    stage_clear = cv2.imread('images/needles/stage_clear.png', cv2.IMREAD_COLOR)
    you_lose = cv2.imread('images/needles/you_lose.png', cv2.IMREAD_COLOR)
    fight_button = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    game_over = cv2.imread('images/needles/game_over.png', cv2.IMREAD_COLOR)
    give_up = cv2.imread('images/needles/give_up.png', cv2.IMREAD_COLOR)
    battle_timer = 0
    while image_check(stage_clear, 'stage_clear', 0.9) != 1:
        battle_timer += 1
        # or lose once (handle this to update team, before we handle the final game over case)
        if image_check(you_lose, 'you_lose', 0.9) > 0:
            multiple_button_click_patient(you_lose, 'you_lose', 15)
            random_sleep(3)
            button_click_patient(fight_button, 'fight button', 3)
            random_sleep(5)
            highest_button_click_patient(fight_button, 'fight button', 3)
            return 'lose'
        if image_check(game_over, 'game_over') == 1:
            button_click(game_over, 'game_over', 0.7)
            random_sleep(9 + random.randint(0, 1))
            # button_click_patient(give_up, 'give_up', 3, 0.8)
            # random_sleep(5 + random.randint(0, 3))
            return 'defeat'
        if battle_timer > 170:
            # about half an hour
            print_log_and_exit('Battle lasts too long/ stage clear image not found')
    button_click(stage_clear, 'stage_clear', 0.8)
    return 'pass'


def consecutive_battle_loop():
    status = 'start'
    while status != 'defeat' and status != 'complete':
        status = consecutive_battle_single()
        reward_claim()
        random_sleep(10)
    print_and_log(status)
    return status


def tempest_trial_enter(level):
    banner = cv2.imread('images/needles/event/tempest_trials/tempest_trials_banner.png')
    if image_check(banner, 'tempest_trials_banner') != 1:
        # get into tempest trails
        return 'Not in tempest trials, needs navigation'
    random_sleep(3)
    tempest_level = tempest_trial_image(level)
    match = image_check(tempest_level, 'tempest_level ' + str(level), 0.9)
    scroll_counter = 0
    while match != 1:
        if match > 1:
            print_log_and_exit('Tempest trial level gets multiple matches')
        if scroll_counter > 3:
            break
        scroll('down')
        scroll_counter += 1
        random_sleep(1)
        match = image_check(tempest_level, 'tempest_level ' + str(level), 0.9)
    # try scroll the other way
    scroll_counter = 0
    while match != 1:
        if match > 1:
            print_log_and_exit('Tempest trial level gets multiple matches')
        if scroll_counter > 4:
            print_log_and_exit('Cannot find tempest trial level by scrolling')
        scroll('up')
        scroll_counter += 1
        random_sleep(1)
        match = image_check(tempest_level, 'tempest_level ' + str(level), 0.9)
    button_click_patient(tempest_level, 'tempest level', 3, 0.9)
    fight_button = cv2.imread('images/needles/fight.PNG')
    button_click_patient(fight_button, 'fight button', 3)
    random_sleep(random.randint(10, 14))
    # check if stamina not enough (stamina screen)
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    status = consecutive_battle_loop()
    reward_claim()
    ok_button = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    button_click_patient(ok_button, 'ok_button', 20)
    random_sleep(5)
    reward_claim()
    return status


def tempest_trial_grinder(level, rounds):
    # handle navigation later
    # select_stage = cv2.imread('images/needles/select_stage.png')
    # button_click_patient(select_stage, 'select_stage', 3)
    status = 'pass'
    counter = 0
    while status != 'exhausted' and counter < rounds:
        status = tempest_trial_enter(level)
        print_and_log(status)
        if status == 'defeat':
            level -= 5
        random_sleep(10)
    return status


def tap_loop():
    while True:
        device.shell('input touchscreen tap 536 1748')


def aether_raids_battle_single():
    battle_big = cv2.imread('images/needles/battle_button_big.png', cv2.IMREAD_COLOR)
    battle_small = cv2.imread('images/needles/battle_button_small.png', cv2.IMREAD_COLOR)
    proceed = cv2.imread('images/needles/proceed.png', cv2.IMREAD_COLOR)
    beginner = cv2.imread('images/needles/coliseum/arena/beginner.png', cv2.IMREAD_COLOR)
    # send_friend_request = cv2.imread('images/needles/send.png', cv2.IMREAD_COLOR)
    send_friend_request = cv2.imread('images/needles/dont_send.png', cv2.IMREAD_COLOR)
    ok = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    aether_fight = cv2.imread('images/needles/fight_aether_big.png', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.png', cv2.IMREAD_COLOR)
    # automation starts
    button_click_patient(battle_big, 'big battle button', 5)
    if optional_click_patient(stamina_back, 'stamina_back', 5) == 'hit':
        print_and_log('exhausted during training')
        return 'exhausted'
    button_click_patient(proceed, 'proceed', 5)
    random_sleep(1)
    optional_click_patient(proceed, 'proceed', 5)
    random_sleep(2)
    button_click_patient(aether_fight, 'aether fight button', 5)
    random_sleep(1)
    button_click_patient(fight, 'fight button', 5)
    random_sleep(8)
    auto_battle_helper()
    battle_watch_helper()
    optional_click_patient(send_friend_request, 'send friend request', 5)
    random_sleep(4)
    button_click_patient(ok, 'ok', 5)
    random_sleep(1)
    reward_claim()
    return 'pass'


def grand_conquest_single():
    ok = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    auto_battle_helper()
    battle_watch_helper()
    random_sleep(1)
    button_click_patient(ok, 'ok', 5)
    random_sleep(1)
    reward_claim()


def arena_battle_single():
    battle_big = cv2.imread('images/needles/battle_button_big.png', cv2.IMREAD_COLOR)
    battle_small = cv2.imread('images/needles/battle_button_small.png', cv2.IMREAD_COLOR)
    proceed = cv2.imread('images/needles/proceed.png', cv2.IMREAD_COLOR)
    beginner = cv2.imread('images/needles/coliseum/arena/beginner.png', cv2.IMREAD_COLOR)
    # restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    # send_friend_request = cv2.imread('images/needles/send.png', cv2.IMREAD_COLOR)
    send_friend_request = cv2.imread('images/needles/dont_send.png', cv2.IMREAD_COLOR)
    ok = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    button_click_patient(battle_big, 'big battle button', 5)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    if optional_click_patient(stamina_back, 'stamina_back', 5) == 'hit':
        # button_click(restore, 'stamina restore button')
        print_and_log('exhausted during arena')
        return 'exhausted'
    button_click_patient(proceed, 'proceed', 5)
    random_sleep_extra(5)
    button_click_patient(beginner, 'beginner', 5)
    button_click_patient(battle_small, 'battle_small', 5)
    random_sleep(5)
    auto_battle_helper()
    battle_watch_helper()
    optional_click_patient(send_friend_request, 'send friend request', 5)
    random_sleep(3)
    button_click_patient(ok, 'ok', 5)
    random_sleep(1)
    reward_claim()
    return 'pass'


# start from battle or battle icon available. return to coliseum's home screen
def arena_grinder():
    coliseum = cv2.imread('images/needles/coliseum/coliseum.png', cv2.IMREAD_COLOR)
    battle = cv2.imread('images/needles/battle.PNG', cv2.IMREAD_COLOR)
    arena_button = cv2.imread('images/needles/coliseum/arena_button.png', cv2.IMREAD_COLOR)
    if image_check(coliseum, 'coliseum') != 1:
        button_click_patient(battle, 'battle', 3)
        random_sleep(1)
    button_click_patient(coliseum, 'coliseum', 3)
    random_sleep(random.randint(2, 3))
    if scroll_to_find_unique(arena_button, 'arena_button', 1, 2, 0.9) != 'hit':
        return 'not found'
    button_click_patient(arena_button, 'arena button', 3)
    random_sleep_extra(7)
    reward_claim()
    status = 'pass'
    while status == 'pass':
        status = arena_battle_single()
        random_sleep_extra(5)
    back_arrow_helper(1)
    random_sleep(2)
    back_arrow_helper(1)
    return status


def aether_keep_grinder(rounds=2):
    aether_keeps = cv2.imread('images/needles/aether_raids/aether_keeps.png', cv2.IMREAD_COLOR)
    battle = cv2.imread('images/needles/battle.PNG', cv2.IMREAD_COLOR)
    arena_button = cv2.imread('images/needles/coliseum/arena_button.png', cv2.IMREAD_COLOR)
    if image_check(aether_keeps, 'aether_keeps') != 1:
        button_click_patient(battle, 'battle', 3)
        random_sleep(1)
    button_click_patient_accelerate(aether_keeps, 'aether_keeps', 10)
    random_sleep(random.randint(2, 3))
    reward_claim()
    status = 'pass'
    counter = 0
    while status == 'pass' and counter < rounds:
        status = aether_raids_battle_single()
        counter += 1
        random_sleep_extra(5)
    back_arrow_helper(1)
    return status


def tap_battle_single():
    not_cleared = cv2.imread('images/needles/not_cleared.PNG', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    stage_clear = cv2.imread('images/needles/stage_clear.png', cv2.IMREAD_COLOR)
    skip = cv2.imread('images/needles/skip.png', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    if scroll_to_find_multiple(not_cleared, 'not_cleared', 1, 7) == 'miss':
        return 'complete'
    button_click_patient_accelerate(not_cleared, 'not_cleared', 10)
    random_sleep(1)
    button_click_patient_accelerate(fight, 'fight', 10)
    random_sleep(5)
    tik = time.perf_counter()
    while not keyboard.is_pressed('q'):
        if pyautogui.pixel(265, 1440)[0] > 250 or pyautogui.pixel(265, 1195)[0] > 250 \
                or pyautogui.pixel(265, 946)[0] > 250 or pyautogui.pixel(265, 695)[0] > 250:
            mouse_click(random.randint(302, 773), random.randint(1823, 1950))
            tik = time.perf_counter()
            time.sleep(0.2)
        tok = time.perf_counter()
        if tok - tik > 7:
            if optional_click_patient(skip, 'skip', 5) == 'hit':
                tik = time.perf_counter()
                continue
            button_click_patient_accelerate(stage_clear, 'stage_clear', 15)
            break
        # if pyautogui.pixel(1060, 1036)[0] > 220 and pyautogui.pixel(1060, 1036)[1] > 250 \
        #         and pyautogui.pixel(1060, 1036)[2] > 250:
        #     break
    random_sleep(5)
    reward_claim()
    random_sleep(5)
    ok_button = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    optional_click_patient(ok_button, 'ok button', 20)
    close_button = cv2.imread('images/needles/close.PNG', cv2.IMREAD_COLOR)
    optional_click_patient(close_button, 'close button', 20)
    return 'pass'


def tap_battle_grinder():
    status = 'pass'
    while status != 'complete':
        status = tap_battle_single()
        random_sleep(5)


def daily_routine():
    aether_keep_grinder(2)
    random_sleep(3)
    arena_grinder()
    # home = cv2.imread('images/needles/home.png', cv2.IMREAD_COLOR)
    # reward_claim()


# currently, only intermediate level available
def heroes_journey_single():
    select_stage = cv2.imread('images/needles/select_stage.png', cv2.IMREAD_COLOR)
    level = cv2.imread('images/needles/event/heroes_journey/intermediate.png', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    # button_click_patient(select_stage, 'select_stage', 3)
    button_click_patient(level, 'level', 3)
    button_click_patient(fight, 'fight', 3)
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    random_sleep(5)
    auto_battle_helper()
    battle_watch_helper()
    random_sleep(5)
    reward_claim()
    return 'pass'


def heroes_journey_grinder(rounds=20):
    status = 'pass'
    counter = 0
    while status == 'pass' and counter < rounds:
        status = heroes_journey_single()
        counter += 1
        random_sleep(3)
    return status


def forging_bonds_single():
    select_stage = cv2.imread('images/needles/select_stage.png', cv2.IMREAD_COLOR)
    level = cv2.imread('images/needles/event/forging_bonds/advanced.png', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_COLOR)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_COLOR)
    skip = cv2.imread('images/needles/skip.png', cv2.IMREAD_COLOR)
    yes = cv2.imread('images/needles/yes.png', cv2.IMREAD_COLOR)
    # button_click_patient(select_stage, 'select_stage', 3)
    button_click_patient(level, 'level', 3)
    button_click_patient(fight, 'fight', 3)
    random_sleep(2)
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    optional_click_patient(yes, 'yes', 2)
    random_sleep(5)
    auto_battle_helper()
    battle_watch_helper()
    random_sleep(5)
    reward_claim()
    optional_click_patient(skip, 'skip', 3)
    optional_click_patient(skip, 'skip', 2)
    optional_click_patient(skip, 'skip', 2)
    optional_click_patient(skip, 'skip', 2)
    random_sleep(3)
    reward_claim()
    return 'pass'


def forging_bonds_grinder(rounds=20):
    status = 'pass'
    counter = 0
    while status == 'pass' and counter < rounds:
        status = forging_bonds_single()
        counter += 1
        random_sleep(3)
    return status


def summoner_duel_single():
    favor_battles = cv2.imread('images/needles/coliseum/summoner_duel/favor_battle.png', cv2.IMREAD_COLOR)
    # favor_battles = cv2.imread('images/needles/battle_button_big.png', cv2.IMREAD_COLOR)
    battle_button = cv2.imread('images/needles/battle_button_small.png', cv2.IMREAD_COLOR)
    fight = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    friend_request = cv2.imread('images/needles/dont_send.png', cv2.IMREAD_COLOR)
    ok = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
    close = cv2.imread('images/needles/close.png', cv2.IMREAD_COLOR)
    button_click_patient(favor_battles, 'favor_battles', 4)
    random_sleep(1)
    button_click_patient(battle_button, 'battle_button', 4)
    random_sleep(7)
    while image_check(fight, 'fight', 0.8) != 1:
        if image_check(close, 'close') == 1:
            button_click(close, 'close', 0.8)
            return 'no_opponent'
        random_sleep(1)
    random_sleep(7)
    button_click_patient(fight, 'fight', 10)
    random_sleep_extra(7)
    if image_check(close, 'close') == 1:
        button_click(close, 'close', 0.8)
        random_sleep(1)
    else:
        auto_battle_helper()
    battle_watch_helper(1)
    random_sleep(1)
    optional_click_patient(friend_request, 'friend_request', 5)
    random_sleep(1)
    button_click_patient(ok, 'ok', 6)
    reward_claim()


def summoner_duels_grinder(rounds=20):
    counter = 0
    while counter < rounds:
        summoner_duel_single()
        counter += 1
        random_sleep_extra(6)
    return 0

def single_arena_assault():
    battle_small = cv2.imread('images/needles/battle_button_small.png', cv2.IMREAD_COLOR)
    beginner = cv2.imread('images/needles/coliseum/arena/beginner.png', cv2.IMREAD_COLOR)
    button_click_patient(beginner, 'beginner', 5)
    button_click_patient(battle_small, 'battle_small', 5)
    random_sleep(5)
    fight_button = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_COLOR)
    button_click(fight_button, 'fight')
    random_sleep(5)
    highest_button_click_patient(fight_button, 'fight button', 3)
    auto_battle_helper()
    battle_watch_helper()
    reward_claim()



# Automation starts here (main)
# Connect to device, adb host and port number is static
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
# for item in devices:
#     print(item.shell('getprop'))
device = devices[0]
# summoner_duels_grinder(950)
# back_arrow_helper(2)

# clearable_section_grinder('rival_domains')
# clearable_section_grinder('story')
# clearable_book_grinder()
# forging_bonds_grinder(10)
# back_arrow_helper(2)
# daily_routine()
# arena_grinder()

# tap_battle_grinder()
#
while True:
    # single_arena_assault()
    tempest_trial_grinder(35, 9)
#     forging_bonds_grinder(20)
#     clearable_book_grinder()
#     training_grinder(1)
#     heroes_journey_grinder(9)
    random_sleep(3600 * 4)
# heroes_journey_grinder()
# select_stage = cv2.imread('images/needles/select_stage.png', cv2.IMREAD_COLOR)
# button_click_patient(select_stage, 'select_stage', 4)
# aether_keep_grinder(4)
# tempest_trial_grinder(30, 2)
# daily_routine()
# grand_conquest_single()
# arena_grinder()
# start_level = 10
# while True:
#     start_level = training_grinder(start_level)
#     print('next training starts with ' + str(start_level))
#     random_sleep(3600*5)
# test = cv2.imread('images/needles/ok.png', cv2.IMREAD_COLOR)
# image_check(test, 'test')

#global_debug = True
# screen = cv2.imread('Screenshot (19).png', cv2.IMREAD_COLOR)
# plt.imshow(screen, interpolation='nearest')
# plt.show()
# cv2.waitKey()
#print(screen[265, 1440])
#print(screen[265, 1195])
#print(screen[265, 695])
#
# screen = current_screen()
# crop_image(screen, 356, 370, 920, 1000)
# crop_image(screen, 353, 463, 920, 1000)
#
# test = cv2.imread('crop_result.png', cv2.IMREAD_COLOR)
# button_click_patient(test, 'test', 10)
# multiple_button_click_patient(test, 'test', 1)



