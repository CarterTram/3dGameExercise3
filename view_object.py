from pubsub import pub

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object

        self.cube_texture = base.loader.loadTexture("textures/crate.png")
        if game_object.kind == "player":
            self.model = base.loader.loadModel("models/frowney.egg")
            self.model.setTexture(None)
        elif game_object.kind == "panda":
            self.model = base.loader.loadModel("models/panda.egg")
        else:  # Default to cube
            self.model = base.loader.loadModel("models/cube")
            self.model.setTexture(self.cube_texture)
        self.model.reparentTo(base.render)
        self.model.setTag('selectable', '')
        self.model.setPythonTag("owner", self)
        self.model.setPos(*game_object.position)
        self.model.setScale(1, 1, 1)

        self.current_hpr = self.model.getHpr()
        self.is_selected = False
        self.toggle_texture_pressed = False
        self.rotate_panda_pressed = False
        self.texture_on = True

        pub.subscribe(self.toggle_texture, 'input')
        pub.subscribe(self.rotate_panda, 'input')

    def deleted(self):
        self.cube.setPythonTag("owner", None)

    def selected(self):
        self.is_selected = True

    def toggle_texture(self, events=None):
        if self.game_object.kind == "panda" and 'toggleTexture' in events:
            self.toggle_texture_pressed = True


    def rotate_panda(self, events=None):
        print('hi')
        if self.game_object.kind == "panda" and 'spin' in events:
            print('helo')
            if self.rotate_panda_pressed == False:
               self.rotate_panda_pressed = True
            else:
                self.rotate_panda_pressed = False

    def tick(self):
        h = self.game_object.z_rotation
        p = self.game_object.x_rotation
        r = self.game_object.y_rotation
        self.model.setHpr(h, p, r)
        if self.rotate_panda_pressed:
            self.current_hpr = self.current_hpr + (10, 0, 0)
            self.model.setHpr(self.current_hpr)

        if self.toggle_texture_pressed and self.is_selected:
            if self.texture_on:
                self.texture_on = False
                self.model.setTextureOff(1)
            else:
                self.texture_on = True
                self.model.setTexture(self.cube_texture)

            self.toggle_texture_pressed = False
