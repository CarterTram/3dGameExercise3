from panda3d.core import Quat
from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id):
        super().__init__(position, kind, id)
        pub.subscribe(self.input_event, 'input')
        # pub.subscribe(self.new_game_object,'create')
        self.speed = 0.1
        self.is_jumping = False
        self.jump_height = 2
        self.jump_speed = 0.2
        self.jump_progress = 0

    def input_event(self, events=None):
        if events:
            q = Quat()
            q.setHpr((self.z_rotation, self.x_rotation, self.y_rotation))
            delta_x = delta_y = delta_z = 0

            if 'forward' in events:
                forward = q.getForward()
                delta_x, delta_y, delta_z = forward[0], forward[1], forward[2]

            if 'backward' in events:
                forward = q.getForward()
                delta_x, delta_y, delta_z = -forward[0], -forward[1], -forward[2]

            if 'left' in events:
                right = q.getRight()
                delta_x, delta_y, delta_z = -right[0], -right[1], -right[2]

            if 'right' in events:
                right = q.getRight()
                delta_x, delta_y, delta_z = right[0], right[1], right[2]

            if delta_x or delta_y or delta_z:
                x, y, z = self.position
                self.position = (x + delta_x * self.speed, y + delta_y * self.speed, z + delta_z * self.speed)

    def tick(self):

        if self.is_jumping:
            self.jump_progress += self.jump_speed
            if self.jump_progress < 1:
                self.position = (self.position[0], self.position[1], self.position[2] + self.jump_height * self.jump_speed)
            elif self.jump_progress < 2:
                self.position = (self.position[0], self.position[1], self.position[2] - self.jump_height * self.jump_speed)
            else:
                self.is_jumping = False
