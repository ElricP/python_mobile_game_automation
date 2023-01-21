import random
import cv2
import numpy as np
from ppadb.client import Client
import time
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
global_needle_path = 'images/needles/'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def random_sleep(secs):
    time.sleep(secs + random.random())


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
    # cv2.rectangle(template, max_loc, (max_loc[0]+w, max_loc[1] + h), (0, 255, 255), 2)
    # resized = cv2.resize(template, (540, 800))
    # cv2.imshow('Check', resized)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return len(rectangles), max_loc


# scroll takes argument 'up' or 'down'
def scroll(up):
    x1 = random.randint(20, 60)
    x2 = random.randint(20, 60)
    y1 = random.randint(500, 700)
    y2 = random.randint(1000, 1300)
    duration = random.randint(100, 600)
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
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
    result = cv2.imread('screen.png', cv2.IMREAD_UNCHANGED)
    return result


# return exhausted/clear/defeat
def start_training(level):
    tower_banner = cv2.imread('images/needles/training_tower_banner.PNG', cv2.IMREAD_UNCHANGED)
    match = image_check(tower_banner, 'tower_banner', 0.7)
    if match != 1:
        print('Tower banner mismatch')
        return 1
    stratums = ['starting', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
                'seventh', 'eighth', 'ninth', 'tenth']
    screen = current_screen()
    stratum = stratum_image(stratums[level])
    match, max_loc = check_needle(screen, stratum, 0.85)
    scroll_counter = 0
    while match != 1:
        if match > 1:
            print('Stratum needle gets multiple matches')
            sys.exit('Stratum needle gets multiple matches')
        if scroll_counter > 5:
            break
        scroll('down')
        screen = current_screen()
        scroll_counter += 1
        match, max_loc = check_needle(screen, stratum, 0.85)
    # try scroll the other way
    while match != 1:
        if match > 1:
            print('Stratum needle gets multiple matches')
            sys.exit('Stratum needle gets multiple matches')
        if scroll_counter > 5:
            print('Cannot find stratum by scrolling')
            sys.exit('Cannot find stratum by scrolling')
        scroll('up')
        screen = current_screen()
        scroll_counter += 1
        match, max_loc = check_needle(screen, stratum, 0.85)
    print('Stratum is found')
    h = stratum.shape[0]
    w = stratum.shape[1]
    random_sleep(1)
    device.shell('input touchscreen tap ' + str(max_loc[0] + w) + ' ' + str(max_loc[1] + h))
    random_sleep(random.randint(1, 2))
    # check if stamina not enough (stamina screen)
    stamina_restore = cv2.imread('images/needles/stamina_restore.png', cv2.IMREAD_UNCHANGED)
    stamina_back = cv2.imread('images/needles/back.PNG', cv2.IMREAD_UNCHANGED)
    fight_button = cv2.imread('images/needles/fight.PNG', cv2.IMREAD_UNCHANGED)
    button_click(fight_button, 'fight')
    random_sleep(random.randint(10, 14))
    if image_check(stamina_restore, 'stamina_restore') == 1:
        button_click(stamina_back, 'stamina_back')
        print('exhausted during training')
        return 'exhausted'
    auto_battle = cv2.imread('images/needles/auto_battle.PNG', cv2.IMREAD_UNCHANGED)
    button_click(auto_battle, 'auto_battle', 0.75)
    random_sleep(2)
    auto_text = cv2.imread('images/needles/auto_battle_text.png', cv2.IMREAD_UNCHANGED)
    button_click(auto_text, 'auto_battle_text', 0.8)
    stage_clear = cv2.imread('images/needles/stage_clear.png', cv2.IMREAD_UNCHANGED)
    game_over = cv2.imread('images/needles/game_over.png', cv2.IMREAD_UNCHANGED)
    give_up = cv2.imread('images/needles/give_up.png', cv2.IMREAD_UNCHANGED)
    battle_timer = 0
    # keep checking if stage is cleared
    while image_check(stage_clear, 'stage_clear', 0.9) != 1:
        random_sleep(10)
        battle_timer += 1
        # or game over
        if image_check(game_over, 'game_over') == 1:
            button_click(game_over, 'game_over', 0.7)
            random_sleep(9 + random.randint(0, 1))
            button_click_patient(give_up, 'give_up', 3, 0.8)
            random_sleep(5 + random.randint(0, 3))
            return 'defeat'
        if battle_timer > 170:
            # about half an hour
            print('Battle lasts too long/ stage clear image not found')
            sys.exit('Battle lasts too long')
    button_click(stage_clear, 'stage_clear', 0.8)
    random_sleep(10)
    return 'clear'


