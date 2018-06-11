# Genetic Algorithm

from random import randint
from random import choice
from random import shuffle
from math   import log
from math   import gcd
from math   import ceil
from copy   import copy
from copy   import deepcopy
from time   import sleep
from time   import time

import pygame

pygame.init()

# Display
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
DISPLAYINFO = pygame.display.Info()
DISPLAY_W   = DISPLAYINFO.current_w
DISPLAY_H   = DISPLAYINFO.current_h

# Text
FONT        = pygame.font.SysFont("CourierNew", 16)
BOLD        = pygame.font.SysFont("CourierNew", 64, bold    = True)
ITALIC      = pygame.font.SysFont("CourierNew", 32, italic  = False)
GREEN       = (32 , 194 , 14 )
BLACK       = (0  , 0   , 0  )
RED         = (255, 0   , 0  )
LBLUE       = (0  , 191 , 255)

# Files
pygame.mixer.music.load("phenotype.mp3")
PHEN_RED    = pygame.image.load("Red.png")
PHEN_GREEN  = pygame.image.load("Green.png")
PHEN_LBLUE  = pygame.image.load("LBlue.png")
CODE        = "code.txt"

# Settings
ACTIVE      = True
DRAWN       = False
CODEMODE    = False
CLOCK       = pygame.time.Clock()
GENERATION  = 1
GLOBAL_FIT  = float("inf")

# Hyperparameters
POPULATION_SIZE = 100
GENERATIONS     = 100
MUTATION_CONST  = 0.01
SCOPE           = (2, 100)

# Mutations
mutations_bases = [["%s * 2"                , "%s * 3"               ],
                   ["%s + choice([1, -1])"  , "%s + choice([2, -2])" ],
                   ["%s * randint(2,100)"   , "%s"                   ],
                   ["%s // 2"               , "%s + randint(1,100)*2"],
                   ["int(str(%s) + choice(['1', '3', '7', '9']))"     ,
                    "int(str(%s) + str(randint(0,9)))"               ], ]

# Phenotype class
class Phenotype:

    #Initialization
    def __init__(self, A, B, x, y):
        self.A  = A
        self.B  = B
        self.x  = x
        self.y  = y
        self.Cz = self.A**self.x + self.B**self.y

        self.error, \
        self.C,     \
        self.z      = self.log3()

        self.fit = self.fitness()

    # Overriding "less-than" operator
    def __lt__(self, other):
        return self.fit < other.fit

    # Overriding "reverse-add" operator
    def __radd__(self, other):
        return self.fit + other

    # Cz calculation using logarithms
    def log3(self):
        max_exp = ceil(log(self.Cz, 3))
        minDiff = (float("inf"), None, None)
        
        for exp in primes(max_exp):

            base      = round(self.Cz**(1/exp))
            diff    = abs(self.Cz - base**exp)

            if diff < minDiff[0]:
                minDiff = (diff, base, exp)
            
        return minDiff

    #Fitness calculation
    def fitness(self):

        Fx = 1/self.x
        Fy = 1/self.y
        Fv = self.error if gcd(self.A, self.B) == 1 and self.A != self.C and self.B != self.C else float("inf")
        Ft = Fx * Fy * Fv

        if Ft == 0:
            exit()

        return Ft

    #Phenotype mutation function
    def mutate(self):
        
        self.A  = eval(choice(mutations_bases)[self.A%2] %self.A)
        self.B  = eval(choice(mutations_bases)[self.B%2] %self.B)
        self.x  = max(3, self.x + choice([-1, 0 ,1]))
        self.y  = max(3, self.y + choice([-1, 0 ,1]))
        self.Cz = self.A**self.x + self.B**self.y

        self.error, \
        self.C,     \
        self.z      = self.log3()

        self.fit = self.fitness()

