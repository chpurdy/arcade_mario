import arcade
from constants import *
from player import Player

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLUE)
        self.background = None

    def setup(self):
        self.background = arcade.load_texture('images/BG/BG.png')
        map_name = 'maps/mario.tmx'
        platform_layer = 'Main Layer'
        scenary_layer = 'Scenary'
    
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platform_layer,0.5)
        self.scenary_list = arcade.tilemap.process_layer(my_map,scenary_layer,0.5)
        self.map_width = (my_map.tile_size.width*my_map.map_size.width)
        self.player = Player()
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.wall_list)

        # setup the viewport variables
        self.view_left = 0
        self.view_bottom = 0



    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(self.view_left,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.wall_list.draw()
        self.player.draw()
        self.scenary_list.draw()
        

    def on_update(self, delta_time):
        self.physics_engine.update()

        # manage scrolling

        # only call change_viewport if we actually changed it!
        changed = False

        # scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary and self.view_left > 0:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary and self.view_left + SCREEN_WIDTH < self.map_width/2:
            self.view_left += self.player.right - right_boundary
            changed = True

        
        # scroll up
        # top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        # if self.player.top > top_boundary:
        #     self.view_bottom += self.player.top - top_boundary
        #     changed = True

        # # scroll down
        # bottom_boundary = self.view_bottom 
        # if self.player.bottom < bottom_boundary:
        #     self.view_bottom -= bottom_boundary 
        #     changed = True

        # make sure boundaries are integers
        self.view_bottom = int(self.view_bottom)
        self.view_left = int(self.view_left)

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT+self.view_bottom - 1)
                                


        self.player.update()
        self.player.update_animation()
        
        if self.player.change_y == 0:
            self.player.jumping = False
            self.player.falling = False
        
        if self.player.center_y < 0:
            self.player.start_over()

        if self.player.right >= self.view_left + SCREEN_WIDTH:
            self.player.change_x = 0


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT and self.player.right < self.view_left + SCREEN_WIDTH:
            self.player.change_x = self.player.speed
        elif key == arcade.key.LEFT:
            self.player.change_x = -self.player.speed

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.jump()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.player.change_x = 0


def main():
    game = Game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()



    