def reward_claim():
    reward_banner = cv2.imread('images/needles/reward_banner.png', cv2.IMREAD_UNCHANGED)
    close_button = cv2.imread('images/needles/close.PNG', cv2.IMREAD_UNCHANGED)
    while image_check(reward_banner, 'reward_banner') > 0:
        button_click(close_button, 'close_button', 0.85)
        random_sleep(2)


def training_loop(level):
    tower_banner = cv2.imread('images/needles/training_tower_banner.PNG', cv2.IMREAD_UNCHANGED)
    match = image_check(tower_banner, 'tower_banner', 0.7)
    if match != 1:
        battle_button = cv2.imread('images/needles/battle.PNG', cv2.IMREAD_UNCHANGED)
        button_click_patient(battle_button, 'battle_button', 5)
        training_tower_icon = cv2.imread('images/needles/training_tower.PNG', cv2.IMREAD_UNCHANGED)
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


#
def stratum_image(name):
    return cv2.imread('images/needles/stratums/' + name + '_stratum.PNG', cv2.IMREAD_UNCHANGED)


def button_click(button, name, threshold=0.85):
    print('clicking button ' + name)
    screen = current_screen()
    match, max_loc = check_needle(screen, button, threshold)
    if match != 1:
        print(name + ' button not found')
        sys.exit(name + ' button not found')
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
            print(name + ' button not found')
            sys.exit(name + ' button not found')
        random_sleep(1)
        counter += 1
        screen = current_screen()
        match, max_loc = check_needle(screen, button, threshold)
    h = button.shape[0]
    w = button.shape[1]
    device.shell('input touchscreen tap ' + str(max_loc[0] + random.randint(0, w)) + ' '
                 + str(max_loc[1] + random.randint(0, h)))


def image_check(image, name, threshold=0.8):
    print('checking image ' + name)
    screen = current_screen()
    print('screenshot acquired')
    match, max_loc = check_needle(screen, image, threshold)
    return match


def close_notification():
    notification = cv2.imread('images/needles/notification.PNG', cv2.IMREAD_UNCHANGED)
    if image_check(notification, 'notification', 0.7) > 0:
        close_notification_icon = cv2.imread('images/needles/close_notification.PNG', cv2.IMREAD_UNCHANGED)
        button_click(close_notification_icon, 'close_notification', 0.9)


def close_pop_ups():
    random_sleep(random.randint(2, 3))
    close_button = cv2.imread('images/needles/close.PNG', cv2.IMREAD_UNCHANGED)
    remind_me_later = cv2.imread('images/needles/remind_me_later.png', cv2.IMREAD_UNCHANGED)
    while image_check(close_button, 'close_button', 0.85) > 0 or \
            image_check(remind_me_later, 'remind_me_later', 0.85) > 0:
        if image_check(close_button, 'close_button', 0.85) > 0:
            button_click(close_button, 'close_button', 0.85)
        else:
            button_click(remind_me_later, 'remind_me_later', 0.85)
        random_sleep(random.randint(2, 3))


# Automation starts here (main)
# Connect to device, adb host and port number is static)
# sleep_time = random.randint(0, 7200)
# random_sleep(sleep_time)
# print('sleep for ' + str(sleep_time))
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]
# first, close everything (home, arena, some events
close_pop_ups()
close_notification()
training_loop(1)


#test = cv2.imread('images/needles/event_not_completed.PNG', cv2.IMREAD_UNCHANGED)
# image_check(test, 'test')
#button_click_patient(test, 'test', 10)
#training_loop(6)
# if there is a notification


# if image_check(game_over, 'game_over') == 1:
#     button_click(game_over, 'game_over', 0.7)
#     random_sleep(2)

# current_screen = current_screen()
#start_training(4)


# battle_button_result = cv2.matchTemplate(current_screen, battle_button, cv2.TM_CCOEFF_NORMED)
# (_, max_val, _, max_loc) = cv2.minMaxLoc(battle_button_result)
# print(max_val)
# print(max_loc)
# width = battle_button.shape[1]
# height = battle_button.shape[0]
# # (0, 255, 255) is color yellow, 2 is border thickness
# cv2.rectangle(current_screen, max_loc, (max_loc[0]+width, max_loc[1] + height), (0, 255, 255), 2)
# resized = cv2.resize(current_screen, (540, 800))
# cv2.imshow('Screen', resized)
# cv2.waitKey()
# cv2.destroyAllWindows()
#print(device.shell('wm size'))
#device.shell('input touchscreen tap 1000 500')
#device.shell('input touchscreen swipe 500 500 500 1000 2000')
# swipe from coordinate - to coordinate - duration
