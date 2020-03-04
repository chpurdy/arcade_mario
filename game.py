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
    
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platform_layer,0.5)

        self.player = Player()
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.wall_list)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.wall_list.draw()
        self.player.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player.update()
        self.player.update_animation()
        
        if self.player.change_y == 0:
            self.player.jumping = False
            self.player.falling = False
        
        if self.player.center_y < 0:
            self.player.start_over()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
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



    