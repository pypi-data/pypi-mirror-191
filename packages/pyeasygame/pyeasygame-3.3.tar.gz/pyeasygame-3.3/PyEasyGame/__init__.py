import pygame
import random as r
import keyboard as kb
import sys
import time as t

pygame.init()
pygame.display.set_caption('PyEasy Game Window')
pygame.display.set_icon(pygame.image.load('logo.png'))

#window variables
screen = None
screen_once = True
screen_color = (255,255,255)
screen_width = 0
screen_height = 0

#time variables
clock = pygame.time.Clock()

#variables
frames = 60
time = 0 #time delay

#player
player_x = 0
player_y = 0
jumped = False
jump_velocity = 0
player_width = 0
player_height = 0
player_run_once = True
player_speed = 0

original_x = 0
original_y = 0

change_x = 0
change_y = 0

#mouse_click
left_click = False
right_click = False

#key_pressed
keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','space','1','2','3','4','5','6','7','8','9','0']
pygame_keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_SPACE,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]
keys_boolean = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

def mouse_pos(xy):
    mx,my = pygame.mouse.get_pos()
    if xy == 'x':
        return mx
    if xy == 'y':
        return my
    if xy == 'xy':
        return (mx,my)
    pass

def get_fps():
    if clock.get_fps() != 0:
        return clock.get_fps()
    pass

def render_font(font, size):
    return pygame.font.SysFont(font, size)
    pass

def load_img(img_location):
    return pygame.image.load(img_location)
    pass

def rotate(image, angle):
    return pygame.transform.rotate(image, angle)
    pass

def delay_time(time_delay):
    global time
    time = time_delay
    pass

def resize(image, new_width, new_height):
    return pygame.transform.scale(image, (new_width, new_height))
    pass

def set_fps(fps):
    global frames
    frames = fps
    pass

def set_name(name):
    pygame.display.set_caption(name)
    pass

def set_icon(image):
    pygame.display.set_icon(image)
    pass

def update_screen():
    global frames
    clock.tick(frames)
    pygame.time.delay(time)
    pygame.display.flip()
    pass

class Timer:
    def __init__(self, seconds):
        self.sec = seconds
        self.start_time = None
        self.run_timer = True
        self.timer = 0
        self.start_timer = True
    def start(self):
        if self.start_timer:
            self.start_time = t.time()
            self.start_timer = False
        self.current_time = t.time()
        if self.run_timer:
            if self.start_time != None:
                self.timer = self.current_time - self.start_time
        if self.timer >= self.sec:
            self.run_timer = False
            self.timer = self.sec
    def stop(self):
        self.run_timer = False
        pass
    def restart(self,new_time):
        self.start_time = None
        self.run_timer = True
        self.sec = new_time
        self.start_timer = True
        pass
    def time(self):
        return self.timer
        pass
    def __bool__(self):
        if self.timer != self.sec:
            return False
        else:
            return True
    pass