#Prime number generation
def primes(n):
    n+=1
    sieve = n // 2 * [True] 
    
    for i in range(3, int(n**0.5)+1 ,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1) // (2*i)+1)
    
    return (n>3)*[4]+[2*i+1 for i in range(1,n//2) if sieve[i]]

#Grid drawing
def grid():
    global GENERATION
    global GLOBAL_FIT

    #X axis
    for i in range(10, DISPLAY_W-10):
        DISPLAYSURF.set_at((i,DISPLAY_H - 10), pygame.Color(*GREEN))

    for sign in range(-1,2,2):
        DISPLAYSURF.set_at((i - 1,DISPLAY_H - 10 + 1 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 2,DISPLAY_H - 10 + 1 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 3,DISPLAY_H - 10 + 2 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 3,DISPLAY_H - 10 + 2 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 4,DISPLAY_H - 10 + 2 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 4,DISPLAY_H - 10 + 2 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 5,DISPLAY_H - 10 + 3 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 5,DISPLAY_H - 10 + 3 * sign), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((i - 5,DISPLAY_H - 10 + 3 * sign), pygame.Color(*GREEN))

    X_AXIS = FONT.render("A^x", False, GREEN)
    DISPLAYSURF.blit(X_AXIS, (i - 20, DISPLAY_H - 30))

    #Y axis
    for i in range(10, DISPLAY_H-10):
        DISPLAYSURF.set_at((10, i), pygame.Color(*GREEN))

    for sign in range(-1,2,2):
        DISPLAYSURF.set_at((10 + 1 * sign,10 + 1), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 1 * sign,10 + 2), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 2 * sign,10 + 3), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 2 * sign,10 + 3), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 2 * sign,10 + 4), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 2 * sign,10 + 4), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 3 * sign,10 + 5), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 3 * sign,10 + 5), pygame.Color(*GREEN))
        DISPLAYSURF.set_at((10 + 3 * sign,10 + 5), pygame.Color(*GREEN))

    Y_AXIS = FONT.render("B^y", False, GREEN)
    DISPLAYSURF.blit(Y_AXIS, (15, 10))

    #Scale
    for i in range(20):
        DISPLAYSURF.set_at((DISPLAY_W - 10, 10 + i), pygame.Color(*GREEN))

    DISPLAYSURF.set_at((DISPLAY_W - 10 - 1, 10 + i), pygame.Color(*GREEN))
    DISPLAYSURF.set_at((DISPLAY_W - 10 + 1, 10 + i), pygame.Color(*GREEN))
    
    for i in range(20):
        DISPLAYSURF.set_at((DISPLAY_W - 10 - i, 10), pygame.Color(*GREEN))

    DISPLAYSURF.set_at((DISPLAY_W - 10 - i, 10 + 1), pygame.Color(*GREEN))
    DISPLAYSURF.set_at((DISPLAY_W - 10 - i, 10 - 1), pygame.Color(*GREEN))

    G = "GEN: %s" %GENERATION
    F = "FIT: %s" %GLOBAL_FIT
    GENERAT     = FONT.render(G, False, GREEN)
    FITNESS     = FONT.render(F, False, GREEN)

    DISPLAYSURF.blit(GENERAT, (DISPLAY_W - 35 - 10*len(G), 28))
    DISPLAYSURF.blit(FITNESS, (DISPLAY_W - 35 - 10*len(F), 41))

#Position scaling
def scale(pop):
    MAX_AxP = max(pop, key = lambda phenotype: phenotype.A ** phenotype.x)
    MAX_ByP = max(pop, key = lambda phenotype: phenotype.B ** phenotype.y)
    MAX_Ax  = MAX_AxP.A ** MAX_AxP.x
    MAX_By  = MAX_ByP.B ** MAX_ByP.y

    X_SCALEV    = str(round(MAX_Ax / DISPLAY_W * 20))
    X_SCALE     = FONT.render(X_SCALEV, False, GREEN)
    DISPLAYSURF.blit(X_SCALE, (DISPLAY_W - 35 - 10*len(X_SCALEV),  2))

    Y_SCALEV    = str(round(MAX_By / DISPLAY_H * 20))
    Y_SCALE     = FONT.render(Y_SCALEV, False, GREEN)
    DISPLAYSURF.blit(Y_SCALE, (DISPLAY_W - 35 - 10*len(Y_SCALEV), 15))

    return MAX_Ax, MAX_By

#Phenotype positioning
def display(pop, MAX_Ax, MAX_By, logarithm=False, color=PHEN_GREEN, delay=0.02):

    WID = DISPLAY_W - 20
    HEI = DISPLAY_H - 20

    LOCATIONS = {}
    
    for phenotype in pop:

        Ax = phenotype.A ** phenotype.x
        By = phenotype.B ** phenotype.y
        
        if logarithm:
            X = round(10 +       log(Ax,  MAX_Ax ** (1 / WID)) - 7)
            Y = round(10 + HEI - log(By,  MAX_By ** (1 / HEI)) - 7)
        
        else:
            X = round(10 +       WID / MAX_Ax * Ax - 7)
            Y = round(10 + HEI - HEI / MAX_By * By - 7)
        
        DISPLAYSURF.blit(color, (X, Y))
        LOCATIONS[(X+7, Y+7)] = (phenotype, color)

        sfx(1)
        if delay:
            sleep(delay)
            pygame.display.update()

    return LOCATIONS

