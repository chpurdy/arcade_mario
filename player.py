import arcade
from constants import *
import math

GRAVITY = 1
FACE_RIGHT = 1
FACE_LEFT = 2


class Player(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()
        self.jump_right_textures = []
        self.jump_left_textures = []
        self.slide_left_textures = []
        self.slide_right_textures = []
        self.scale = 0.2
        self.center_y = 110
        self.center_x = 50
        self.speed = 5
        self.jumping = False
        self.falling = False
        self.sliding = False

        for i in range(5):
            texture = arcade.load_texture(f"images/Character/Idle__00{i}.png")
            self.stand_right_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Idle__00{i}.png",mirrored=True)
            self.stand_left_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Run__00{i}.png")
            self.walk_right_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Run__00{i}.png",mirrored=True)
            self.walk_left_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Jump__00{i}.png")
            self.jump_right_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Jump__00{i}.png",mirrored=True)
            self.jump_left_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Slide__00{i}.png")
            self.slide_right_textures.append(texture)
            texture = arcade.load_texture(f"images/Character/Slide__00{i}.png",mirrored=True)
            self.slide_left_textures.append(texture)

        self.update_animation()

    def start_over(self):
        self.center_y = 110
        self.center_x = 50
        self.speed = 5
        self.jumping = False
        self.falling = False
        self.change_x = 0
        self.change_y = 0

    
    def jump(self):
        self.jumping = True
        self.change_y = 10

    def land(self):
        self.jumping = False
        self.falling = False
        self.change_y = 0

    def update(self):
        if self.change_x == 0:
            self.sliding = False
        if self.jumping:
            self.sliding = False
        self.center_x += self.change_x
        self.center_y += self.change_y


        
        
    
    def update_animation(self, delta_time: float = 1/60):
        
        """
        Logic for selecting the proper texture to use.
        """
        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        texture_list = []

        change_direction = False
        if self.change_x > 0 and self.state != FACE_RIGHT:
            self.state = FACE_RIGHT
            change_direction = True
        elif self.change_x < 0 and self.state != FACE_LEFT:
            self.state = FACE_LEFT
            change_direction = True
        
        if self.change_x == 0 and self.change_y == 0:
            if self.state == FACE_LEFT:
                self.texture = self.stand_left_textures[0]
                #texture_list = self.stand_left_textures
            elif self.state == FACE_RIGHT:
                self.texture = self.stand_right_textures[0]
                #texture_list = self.stand_right_textures

        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == FACE_LEFT:
                if self.sliding:
                    texture_list = self.slide_left_textures
                elif self.change_y == 0:   
                    texture_list = self.walk_left_textures
                elif self.change_y > 0:
                    texture_list = self.jump_left_textures[:1]
                
                else:
                    texture_list = self.jump_right_textures[1:2]
            
                
            elif self.state == FACE_RIGHT:
                if self.sliding:
                    texture_list = self.slide_right_textures
                elif self.change_y == 0:
                    texture_list = self.walk_right_textures
                elif self.change_y > 0:
                    texture_list = self.jump_right_textures[:1]
                
                else:
                    texture_list = self.jump_right_textures[1:2]
               
                
            self.cur_texture_index += 1
            
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0
            self.texture = texture_list[self.cur_texture_index]

        if self._texture is None:
            print("Error, no texture set")
        else:
            self.width = self._texture.width * self.scale
            self.height = self._texture.height * self.scale

            