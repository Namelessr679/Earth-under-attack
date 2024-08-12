"""
Name: Robel Solomon Gizaw and Naod Asfaw
CSC 201
Project 3 (checkpoint)

Use the witch to catch spiders. Move the witch using the left and right arrow keys.
If the witch catches enough spiders before they escape, you win.

Document Assistance:
Azaria (current sophmore) explained to us how to exit a program after a function occurred


"""

import sys
from graphics2 import *
import time
import random
import math
from button import Button

ASTEROID_SPEED = 5
TANK_SPEED = 25
NUM_LOSE = -15
NUM_WIN = 20
STALL_TIME = 0.05
THRESHOLD = 50
ROCKET_SPEED = -10


def distance_between_points(point1, point2):
    """
    Calculate the distance between two points.

    Args:
        point1 (Point): First point.
        point2 (Point): Second point.

    Returns:
        float: Distance between the two points.
    """
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x) ** 2 + (p1y - p2y) ** 2)


def is_close_enough(rocket_img, asteroid_img):
    """
    Check if the rocket is close enough to the asteroid.

    Args:
        rocket_img (Image): Rocket image.
        asteroid_img (Image): Asteroid image.

    Returns:
        bool: True if close enough, False otherwise.
    """
    center_rocket = rocket_img.getCenter()
    center_asteroid = asteroid_img.getCenter()
    distance = distance_between_points(center_rocket, center_asteroid)

    return distance < THRESHOLD


def move_asteroid(asteroid_img_list):
    """
    Move asteroids downwards.

    Args:
        asteroid_img_list (list): List of asteroid images.
    """
    for asteroid in asteroid_img_list:
        asteroid.move(0, ASTEROID_SPEED)


def move_rocket(rocket_img_list):
    """
    Move rockets upwards.

    Args:
        rocket_img_list (list): List of rocket images.
    """
    for rocket in rocket_img_list:
        rocket.move(0, ROCKET_SPEED)


def is_object_out(object, limit):
    """
    Check if the object is out of bounds.

    Args:
        object (Image): Object image.
        limit (int): Y-coordinate limit.

    Returns:
        bool: True if the object is out of bounds, False otherwise.
    """
    object_center = object.getCenter()
    return object_center.getY() >= limit


def move_tank(window, tank_img):
    """
    Move the tank based on user input.

    Args:
        window (GraphWin): Graphics window.
        tank_img (Image): Tank image.
    """
    click_point = window.checkMouse()
    if click_point:
        tank_center = tank_img.getCenter()
        if click_point.getY() > tank_center.getY() - tank_img.getHeight() // 2:
            if click_point.getX() < tank_center.getX() - tank_img.getWidth() // 2:
                tank_img.move(-TANK_SPEED, 0)
            elif click_point.getX() > tank_center.getX() + tank_img.getWidth() // 2:
                tank_img.move(TANK_SPEED, 0)


def add_asteroid_to_window(window):
    """
    Add a new asteroid to the window.

    Args:
        window (GraphWin): Graphics window.

    Returns:
        Image: Asteroid image.
    """
    x_location = random.randrange(40, 601)
    asteroid_img = Image(Point(x_location, 0), 'asteroid.gif')
    asteroid_img.draw(window)
    return asteroid_img


def add_rocket_to_window(window, tank_img):
    """
    Add a new rocket to the window.

    Args:
        window (GraphWin): Graphics window.
        tank_img (Image): Tank image.

    Returns:
        Image: Rocket image.
    """
    rocket_img = Image(tank_img.getCenter(), 'shooter.gif')
    rocket_img.draw(window)
    return rocket_img


def lose_window():
    """
    Display the lose window with play again and quit buttons.
    """
    window = GraphWin('lose window', 400, 200)
    lose_image = Image(Point(200, 100), 'you lose.png')
    lose_image.draw(window)

    play_button = Button(Point(110, 155), 90, 30, 'Play again')
    play_button.draw(window)
    play_button.activate()

    quit_button = Button(Point(300, 155), 90, 30, 'Quit')
    quit_button.draw(window)
    quit_button.activate()

    click = window.getMouse()

    while not (quit_button.isClicked(click) or play_button.isClicked(click)):
        click = window.getMouse()

    if play_button.isClicked(click):
        window.close()
        main()
    elif quit_button.isClicked(click):
        sys.exit()
