import json
import pygame
import random
import sys

#button class
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

#generate the screen the game will be played on
def init_game_display():
    flags = pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN
    screenSize, clock = get_screen_size()
    #screenSize = [1920, 1080]
    pygame.init()
    screen = pygame.display.set_mode(screenSize, flags)
    #screen = pygame.display.set_mode((1920, 1080), flags)
    return screen, clock, screenSize

#start the "menu" window
def main_menu(screen, clock, screenSize):
    pygame.display.set_caption("Menu")
    colors = ["#d1cbcb", "#b68f40", "#050505", "#262626", "#d7fcd4"]
    BG = pygame.image.load("assets/background2.png").convert_alpha()
    BG = pygame.transform.scale(BG, screenSize)

    while True:
        mousePos = pygame.mouse.get_pos()

        #screen.fill("Black")
        screen.blit(BG, (0,0))

        #create the menu text
        menuText = get_font(100).render("TRIVIA GAME!", True, "#b68f40")
        menuRect = menuText.get_rect(center=(screenSize[0]/2, screenSize[1]/4))

        #create the buttons
        start_button = Button(None, (screenSize[0]/2, screenSize[1]/2), "Start", get_font(75), "#d7fcd4", "White")
        exit_button = Button(None, (screenSize[0]/2, screenSize[1]/1.5), "Exit", get_font(75), "#d7fcd4", "White")

        #draw the menu text and rectangle
        screen.blit(menuText, menuRect)

        #if the button is hovered over, change color to hovering_color
        for button in [start_button, exit_button]:
            button.changeColor(mousePos)
            button.update(screen)

        #for functionality for each button:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (start_button.checkForInput(pygame.mouse.get_pos())):
                    score = play_trivia("questions.json", screen, clock, screenSize)
                    score_screen(screen, clock, screenSize, score)
                if (exit_button.checkForInput(pygame.mouse.get_pos())):
                    pygame.quit()
                    sys.exit(0)
        

        #continuously update the display and set the tick rate
        pygame.display.update()
        clock.tick(144)

#start the "game trivia" window
def play_trivia(filePath, screen, clock, screenSize):
    pygame.display.set_caption("Trivia!")

    #print("\nWelcome to trivia! Best of luck!")
    questionsDict = get_questions_dict(filePath)
    idx = 1
    correctAns = 0
    random.shuffle(questionsDict["questions"])

    for i in range(10):
        triviaQuestion = f"Question {idx}: {questionsDict['questions'][i]['question']}"
        triviaChoice1 = f"1) {questionsDict['questions'][i]['choices'][0]}"
        triviaChoice2 = f"2) {questionsDict['questions'][i]['choices'][1]}"
        triviaChoice3 = f"3) {questionsDict['questions'][i]['choices'][2]}"
        triviaChoice4 = f"4) {questionsDict['questions'][i]['choices'][3]}"
        questionAns = trivia_question(triviaQuestion, triviaChoice1, triviaChoice2, triviaChoice3, triviaChoice4, screen, clock, screenSize, idx)

        if (questionAns == questionsDict["questions"][i]["correctAnswerIdx"]):
            correctAns += 1
        idx += 1
    return correctAns

#start the trivia game
def trivia_question(triviaQuestion, triviaChoice1, triviaChoice2, triviaChoice3, triviaChoice4, screen, clock, screenSize, idx):
    pygame.display.set_caption(f"Trivia! Question: {idx}")
    textfontSize = get_font(38, (1920, 1080), screenSize[0], 0.70)
    buttonfontSize = get_font(50, (1920, 1080), screenSize[0], 0.70)
    colors = ["#d1cbcb", "#b68f40", "#050505", "#262626", "#d7fcd4"]
    textColor = colors[0]
    buttonColor = colors[0]
    BG = pygame.image.load("assets/Background.png").convert_alpha()
    BG = pygame.transform.scale(BG, screenSize)

    #BG = pygame.image.load("assets/slop.png")
    while (True):
        mousePos = pygame.mouse.get_pos()

        #screen.fill("#21063b")
        screen.blit(BG, (0,0))

        #create the buttons
        exit_button = Button(None, (screenSize[0]/2, screenSize[1]/1.25), "Exit", get_font(75), buttonColor, "White")

        questionText = textfontSize.render(triviaQuestion, True, textColor)
        questionRect = questionText.get_rect(center=(screenSize[0]/2, screenSize[1]/8))

        triviaChoice1Text = textfontSize.render(triviaChoice1, True, textColor)
        triviaChoice1Rect = questionText.get_rect(center=(screenSize[0]/2, screenSize[1]/5))

        triviaChoice2Text = textfontSize.render(triviaChoice2, True, textColor)
        triviaChoice2Rect = questionText.get_rect(center=(screenSize[0]/2, screenSize[1]/3.5))

        triviaChoice3Text = textfontSize.render(triviaChoice3, True, textColor)
        triviaChoice3Rect = questionText.get_rect(center=(screenSize[0]/2, screenSize[1]/2.65))

        triviaChoice4Text = textfontSize.render(triviaChoice4, True, textColor)
        triviaChoice4Rect = questionText.get_rect(center=(screenSize[0]/2, screenSize[1]/2.15))

        button_offset = (screenSize[0]/4)/2

        choice1_button = Button(None, (screenSize[0]/2 - button_offset, screenSize[1]/1.7), "1", buttonfontSize, buttonColor, "White")
        choice2_button = Button(None, (screenSize[0]/2 - button_offset/2.85, screenSize[1]/1.7), "2", buttonfontSize, buttonColor, "White")
        choice3_button = Button(None, (screenSize[0]/2 + button_offset/2.85, screenSize[1]/1.7), "3", buttonfontSize, buttonColor, "White")
        choice4_button = Button(None, (screenSize[0]/2 + button_offset, screenSize[1]/1.7), "4", buttonfontSize, buttonColor, "White")

        screen.blit(questionText, questionRect)
        screen.blit(triviaChoice1Text, triviaChoice1Rect)
        screen.blit(triviaChoice2Text, triviaChoice2Rect)
        screen.blit(triviaChoice3Text, triviaChoice3Rect)
        screen.blit(triviaChoice4Text, triviaChoice4Rect)

        #if the button is hovered over, change color to hovering_color
        for button in [exit_button, choice1_button, choice2_button, choice3_button, choice4_button]:
            button.changeColor(mousePos)
            button.update(screen)
        
        #for functionality for each button:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (choice1_button.checkForInput(pygame.mouse.get_pos())):
                    return 1
                if (choice2_button.checkForInput(pygame.mouse.get_pos())):
                    return 2
                if (choice3_button.checkForInput(pygame.mouse.get_pos())):
                    return 3
                if (choice4_button.checkForInput(pygame.mouse.get_pos())):
                    return 4
                if (exit_button.checkForInput(pygame.mouse.get_pos())):
                    pygame.quit()
                    sys.exit(0)

        #continuously update the display and set the tick rate
        pygame.display.update()
        clock.tick(144)