#Sound effects
def sfx(num):

    if num == 1:
        pygame.mixer.music.play(0)
        
    elif num == 2:
        pygame.mixer.music.load("complete.mp3")
        pygame.mixer.music.play(0)
        sleep(1)
        pygame.mixer.music.load("phenotype.mp3")
            
#Code preview
def code_display(DELTA):
    
    FONT_SIZE   = 16
    LINE_WIDTH  = 18
    
    DISPLAYSURF.fill(BLACK)
    CODEFONT    = pygame.font.SysFont("CourierNew", FONT_SIZE)
    NO          = 0
    
    with open(CODE, "r") as f:
        for line in f:

            if (line + "0").lstrip()[0] == "#":
                COLOR = RED

            elif (line + "0").lstrip().split()[0] == "def":
                COLOR = LBLUE

            else:
                COLOR = GREEN
                
            NO  += 1
            text = CODEFONT.render(line.strip("\n"), False, COLOR)
            DISPLAYSURF.blit(text, (0, NO * LINE_WIDTH + DELTA))

#Main loop            
grid()
while ACTIVE:
    CLOCK.tick(60)

    #Event handler
    for event in pygame.event.get():

        #Quit event
        if event.type == pygame.QUIT:
            ACTIVE = False

        #Keyboard click event
        elif event.type == pygame.KEYUP:

            #N
            if event.key == pygame.K_n:

                DRAWN       = True
                CODEMODE    = False
                GENERATION  = 1
                GLOBAL_FIT  = float("inf")

                population = []
                for _ in range(POPULATION_SIZE):
                    new = Phenotype(randint(*SCOPE), randint(*SCOPE), 3, 3)
                    population.append(new)
                
                DISPLAYSURF.fill(BLACK)
                grid()
                MAX_Ax, MAX_By = scale(population)
                LOCATIONS = display(population, MAX_Ax, MAX_By, logarithm = False)

                sfx(2)
                
            #BACKSPACE
            elif event.key == pygame.K_BACKSPACE and not DRAWN:

                try:
                    DRAWN       = True
                    CODEMODE    = False
                    
                    DISPLAYSURF.fill(BLACK)
                    grid()
                    MAX_Ax, MAX_By = scale(population)
                    LOCATIONS = display(population, MAX_Ax, MAX_By, logarithm = GENERATION > 1)
                    
                except NameError:
                    pass

                sfx(2)

            #R
            elif event.key == pygame.K_r:

                DRAWN       = False
                CODEMODE    = False
                DISPLAYSURF.fill(BLACK)
                grid()
                pygame.display.update()
                sfx(2)

            #Q
            elif event.key == pygame.K_q:
                
                DRAWN       = False
                CODEMODE    = True
                DELTA       = 0
                code_display(DELTA)
                pygame.display.update()
                sfx(2)
                
            #ARROW KEYS
            elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and CODEMODE:

                DELTA_DELTA = 50
                
                if event.key == pygame.K_DOWN:
                    DELTA -= DELTA_DELTA

                else:
                    DELTA = min(0, DELTA + DELTA_DELTA)
                    
                code_display(DELTA)
                
            #G
            elif event.key == pygame.K_g and DRAWN:

                #Death
                for phenotype in population[:]:
                    if phenotype.fit == float("inf"):
                        population.remove(phenotype)
                        display([phenotype], MAX_Ax, MAX_By, logarithm = GENERATION > 1, color = PHEN_RED)

                sleep(1)

                #Birth
                for _ in range(POPULATION_SIZE-len(population)):
                    newborn = Phenotype(choice(population).A, \
                                        choice(population).B, \
                                        choice(population).x, \
                                        choice(population).y)

                    population.append(newborn)
                    display([newborn], MAX_Ax, MAX_By, logarithm = True, color = PHEN_LBLUE, delay = 0.05)
                    
                population.sort(reverse = True)

                #Mutation
                for index in range(round(POPULATION_SIZE*MUTATION_CONST)):
                    children    = [population[index]]
                    start       = time()
                    
                    while min(children).fit >= population[index].fit and time()-start < 20:
                        for child in children[:]:
                            mutation = copy(child)
                            mutation.mutate()

                            children.append(mutation)

                            DISPLAYSURF.fill(BLACK)
                            grid()
                            MAX_Ax, MAX_By = scale(population + children)
                            display(population, MAX_Ax, MAX_By, logarithm=True, color=PHEN_GREEN, delay=0)
                            display(children  , MAX_Ax, MAX_By, logarithm=True, color=PHEN_LBLUE, delay=0)

                            sleep(0.2)
                            pygame.display.update()
                            

                    population[index] = min(children)

                sfx(2)

                scores = [phenotype for phenotype in population \
                if phenotype.fit != float("inf")]

                GLOBAL_FIT = round(sum(scores)/len(scores), 5)
                GENERATION += 1
                
                DISPLAYSURF.fill(BLACK)
                grid()
                MAX_Ax, MAX_By = scale(population)
                LOCATIONS = display(population, MAX_Ax, MAX_By, logarithm = True)

                
                
                

        #Phenotype information        
        elif event.type ==  pygame.MOUSEBUTTONUP and DRAWN:
            X = event.pos[0]
            Y = event.pos[1]

            for coords in LOCATIONS:
                if abs(X - coords[0]) + abs(Y - coords[1]) <= 5:
                    
                    DRAWN   = False
                    PHEN    = LOCATIONS[coords][0]
                    COLOR   = [GREEN, RED][PHEN.fit == float("inf")]
                    TEXT_1  = "%s^%s + %s^%s = %s^%s"   %(PHEN.A, PHEN.x, PHEN.B, PHEN.y, PHEN.C, PHEN.z)
                    TEXT_2  = "%s + %s = %s"            %(PHEN.A**PHEN.x, PHEN.B**PHEN.y, PHEN.C**PHEN.z)
                    TEXT_Q  = "%s + %s"                 %(PHEN.A**PHEN.x, PHEN.B**PHEN.y)
                    TEXT_3  = TEXT_Q + " = %s"          %(eval(TEXT_Q))
                    TEXT_4  = "DELTA - %s"              %(PHEN.error)
                    TEXT_5  = "|%s - %s| = %s"          %(PHEN.C**PHEN.z, eval(TEXT_Q), PHEN.error)
                    TEXT_6  = "FITNESS - %s"            %(round(PHEN.fit,3))
                    TEXT_7  = "(1 / %s) * (1 / %s) * %s"%(PHEN.x, PHEN.y, PHEN.error)
                    
                    DISPLAYSURF.fill(BLACK)
                    for i in range(DISPLAY_W):
                        DISPLAYSURF.set_at((i, DISPLAY_H // 4), pygame.Color(*COLOR))

                    FORMULA = BOLD.render(  TEXT_1, False, COLOR)
                    NUMBERS = ITALIC.render(TEXT_2, False, COLOR)
                    REALNUM = ITALIC.render(TEXT_3, False, COLOR)
                    OTDELTA = BOLD.render(  TEXT_4, False, COLOR)
                    CLDELTA = ITALIC.render(TEXT_5, False, COLOR)
                    FITNESS = BOLD.render(  TEXT_6, False, COLOR)
                    CALCFIT = ITALIC.render(TEXT_7, False, COLOR)
                    
                    DISPLAYSURF.blit(FORMULA, (961 - 19 * len(TEXT_1), 34))
                    DISPLAYSURF.blit(NUMBERS, (962 - 10 * len(TEXT_2), 185))
                    DISPLAYSURF.blit(REALNUM, (962 - 10 * len(TEXT_3), 340))
                    DISPLAYSURF.blit(OTDELTA, (961 - 19 * len(TEXT_4), 455))
                    DISPLAYSURF.blit(CLDELTA, (962 - 10 * len(TEXT_5), 550))
                    DISPLAYSURF.blit(FITNESS, (961 - 19 * len(TEXT_6), 725))
                    DISPLAYSURF.blit(CALCFIT, (962 - 10 * len(TEXT_7), 825))
                    pygame.display.update()
                    sfx(2)
                    break
    pygame.display.update()
pygame.quit()