def win_window():
    """
    Display the win window with an image indicating the player has won.
    """
    win_win = GraphWin('Win Window', 400, 200)
    win_image = Image(Point(200, 100), 'you_win.png')  
    win_image.draw(win_win)

    play_again_button = Button(Point(110, 155), 90, 30, 'Play Again')
    play_again_button.draw(win_win)
    play_again_button.activate()

    quit_button = Button(Point(300, 155), 90, 30, 'Quit')
    quit_button.draw(win_win)
    quit_button.activate()

    click = win_win.getMouse()

    while not (quit_button.isClicked(click) or play_again_button.isClicked(click)):
        click = win_win.getMouse()

    if play_again_button.isClicked(click):
        win_win.close()
        main()
    elif quit_button.isClicked(click):
        sys.exit()


def game_loop(window, tank):
    """
    Main game loop.

    Args:
        window (GraphWin): Graphics window.
        tank (Image): Tank image.
    """
    
    
    rocket_list = []
    asteroid_list = []
    score = 0
    score_label = Text(Point(550, 50), '0')
    score_label.setSize(16)
    
    if score == NUM_WIN:
        win_window()
        window.close()

    while score < 20:
        move_tank(window, tank)
        score_label.draw(window)

        if random.randrange(100) < 5:
            asteroid = add_asteroid_to_window(window)
            asteroid_list.append(asteroid)

        move_asteroid(asteroid_list)
        move_rocket(rocket_list)

        if window.checkKey() == 'space':
            rocket = add_rocket_to_window(window, tank)
            rocket_list.append(rocket)
            time.sleep(0.1)

        for asteroid in asteroid_list:
            for rocket in rocket_list:
                if is_close_enough(rocket, asteroid):
                    asteroid.undraw()
                    asteroid_list.remove(asteroid)
                    score += 1
                    rocket.undraw()
                    rocket_list.remove(rocket)
                    explosion = Image(rocket.getCenter(), 'explosion.png')
                    explosion.draw(window)
                    time.sleep(0.1)
                    explosion.undraw()

                if not is_object_out(rocket, 0):
                    rocket.undraw()
                    rocket_list.remove(rocket)

            if is_object_out(asteroid, 666):
                asteroid.undraw()
                asteroid_list.remove(asteroid)
                score -= 1

            if is_close_enough(tank, asteroid):
                score_label.undraw()
                tank.move(500, 500)
                window.close()
                lose_window()

        time.sleep(STALL_TIME)
        score_label.setText(f"Score: {score}")
        score_label.undraw()

        if score == NUM_WIN:
            window.close()
            win_window()
            

def options_window(window):
    """
    Display the options window to choose a tank.

    Args:
        window (GraphWin): Graphics window.

    Returns:
        str: Selected tank image filename.
    """
    #window.setBackground('white')
    choose = Image(Point(333,333),'choosetank.png')
    choose.draw(window)
    

    keys = Text(Point(300, 50), 'Choose your Tank')
    keys.setSize(30)
    keys.draw(window)

    tank1button = Button(Point(50, 170), 70, 20, 'skunk')
    tank1button.draw(window)
    tank1button.activate()
    tank1 = Image(Point(120, 170), 'tankmain1.gif')
    tank1.draw(window)

    tank2button = Button(Point(50, 280), 70, 20, 'rodeo')
    tank2button.draw(window)
    tank2button.activate()
    tank2 = Image(Point(120, 280), 'tanko.gif')
    tank2.draw(window)

    tank3button = Button(Point(500, 170), 70, 20, 'dipper')
    tank3button.draw(window)
    tank3button.activate()
    tank3 = Image(Point(400, 170), 'greeno.gif')
    tank3.draw(window)

    tank4button = Button(Point(500, 280), 70, 20, 'skull')
    tank4button.draw(window)
    tank4button.activate()
    tank4 = Image(Point(400, 280), 'bazinga1.gif')
    tank4.draw(window)

    click_point = window.getMouse()

    image_select = ''
    while not (
        tank1button.isClicked(click_point)
        or tank2button.isClicked(click_point)
        or tank3button.isClicked(click_point)
        or tank4button.isClicked(click_point)
    ):
        click_point = window.getMouse()

    if tank1button.isClicked(click_point):
        image_select = 'tankmain1.gif'
    elif tank2button.isClicked(click_point):
        image_select = 'tanko.gif'
    elif tank3button.isClicked(click_point):
        image_select = 'greeno.gif'
    elif tank4button.isClicked(click_point):
        image_select = 'bazinga1.gif'

    window.close()

    return image_select


