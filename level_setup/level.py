from importlib.util import set_loader
import pygame
from player.player import Player, player_speed
from settings.settings import *
from support.support import Import_CSV, Split_TileSet
from support.tile import *
from .layer_loader import tile_grouper
from distutils.log import debug


class Level:
    def __init__(self, csv_path = "tilesets\\export_map\\prototype\\", level_path = "assets\placeholder tileset.png"):
        
        # set sprite groups
        self.world_sprites = pygame.sprite.Group()
        self.collidable_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
    
        # group the sprite groups
        self.groups = [self.world_sprites,self.collidable_sprites,self.player]

        # tiling stuff
        self.layers = None
        self.surface = pygame.display.get_surface()
        self.path = csv_path
        
        # self.layout = Import_CSV(csv_path)
        self.align = 0
        self.tiles = Split_TileSet(level_path)
        self.setup_level()

        # optics
        self.initial_pos = self.Get_init_pos()
        self.level_shift = 0
        self.map_height = len(Import_CSV(csv_path + "prototype map_base.csv")) * TILE_SIZE
        self.map_length = len(Import_CSV(csv_path + "prototype map_base.csv")[0]) * TILE_SIZE
        self.screen_view = pygame.display.get_surface()
        self.offset = abs(self.map_height  - SCREEN_HEIGHT)

        self.map_rect = Screen_Fill((0,self.map_height - LOWER_BOUND),self.world_sprites,(self.map_length , LOWER_BOUND))

        self.playerObj = None
        
        # camera settings
        self.look_ahead_vertical = 0
        self.look_ahead_horizontal = 0


    
    def Side_Scroll(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        x_direct = player.direction.x

        LEFT_BOUND = SCREEN_WIDTH / 4
        RIGHT_BOUND = SCREEN_WIDTH - LEFT_BOUND

        # if player_x <= LEFT_BOUND or player_x >= RIGHT_BOUND:
        #     self.level_shift = -player.direction.x * player_speed
        #     player.speed = 0
        if player_x <= LEFT_BOUND and x_direct < 0:
            self.level_shift = -x_direct * player_speed
            player.speed = 0
        elif player_x >= RIGHT_BOUND and x_direct > 0:
            self.level_shift = -x_direct * player_speed
            player.speed = 0
        else:
            self.level_shift = 0
            player.speed = player_speed

    def Get_init_pos(self):
        pos = []
        for sprite in self.world_sprites:
            pos.append(sprite.rect.y)
        return pos

    def Vertical_Align(self):
        player = self.player.sprite
        player_y = player.rect.centery
        y_direct = player.direction.y

        
        if player_y <= UPPER_BOUND and y_direct < 0:
            self.align = -y_direct * player.gravity_factor
        elif player_y >= LOWER_BOUND and y_direct > player.gravity_factor:
            self.align = -y_direct * player.gravity_factor
        else:
            self.align = 0
        if self.map_rect.rect.colliderect(player):
            self.align = 0

        # black_box = pygame.draw.rect(self.screen_view, (0,0,0,0), (0, (SCREEN_HEIGHT - self.offset ) + self.align * -y_direct, SCREEN_WIDTH, self.offset))
        
        # pygame.draw.rect(lower_collider_box)
        # if player.rect.y > self.mapoffset
        # somehow lock the map pos

    def setup_level(self):
        tile_grouper(self.player, self.path,self.tiles, self.groups)
   

    def Vertical_Collision(self):
        player = self.player.sprite
        player.Apply_Gravity()
        grounded = False
        for sprite in self.collidable_sprites:
            has_collided = sprite.rect.colliderect(player)
            if has_collided:
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.is_grounded = True
                    player.direction.y = 0
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def Horizontal_Collision(self):
        player = self.player.sprite
        player.Move_Horizontal()
        for sprite in self.collidable_sprites:
            has_collided = sprite.rect.colliderect(player)
            if has_collided:
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def Draw(self):
        self.player.update()
        self.player.draw(self.surface)
        self.world_sprites.update(self.level_shift, self.align)
        self.world_sprites.draw(self.surface)
 
    def Check_Collisions(self):
        self.Horizontal_Collision()
        self.Vertical_Collision()
    
    def Check_Grounded(self):
        return self.player.sprite.is_grounded
    
    def run(self):
        self.playerObj = self.player.sprite
        self.Side_Scroll()
        self.Draw()
        self.Check_Collisions()
        self.Vertical_Align()