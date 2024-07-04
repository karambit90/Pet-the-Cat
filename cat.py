import math
import pygame
import time
import random
import os
pygame.init()


TOP_BAR_HEIGHT = 50
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0,0,0)
LIVES = 9
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

original_image = pygame.image.load(os.path.join("pic", "cat.png"))

original_width, original_height = original_image.get_size()

scale_factor = 0.2

new_width = int(original_width * scale_factor)
new_height = int(original_height * scale_factor)

CAT_IMG = pygame.transform.scale(original_image, (new_width, new_height))

original_image1 = pygame.image.load(os.path.join("pic", "hand.png"))

original_width1, original_height1 = original_image1.get_size()

scale_factor1 = 0.03

new_width1 = int(original_width1 * scale_factor1)
new_height1 = int(original_height1 * scale_factor1)

hand_image = pygame.transform.scale(original_image1, (new_width1, new_height1))

pygame.mixer.music.load('espresso.mp3')

pygame.mixer.music.play(-1) 


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kiss the Cat")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

class Target:
    MAX_SIZE = 60
    MIN_SIZE=0
    GROWTH_RATE = 0.3



    def __init__(self,x,y):
        self.x =x
        self.y= y
        self.size = 0
        self.grow = True


    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

        self.size = max(self.MIN_SIZE, min(self.size, self.MAX_SIZE))

    def draw(self, win):
        scaled_img = pygame.transform.scale(CAT_IMG, (int(self.size), int(self.size)))
        
        win.blit(scaled_img, (self.x - self.size // 1.5, self.y - self.size // 1.5))

    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size



def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)
    
    

def format_time(secs):
    milli = math.floor(int(secs*1000% 1000)/100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs //60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "white", (0,0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
            f"Time: {format_time(elapsed_time)}" , 1 , "red")
    
    speed = round((targets_pressed / elapsed_time), 1)
    speed_label = LABEL_FONT.render(f"Speed :{speed} t/s", 1 , "red")
    pets_label = LABEL_FONT.render(f"Pets :{targets_pressed}", 1 , "red")
    lives_label = LABEL_FONT.render(f"Lives :{LIVES - misses}", 1 , "red")


    win.blit(speed_label, (200, 5))
    win.blit(pets_label, (450, 5))
    win.blit(lives_label, (650, 5))
    win.blit(time_label, (5,5))

def end_screen(win, elapsed_time, target_pressed, click):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
            f"Time: {format_time(elapsed_time)}" , 1 , "red")
    
    speed = round((target_pressed / elapsed_time), 1)
    speed_label = LABEL_FONT.render(f"Speed :{speed} t/s", 1 , "red")
    pets_label = LABEL_FONT.render(f"Pets :{target_pressed}", 1 , "red")
    espresso_label = LABEL_FONT.render(f"Okay but coffee first", 2, "Brown")
   # accuracy = round(target_pressed/click*100 , 1) if click >0 else  0
    #accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1 , "red")

    
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(pets_label, (get_middle(pets_label), 300))
    #win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    win.blit(time_label, (get_middle(time_label),400))
    win.blit(CAT_IMG, (get_middle(CAT_IMG), 100))
    win.blit(espresso_label, (get_middle(espresso_label), 500))

    pygame.display.update()

    run = True
    while run:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 run = False
                 quit()
            
''' if event.type == pygame.KEYDOWN:
                run = False
                quit()'''

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2



def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    click = 0
    misses = 0
    start_time = time.time()

    pygame.mouse.set_visible(False)
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(45)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                click +=1


        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, target_pressed, click)


        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)


        
        WIN.blit(hand_image, (mouse_pos[0] - hand_image.get_width() // 2, mouse_pos[1] - hand_image.get_height() // 2))
        pygame.display.update()



    pygame.quit()
    
if __name__ == "__main__":
    main()