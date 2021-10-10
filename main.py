#necessary libraries
import  pygame
from random import randint

pygame.init()
#size of gaming screen
height=936
width=864
screen=pygame.display.set_mode((width,height))
done=False
clock=pygame.time.Clock()
fps=60
#image variables
bg=pygame.image.load('bg.png')
ground=pygame.image.load('ground.png')
button_image = pygame.image.load('restart.png')
#variables
scroll=0
scroll_speed=4
flying=False
gameover=False
pipegap=300
pipe_frequency=1500 #milliseconds
last_pipe=pygame.time.get_ticks()
font=pygame.font.SysFont('Bauhaus 93',60)
white=(255,255,255)
pass_pipe=False
score=0

def print_score(text,font,col,x,y):
    img=font.render(text,True,col)
    screen.blit(img,(x,y))
def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(height/2)
    score=0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(1,4):
            img=pygame.image.load(f'bird{i}.png')
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect= self.image.get_rect()
        self.rect.center = (x,y)
        self.vel=0
        self.clicked=False

    def update(self):

        if flying:
            # gravity
            self.vel += 0.5
            if self.vel >8:
                self.vel =8
            if self.rect.bottom <768:
                self.rect.y += self.vel
            #jump when we press mouse
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel =-10
            if pygame.mouse.get_pressed()[0] ==0:
                self.clicked=False
        #handle the animation
            cooldown=5
            self.counter +=1
            if self.counter >cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images):
                    self.index =0
            self.image = self.images[self.index]
        #rotate
            self.image = pygame.transform.rotate(self.images[self.index],self.vel*-1)
        elif gameover:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += self.vel
            self.image = pygame.transform.rotate(self.images[self.index], -90)
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('pipe.png')
        self.rect=self.image.get_rect()
        #position 1 means x and y are from top, if -1 means x and y are from bottom
        if position==-1:
            self.rect.topleft=[x , y+(pipegap/2)]
        else:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-(pipegap/2)]
    def update(self):
        if flying:
            self.rect.x -= scroll_speed
            if self.rect.right <0:
                self.kill()
class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        action=False

        #get position of mouse
        pos= pygame.mouse.get_pos()
        #check whether mouse is clicked on restart button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action=True
        # draw restart button
        screen.blit(self.image, (self.rect.x-100, self.rect.y))
        return action




bird_group = pygame.sprite.Group()
flappy = Bird(100,int(height/2))
bird_group.add(flappy)
pipe_group=pygame.sprite.Group()
button=Button(width//2,height//2,button_image)


while not done:
    clock.tick(fps)
    # background pic
    screen.blit(bg, (0, 0))

    #pipe pic
    pipe_group.draw(screen)
    # bird pic
    bird_group.update()
    bird_group.draw(screen)
    # ground moving
    screen.blit(ground, (scroll, 768))
    #score count
    if len(pipe_group)>0:
        if pass_pipe==False and bird_group.sprites()[0].rect.left >pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right <pipe_group.sprites()[0].rect.right:
            pass_pipe=True
        if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score +=1
            pass_pipe=False
    print_score('score'+'='+str(score),font,white,int(width/2)-100,20)
    #look for collision
    if pygame.sprite.groupcollide(pipe_group,bird_group,False,False) or flappy.rect.top <0 or flappy.rect.bottom>=768:
        gameover=True
        flying=False
        print_score('GAME OVER',font,(0,0,0),int(width/2)-200,int(height/4))

    #check for bird touching ground
    if flappy.rect.bottom >768:
        gameover=True
        print_score('GAME OVER', font, (0, 0, 0), int(width / 2) - 200, int(height / 4))
    if flying and gameover==False:
        #creating new pipes
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe >pipe_frequency:
            pipe_height_variable= randint(-100,100)
            btm_pipe = Pipe(width, int(height / 2)+pipe_height_variable, -1)
            top_pipe = Pipe(width, int(height / 2)+pipe_height_variable, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now
        #moving ground
        scroll=scroll-scroll_speed
        if abs(scroll) > 35:
            scroll = 0
        pipe_group.update()
    #check whether game is ended
    if gameover==True:
        if button.draw():
            gameover=False
            score = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT and gameover==False:
            done = True
        if event.type == pygame.MOUSEBUTTONUP and flying==False and gameover==False:
            flying=True
    pygame.display.update()
pygame.quit()