#loads the question list from the json file and and returns it
def get_questions_dict(filePath):
    try:
        with open(filePath, "r") as questionsFile:
            questionsDict = json.load(questionsFile)
        return questionsDict
    except Exception as error:
        print("An error occured retrieving the questions list the json file:", error)
        sys.exit(1)

#display the score to the user
def score_screen(screen, clock, screenSize, score):
    pygame.display.set_caption("Trivia! Score")
    BG_win = pygame.image.load("assets/background3.jpg").convert()
    BG_win = pygame.transform.scale(BG_win, screenSize)
    BG_loss = pygame.image.load("assets/Background.png").convert()
    BG_loss = pygame.transform.scale(BG_loss, screenSize)
    colors = ["#d1cbcb", "#b68f40", "#050505", "#262626", "#d7fcd4", "#d96b0b"]
    textColor = colors[5]
    buttonColor = colors[4]

    while True:
        mousePos = pygame.mouse.get_pos()

        #create the menu text
        if (score/10 >= 1/2):
            screen.blit(BG_win, (0,0))
            menuText = get_font(40).render(f"Congratuations! You got a score of {score}/{10}", True, textColor)
        else:
            screen.blit(BG_loss, (0,0))
            menuText = get_font(40).render(f"You got a score of {score}/{10}, better luck next time!", True, textColor)
        
        menuRect = menuText.get_rect(center=(screenSize[0]/2, screenSize[1]/4))

        #create the buttons
        mainMenu_button = Button(None, (screenSize[0]/2, screenSize[1]/2), "Main Menu", get_font(75), buttonColor, "White")
        exit_button = Button(None, (screenSize[0]/2, screenSize[1]/1.5), "Exit", get_font(75), buttonColor, "White")

        #draw the menu text and rectangle
        screen.blit(menuText, menuRect)

        #if the button is hovered over, change color to hovering_color
        for button in [mainMenu_button, exit_button]:
            button.changeColor(mousePos)
            button.update(screen)

        #for functionality for each button:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mainMenu_button.checkForInput(pygame.mouse.get_pos())):
                    return
                if (exit_button.checkForInput(pygame.mouse.get_pos())):
                    pygame.quit()
                    sys.exit(0)

        #continuously update the display and set the tick rate
        pygame.display.update()
        clock.tick(144)

#get the users desired screen size
def get_screen_size():
    pygame.init()
    tmpSize = 1200
    screen = pygame.display.set_mode((tmpSize,tmpSize))
    screenSizes = pygame.display.get_desktop_sizes()

    pygame.display.set_caption("Resolution select")
    clock = pygame.time.Clock()

    #BG = pygame.image.load("assets/floyd.jpg")

    while True:
        mousePos = pygame.mouse.get_pos()

        screen.fill("Black")
        #screen.blit(BG, (0,0))

        #create the menu text
        menuText = get_font(50).render("Select your resolution:", True, "#b68f40")
        menuRect = menuText.get_rect(center=(tmpSize/2, tmpSize/4))

        #create the buttons
        resolution1_button = Button(None, (tmpSize/2, tmpSize/2), str(screenSizes[0]), get_font(75), "#d7fcd4", "White")
        resolution2_button = Button(None, (tmpSize/2, tmpSize/1.5), str(screenSizes[1]), get_font(75), "#d7fcd4", "White")

        #draw the menu text and rectangle
        screen.blit(menuText, menuRect)

        #if the button is hovered over, change color to hovering_color
        for button in [resolution1_button, resolution2_button]:
            button.changeColor(mousePos)
            button.update(screen)

        #for functionality for each button:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (resolution1_button.checkForInput(pygame.mouse.get_pos())):
                    pygame.quit()
                    return screenSizes[0], clock
                if (resolution2_button.checkForInput(pygame.mouse.get_pos())):
                    pygame.quit()
                    return screenSizes[1], clock
        
        #continuously update the display and set the tick rate
        pygame.display.update()
        clock.tick(144)

#get a font size from the font
def get_font(size, referenceRes=None, currentWidth=None, fontRatio=None):
    if (referenceRes == None):
        return pygame.font.Font("assets/font.ttf", size)
    
    reference_width = referenceRes[0]

    # Calculate the scaled font size based on the resolution ratio
    scaledSize = int(size * (currentWidth / reference_width) * fontRatio)
    return pygame.font.Font("assets/font.ttf", scaledSize)