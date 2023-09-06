from ursina import *
from ursina.shaders import basic_lighting_shader as bls

Entity.default_shader = bls


class Cars(Entity):
    ignoreList = [None]
    toggle_collisions = False
    def __init__(self, position=Vec3(0), **kwargs):
        super().__init__()
        self.model = "car"
        self.collider="box"
        self.position = position
        self.y = 0.13
        self.vel_vector = Vec3(0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []
        self.lines = []

        self.right_sensor = Entity(parent=self, model="sphere", color=color.cyan, scale=0.1, position=(0.15, 0.05, -0.6), collider="sphere")

        self.left_sensor = Entity(parent=self, model="sphere", color=color.cyan, scale=0.1, position=(-0.15, 0.05, -0.6), collider="sphere")
        
        # user defined extra definitions
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        
        self.drive()
        self.rotate()
        self.radars.clear()

        for line in self.lines:
            destroy(line)
        self.lines.clear()

        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.check_collision()
        self.data()

    def input(self, key):
        if key == "space":
            self.position = Vec3(0)

        if key == "m":
            e = Entity(model="cube", collider="box", position=mouse.world_point)

    def drive(self):
        self.position -= self.forward * time.dt * 2

        self.position -= self.forward * (held_keys["up arrow"]- held_keys["down arrow"]) * time.dt * 7
        self.rotation_y -= (held_keys["left arrow"]- held_keys["right arrow"]) * time.dt * 100


    def check_collision(self):
        length = 50
        # Die on Collision
        if self.right_sensor.intersects(ignore=(self,*Cars.ignoreList), debug=True).hit:
            print_on_screen("right sensor hits")
        if self.left_sensor.intersects(ignore=(self,*Cars.ignoreList), debug=True).hit:
            print_on_screen("left sensor hits")

    def rotate(self):
        if not self.radars: return
        
        print("r",self.radars[0][1]+self.radars[1][1]+self.radars[2][1])
        
        left = self.radars[0][1]+self.radars[1][1]+self.radars[2][1]
        right = self.radars[2][1]+self.radars[3][1]+self.radars[4][1]

        if left > right:
            self.direction = 1
        elif left < right:
            self.direction = -1
        else:
            self.direction = 0


        if self.direction == 1:
            # self.angle -= self.rotation_vel
            self.rotation_y -= 5
        if self.direction == -1:
            # self.angle += self.rotation_vel
            self.rotation_y += 5

    def radar(self, radar_angle):

        length = 0
        x = self.x
        z = self.z

        circle = Entity(model="sphere", color=color.red, scale=0.05, position=self.position, collider="sphere", rotation_y = self.rotation_y+radar_angle+180)

        while not circle.intersects(ignore=(self, self.right_sensor, self.left_sensor, circle, *Cars.ignoreList)).hit and length < 10:
                length += 0.5
                # x = int(self.x + math.cos(math.radians(self.rotation_y + radar_angle +90)) * length)
                # z = int(self.y - math.sin(math.radians(self.rotation_y + radar_angle+90)) * length)
                circle.position += circle.forward * length
                # circle.position = Vec3(x, self.y, z)

                # pos =  circle.intersects(ignore=(self, ground, self.right_sensor, self.left_sensor, circle,self)).point
                # if pos: circle.position = pos

        m = Entity(model = Mesh(vertices=[self.position, circle.position], mode="line",colors = color.green), unlit=True) # Vec3(x,self.y,z)
        # m.model.generate()
        self.lines.append(m)
        self.lines.append(circle)
                

        dist = distance(self, circle)
        self.radars.append([radar_angle, dist])
        

    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        print(input)
        return input
        
if __name__ == "__main__":
    app = Ursina(borderless = False)

    car1 = Cars(position=Vec3(0,0,0))
    # car2 = Car(position=Vec3(10,0,0))
    # car3 = Car(position=Vec3(15,0,0))

    Entity(model="cube", texture="white_cube", x=5, y=1, z=-1, scale=3, collider="box")
    Entity(model="cube", texture="white_cube", x=-5, y=1, z=-2,scale=3, collider="box")
    cube  = Entity(model="cube", texture="white_cube", x=5,  y=1, z=-3, scale=3, collider="box")
    duplicate(cube, z=5)
    duplicate(cube, z=-15)
    duplicate(cube, x=15, z=-10)

    ground = Entity(model="plane", texture="grass", scale=200)

    EditorCamera()

    app.run()