def create_screen(width, height, function=None):
    global screen,screen_once,screen_color,screen_width,screen_height,left_click,right_click
    if screen_once:
        if function == 'fullscreen':
            screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
            screen_width = width
            screen_height = height
        if function == 'resizable':
            screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
            screen_width = width
            screen_height = height
        if function == None:
            screen = pygame.display.set_mode((width,height))
            screen_width = width
            screen_height = height
        screen_once = False
        pass
    screen.fill(screen_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True   
            if event.button == 3:
                right_click = True
        for i in range(len(keys)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame_keys[i]:
                    keys_boolean[i] = True
    pass

def fill_screen(red,green,blue):
    global screen_color
    screen_color = (red,green,blue)
    pass


def draw_image(image,x,y):
    screen.blit(image, (x,y))
    pass

def draw_rect(x,y,width,height,color,border_radius=0):
    if border_radius == 0:
        pygame.draw.rect(screen, color, (x,y,width,height))
    else:
        pygame.draw.rect(screen, color, (x,y,width,height),border_radius)
    pass

def draw_circle(x,y,color,radius,border_radius=0):
    if border_radius != 0:
        pygame.draw.circle(screen,color,(x,y),radius,border_radius)
    else:
        pygame.draw.circle(screen,color,(x,y),radius)
    pass

def draw_line(x1,y1,x2,y2,color,thickness):
    pygame.draw.line(screen, color, (x1,y1), (x2,y2),thickness)
    pass

def player(image,x,y,move_left='a',move_right='d',move_up='w',move_down='s',jump='space',speed=3,jump_height=20, collide_sides=False):
    global original_x,original_y,change_x,change_y,player_speed,player_x,player_y,player_width,player_height,jump_velocity,jumped,player_run_once
    if player_run_once:
        jump_velocity = jump_height
        player_x = x
        player_y = y
        player_width = image.get_width()
        player_height = image.get_height()
        player_speed = speed
        original_x = x
        original_y = y
        player_run_once = False
    change_x = x
    change_y = y
    if change_x != original_x or change_y != original_y:
        player_x = change_x
        player_y = change_y
        player_run_once = True
    if jump != '':
        if jumped == False and kb.is_pressed(jump):
            jumped = True
    if not collide_sides:
        if move_left != '':
            if kb.is_pressed(move_left):
                player_x -= speed
        if move_right != '':
            if kb.is_pressed(move_right):
                player_x += speed
        if move_up != '':
            if kb.is_pressed(move_up):
                player_y -= speed
        if move_down != '':
            if kb.is_pressed(move_down):
                    player_y += speed
        if jump != '':
            if jumped:
                player_y -= jump_velocity
                jump_velocity -= 1
                if jump_velocity < -jump_height:
                    jumped = False
                    jump_velocity = jump_height
    if collide_sides:
        if move_left != '':
            if kb.is_pressed(move_left) and player_x > 0:
                player_x -= speed
        if move_right != '':
            if kb.is_pressed(move_right) and player_x < screen_width - player_width:
                player_x += speed
        if move_up != '':
            if kb.is_pressed(move_up) and player_y > 0:
                player_y -= speed
        if move_down != '':
            if kb.is_pressed(move_down) and player_y < screen_height - player_height:
                player_y += speed
        if jump != '':
            if jumped:
                player_y -= jump_velocity
                jump_velocity -= 1
                if jump_velocity < -jump_height:
                    jumped = False
                    jump_velocity = jump_height
    if collide_sides:
        if player_x > screen_width - player_width:
            player_x = screen_width - player_width
        if player_x < 0:
            player_x = 0
        if player_y > screen_height - player_height:
            player_y = screen_height - player_height
        if player_y < 0:
            player_y = 0
        pass
    screen.blit(image, (player_x,player_y))
    pass

def mouse_click(click='left',one_click=False,return_value=0):
    global left_click, right_click
    mouse = pygame.mouse.get_pressed()
    if click == 'left':
        if not one_click:
            if return_value == 0:
                if mouse[0] == True:
                    return True
                if mouse[0] == False:
                    return False
            else:
                if mouse[0] == True:
                    return 'down'
                if mouse[0] == False:
                    return 'up'
        if one_click:
            if return_value == 0:
                if left_click:
                    left_click = False
                    return True
                else:
                    return False
            else:
                if left_click:
                    left_click = False
                    return 'down'
                else:
                    return 'up'
            pass
    if click == 'right':
        if not one_click:
            if return_value == 0:
                if mouse[2] == True:
                    return True
                if mouse[2] == False:
                    return False
            else:
                if mouse[2] == True:
                    return 'down'
                if mouse[2] == False:
                    return 'up'
        if one_click:
            if return_value == 0:
                if right_click:
                    right_click = False
                    return True
                else:
                    return False
            else:
                if right_click:
                    right_click = False
                    return 'down'
                else:
                    return 'up'
    pass

def key_pressed(key,one_click=False):
    for i in range(len(keys)):
        if one_click:
            if key == keys[i]:
                if keys_boolean[i] == True:
                    keys_boolean[i] = False
                    return True
                else:
                    return False
    if not one_click:
        if kb.is_pressed(key):
            return True
        else:
            return False
    pass    

def text(text,font,color,x,y,show_text=True):
    screen.blit(font.render(text, show_text, color), (x,y))
    pass

def box(image,x,y,collision=True):
    global player_x,player_y,player_width,player_height,player_speed
    player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
    col_box = pygame.Rect(x,y,image.get_width(),image.get_height())
    if collision:
        if player_rect.colliderect(col_box):
            if player_rect.right >= col_box.x and player_rect.right <= col_box.x + (player_speed + 2) :
                player_x = col_box.x - player_rect.width
            if player_rect.left >= col_box.right - (player_speed + 2) and player_rect.left <= col_box.right:
                player_x = col_box.right
            if player_rect.top <= col_box.bottom and player_rect.top >= col_box.bottom - (player_speed + 2):
                player_y = col_box.bottom
            if player_rect.bottom >= col_box.top and player_rect.bottom <= col_box.top + (player_speed + 2):
                player_y = col_box.top - player_rect.height
    screen.blit(image, (x,y))
    pass

def collide(rect1,rect2):
    player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
    mouse_pos = pygame.mouse.get_pos()
    if rect1 == 'player':
        if rect2 != 'mouse':
            if pygame.Rect(player_rect).colliderect(pygame.Rect(rect2)):
                return True
        if rect2 == 'mouse':
            if pygame.Rect(player_rect).collidepoint(mouse_pos):
                return True
    if rect2 == 'player':
        if rect1 != 'mouse':
            if pygame.Rect(player_rect).colliderect(pygame.Rect(rect2)):
                return True
        if rect1 == 'mouse':
            if pygame.Rect(player_rect).collidepoint(mouse_pos):
                return True
    if rect1 == 'mouse':
        if rect2 != 'player':
            if pygame.Rect(rect2).collidepoint(mouse_pos):
                return True
        if rect2 == 'player':
            if pygame.Rect(player_rect).collidepoint(mouse_pos):
                return True
    if rect2 == 'mouse':
        if rect1 != 'player':
            if pygame.Rect(rect2).collidepoint(mouse_pos):
                return True
        if rect1 == 'player':
            if pygame.Rect(player_rect).collidepoint(mouse_pos):
                return True
    if not isinstance(rect1,str) and not isinstance(rect2,str):
        if pygame.Rect(rect1).colliderect(pygame.Rect(rect2)):
            return True

def button(image, x,y,retract_button=True,retract_length=10,click='left', draw_button=True):
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    if draw_button:
        if not retract_button:
            if click == 'left':
                if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                    if mouse[0]:
                        return True
                    else:
                        return False
            if click == 'right':
                if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                    if mouse[2] == True:
                        return True
                    else:
                        return False
            screen.blit(image, (x,y))
        if retract_button:
            if click == 'left':
                if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                    if mouse[0]:
                        screen.blit(resize(image,image.get_width()-retract_length,image.get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                        return True
                    else:
                        screen.blit(image, (x,y))
                        return False
                else:
                    screen.blit(image, (x,y))
            if click == 'right':
                if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                    if mouse[2] == True:
                        screen.blit(resize(image,image.get_width()-retract_length,image.get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                        return True
                    else:
                        screen.blit(image, (x,y))
                        return False
                else:
                    screen.blit(image, (x,y))
    pass

class PickUp:
    def __init__(self, image, x, y, rect,return_value=0):
        self.draw_item = True
        self.image = image
        self.x = x
        self.y = y
        self.rect = rect
        self.box = pygame.Rect(0,0,0,0)
        self.return_value = return_value
    def draw(self):
        global mouse
        mouse = pygame.mouse.get_pressed()
        self.box = pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        if self.draw_item != None:
            if self.rect != 'mouse_click=left' and self.rect != 'mouse_click=right':
                if collide(self.rect,self.box):
                    self.draw_item = False
            elif self.rect == 'mouse_click=left':
                if collide('mouse',self.box):
                    if mouse[0]:
                        self.draw_item = False
            elif self.rect == 'mouse_click=right':
                if collide('mouse',self.box):
                    if mouse[2]:
                        self.draw_item = False
            pass
        if self.draw_item:
            screen.blit(self.image, (self.x,self.y))
        pass
    def __bool__(self):
        if self.draw_item == False:
            if self.return_value == 0:
                self.draw_item = None
                return True
            if self.return_value != 0:
                return True
        else:
            return False
    pass

class Lives:
    def __init__(self,full_heart_img, empty_heart_img, x,y,lives,draw_lives=True):
        self.img1 = full_heart_img
        self.img2 = empty_heart_img
        self.x = x
        self.y = y
        self.health = lives
        self.draw_lives = draw_lives
        pass
    def draw(self,current_lives):
        self.current_lives = current_lives
        if self.draw_lives:
            for i in range(self.health):
                screen.blit(self.img2,(self.x + self.img2.get_width() * i ,self.y))
            for i in range(self.current_lives):
                screen.blit(self.img1, (self.x + self.img1.get_width() * i,self.y))
            if self.current_lives <= 0:
                self.current_lives = 0
    def __int__(self):
        return self.current_lives
    pass

class Bar:
    def __init__(self,x,y,width,height,health,color,border_radius=5,border_img=None,draw_bar=True):
        self.x = x
        self.y = y
        self.h = height
        self.color = color
        self.w = width
        self.health = health
        self.draw_bar = draw_bar
        self.border_img = border_img
        self.border_radius = border_radius
    def draw(self,current_health):
        self.current_health = current_health
        if self.draw_bar:
            if self.border_img != None:
                pygame.draw.rect(screen, self.color, (self.x,self.y,(self.border_img.get_width() * self.current_health) / self.health ,self.border_img.get_height()))
                screen.blit(self.border_img, (self.x,self.y))
            elif self.border_img == None:
                pygame.draw.rect(screen, self.color, (self.x,self.y,(self.w * self.current_health) / self.health ,self.h))
                pygame.draw.rect(screen, (0,0,0), (self.x,self.y,self.w,self.h), self.border_radius)
        if self.current_health <= 0:
            self.current_health = 0
        pass
    def __int__(self):
        return self.current_health
        pass
    pass