def directions(window):
    """
    Display the directions window.

    Args:
        window (GraphWin): Graphics window.
    """
    window.setBackground('green')
    text_content = f'''Earth is under attack!!!
    Protect us by all means necessary!
    Destroy those savages.
    Lose one point for every robot that passes
    Gain one point for each robot shot down
    score {NUM_WIN} points to win
    Good luck soldier! '''

    directions = Text(Point(300, 300), text_content)
    directions.setSize(20)
    directions.setFill('white')
    directions.setStyle('bold')
    directions.draw(window)
    time.sleep(5)


def draw_background():
    """
    Draw the game background.

    Returns:
        tuple: Graphics window and background image.
    """
    window = GraphWin("Earth under attack!!!", 600, 600)
    background = Image(Point(300, 300), 'main background.png')
    background.draw(window)
    return window, background


def draw_title():
    """
    Draw the game title.

    Returns:
        Text: Title text.
    """
    title = Text(Point(300, 700), 'EARTH UNDER ATTACK')
    title.setSize(20)
    title.setFill('black')
    title.setStyle('bold')
    title.draw(window)
    return title


def animate_title(title):
    """
    Animate the game title.

    Args:
        title (Text): Title text.
    """
    title_center = title.getCenter()
    while title_center.getY() > 80:
        title.move(0, -10)
        title_center = title.getCenter()
        time.sleep(0.1)


def draw_buttons():
    """
    Draw play and quit buttons.

    Returns:
        tuple: Play and quit buttons.
    """
    play_button = Button(Point(300, 300), 70, 20, 'PLAY')
    quit_button = Button(Point(300, 370), 70, 20, 'QUIT')

    play_button.draw(window)
    quit_button.draw(window)

    play_button.activate()
    quit_button.activate()

    return play_button, quit_button


def wait_for_button_click(play_button, quit_button):
    """
    Wait for a button click.

    Args:
        play_button (Button): Play button.
        quit_button (Button): Quit button.

    Returns:
        bool: True if play button clicked, False if quit button clicked.
    """
    click_point = window.getMouse()

    while not (quit_button.isClicked(click_point) or play_button.isClicked(click_point)):
        click_point = window.getMouse()

    return play_button.isClicked(click_point)


def undraw_elements(title, play_button, quit_button, background):
    """
    Undraw game elements.

    Args:
        title (Text): Title text.
        play_button (Button): Play button.
        quit_button (Button): Quit button.
        background (Image): Background image.
    """
    title.undraw()
    play_button.undraw()
    quit_button.undraw()
    background.undraw()


def introduction():
    """
    Display the game introduction and get the selected tank.

    Returns:
        str: Selected tank image filename.
    """
    global window
    window, background = draw_background()
    title = draw_title()
    animate_title(title)
    play_button, quit_button = draw_buttons()

    if wait_for_button_click(play_button, quit_button):
        undraw_elements(title, play_button, quit_button, background)
        directions(window)
        tank_type = options_window(window)
    else:
        sys.exit(1)

    return tank_type


def main():
    """
    Main function to setup and run the game.
    """
    # setup the game
    tank_type = introduction()

    window = GraphWin("Earth under attack!!!", 666, 666)

    background_image = Image(Point(333, 333), 'game background.png')
    background_image.draw(window)
    directions = Text(Point(333, 650), 'Click left/right of the tank to move it.')
    directions.setSize(16)

    directions.draw(window)

    tank = Image(Point(333, 580), tank_type)
    tank.draw(window)

    game_loop(window, tank)


main()
