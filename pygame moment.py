import pygame
import json
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tileset_image = pygame.image.load("graphics/mariosimplesheet.png").convert_alpha()
        with open('graphics/mariosprite_data.json', 'r') as file:
            tile_data = json.load(file)["tiles"]
        self.sprite_index = 0
        self.sprite_index2 = 5
        self.increment = 1
        self.leftorright = 1
        self.crouchstate = 0
    
        self.tile_surface = []
        for i, tile_info in enumerate(tile_data):
            x, y, width, height = tile_info["x"], tile_info["y"], tile_info["width"], tile_info["height"]
            singlesprite = tileset_image.subsurface(pygame.Rect(x, y, width, height))
            singlesprite = pygame.transform.rotozoom(singlesprite, 0, 3)
            self.tile_surface.append(singlesprite)

        self.image = self.tile_surface[self.sprite_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/clover_jump_dunes.ogg")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom >= 300:
            if keys[pygame.K_DOWN]:
                self.crouchstate = 1
            else:
                self.crouchstate = 0
                if keys[pygame.K_RIGHT]:
                    self.rect.x += 3
                if keys[pygame.K_LEFT]:
                    self.rect.x -= 3
            if keys[pygame.K_SPACE]:
                self.gravity = -20
                self.jump_sound.play()
        else: 
            if keys[pygame.K_RIGHT]:
                self.rect.x += 3
            if keys[pygame.K_LEFT]:
                self.rect.x -= 3
            if event.type == pygame.KEYUP and keys == pygame.K_SPACE:
                self.gravity *= 0.2
    
    def apply_gravity(self):
        self.gravity += 1
        if self.gravity >= 20: self.gravity = 20
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            if self.rect.bottom >=300:
                if self.crouchstate == 0:
                    if self.leftorright == 0:
                        self.image = self.tile_surface[5]
                    if self.leftorright == 1:
                        self.image = self.tile_surface[0]
            else: 
                if self.crouchstate == 1:
                    if self.leftorright == 0:
                        self.image = self.tile_surface[9]
                    if self.leftorright == 1:
                        self.image = self.tile_surface[4]
                else:
                    if self.leftorright == 0:
                        self.image = self.tile_surface[8]
                    if self.leftorright == 1:
                        self.image = self.tile_surface[3]

        else:
            if keys[pygame.K_RIGHT]:
                self.leftorright = 1
            if keys[pygame.K_LEFT]:
                self.leftorright = 0
            if self.rect.bottom < 300:
                if self.leftorright == 1:
                    if self.crouchstate == 0:
                        self.image = self.tile_surface[3]
                        if keys[pygame.K_RIGHT]:
                            self.image = self.tile_surface[3]
                        elif keys[pygame.K_LEFT]:
                            self.image = self.tile_surface[8]
                    elif self.crouchstate == 1:
                        self.image = self.tile_surface[4]
                elif self.leftorright == 0:
                    if self.crouchstate == 0:
                        self.image = self.tile_surface[8]
                        if keys[pygame.K_RIGHT]:
                            self.image = self.tile_surface[3]
                        elif keys[pygame.K_LEFT]:
                            self.image = self.tile_surface[8]
                    elif self.crouchstate == 1:
                        self.image = self.tile_surface[9]
            else:
                if self.leftorright == 1:
                    if self.crouchstate == 1:
                        self.image = self.tile_surface[4]
                    elif keys[pygame.K_RIGHT]:
                        if self.increment == 1:
                            self.sprite_index += 0.2
                            if self.sprite_index >= 2.8:
                                self.sprite_index = 2.8
                                self.increment = 0
                        if self.increment == 0:
                            self.sprite_index -= 0.2
                            if self.sprite_index <= 0.2:
                                self.sprite_index = 0.2
                                self.increment = 1
                        self.image = self.tile_surface[int(self.sprite_index)]
                    else: self.image = self.tile_surface[0]
                if self.leftorright == 0:
                    if self.crouchstate == 1:
                        self.image = self.tile_surface[9]
                    elif keys[pygame.K_LEFT]:
                        if self.increment == 1:
                            self.sprite_index2 += 0.2
                            if self.sprite_index2 >= 7.8:
                                self.sprite_index2 = 7.8
                                self.increment = 0
                        if self.increment == 0:
                            self.sprite_index2 -= 0.2
                            if self.sprite_index2 <= 5.2:
                                self.sprite_index2 = 5.2
                                self.increment = 1
                        self.image = self.tile_surface[int(self.sprite_index2)]
                    else: self.image = self.tile_surface[5]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
class Block(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "QuestionBlock":
            tileset_image = pygame.image.load("graphics/questionblock.png")
            self.sprites = []
            tileset_width, tileset_height = tileset_image.get_size()
            x = 0
            while x <= tileset_width - 16:
                sprite = tileset_image.subsurface(pygame.Rect(x, 0, 16, 16))
                sprite = pygame.transform.rotozoom(sprite, 0, 3)
                self.sprites.append(sprite)
                x += 17
            block_pos_x = 200
            self.blockspeed = 0.05
        elif type == "BrickBlock":
            tileset_image = pygame.image.load("graphics/brickblock.png")
            self.sprites = []
            tileset_width, tileset_height = tileset_image.get_size()
            x = 0
            while x <= tileset_width - 16:
                sprite = tileset_image.subsurface(pygame.Rect(x, 0, 16, 16))
                sprite = pygame.transform.rotozoom(sprite, 0, 3)
                self.sprites.append(sprite)
                x += 17
            block_pos_x = 400
            self.blockspeed = 0.1

        self.block_animation_index = 0
        self.image = self.sprites[self.block_animation_index]
        self.rect = self.image.get_rect(midbottom = (block_pos_x, 200))

    def animation_state(self):
        self.block_animation_index += self.blockspeed
        if self.block_animation_index >= len(self.sprites): self.block_animation_index = 0
        self.image = self.sprites[int(self.block_animation_index)]      

    def update(self):
        self.animation_state()      
    

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("funny game")
clock = pygame.time.Clock()

floor_surface = pygame.image.load('graphics/floor.jpg').convert()
floor_surface = pygame.transform.rotozoom(floor_surface, 0, 1.25)

bg_music = pygame.mixer.Sound('audio/helpymusic.mp3')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

block_group = pygame.sprite.Group()
block_group.add(Block("QuestionBlock"))
block_group.add(Block("BrickBlock"))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()


    screen.blit(floor_surface, (0, 0))

    player.draw(screen)
    player.update()
    block_group.draw(screen)
    block_group.update()

    pygame.display.update()
    clock.tick(60)