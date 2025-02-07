from game_object import GameObject
from pubsub import pub

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        self.next_id = 0

    def create_object(self, position, kind):
        obj = GameObject(position, kind, self.next_id)
        self.game_objects[obj.id] = obj
        self.next_id += 1
        pub.sendMessage('create', game_object=obj)
        return obj

    def tick(self):
        for obj in self.game_objects.values():
            obj.tick()

    def load_world(self):
        self.create_object([0, 0, 0], "crate")
        self.create_object([2, 0, 0], "crate")
        self.create_object([0, 3, 0], "crate")
        self.create_object([0, -3, 0], "player")

    def get_property(self, key):
        return self.properties.get(key, None)

    def set_property(self, key, value):
        self.properties[key] = value