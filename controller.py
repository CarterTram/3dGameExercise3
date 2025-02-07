import pub
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub
from game_logic import GameLogic
from player_view import PlayerView
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, GeomNode

controls = {
 'w': 'moveForward',
 'shift-w': 'runForward',
 's': 'moveBackward',
 't': 'toggleTexture',
 'mouse1': 'toggleTexture'
}

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.render.setShaderAuto()

        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic)

        self.picker_node = CollisionNode('mouseRay')
        self.picker_np = self.camera.attachNewNode(self.picker_node)
        self.picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.picker_ray = CollisionRay()
        self.picker_node.addSolid(self.picker_ray)
        self.ray_queue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(self.picker_np, self.ray_queue)

    def new_player_object(self, game_object):
        pass

    def go(self):
        self.game_logic.load_world()
        self.camera.set_pos(0, -20, 0)
        self.camera.look_at(0, 0, 0)
        self.taskMgr.add(self.tick)
        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])
        pub.subscribe(self.new_player_object, 'create')
        self.player = None
        self.run()


    def input_event(self, event):
        self.input_events[event] = True

    def get_nearest_object(self):
        self.picker_ray.setFromLens(self.camNode, 0, 0)
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            entry = self.ray_queue.getEntry(0)
            picked_np = entry.getIntoNodePath()
            picked_np = picked_np.findNetTag('selectable')
            if not picked_np.isEmpty() and picked_np.getPythonTag("owner"):
                return picked_np.getPythonTag("owner")
        return None

    def tick(self, task):
        pub.sendMessage('input', events=self.input_events)
        picked_object = self.get_nearest_object()
        if picked_object:
            picked_object.selected()
        h = self.player.z_rotation
        p = self.player.x_rotation
        r = self.player.y_rotation
        self.camera.setHpr(h, p, r)
        self.camera.set_pos(*self.player.position)
        self.game_logic.tick()
        self.player_view.tick()
        if self.game_logic.get_property("quit"):
            sys.exit()
        self.input_events.clear()
        return Task.cont

if __name__ == '__main__':
    main = Main()
    main.go()