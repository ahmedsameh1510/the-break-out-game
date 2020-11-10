import pyglet, pymunk
from pyglet import window
from pyglet.window import key
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random

collision_types = {"ball": 1, "block": 2, "bottom": 3, "stick": 4}


def create_block(space, x, y):
    shape = pymunk.Poly.create_box(None, (80, 30))
    body = pymunk.Body(1, pymunk.inf, body_type=pymunk.Body.STATIC)
    shape.body = body
    shape.elasticity = 0.98
    body.position = (x, y)
    shape.collision_type = collision_types["block"]
    space.add(body, shape)
    return shape


def create_ball(space):
    shape = pymunk.Circle(None, 15)
    #moment1 = pymunk.moment_for_circle(mass=1, inner_radius=0, outer_radius=15)
    body = pymunk.Body(1, pymunk.inf, body_type=pymunk.Body.DYNAMIC)
    shape.body = body
    shape.elasticity = 0.98
    body.position = (355, 70)
    shape.collision_type = collision_types["ball"]
    space.add(body, shape)
    return shape


def create_stick(space):
    shape = pymunk.Poly.create_box(None, (155, 20))
    body = pymunk.Body(1, pymunk.inf, body_type=pymunk.Body.KINEMATIC)
    shape.body = body
    shape.elasticity = 0.98
    body.position = (350, 45)
    shape.collision_type = collision_types["stick"]
    space.add(body, shape)
    return shape


def create_wall(space, pos1, pos2, isbottom=False):
    shape = pymunk.Segment(space.static_body, pos1, pos2, 10)
    shape.elasticity = 0.98
    if isbottom:
        shape.sensor = True
        shape.collision_type = collision_types["bottom"]
    space.add(shape)
    return shape


options = DrawOptions()
window = pyglet.window.Window(700, 500, "Break Out Zamalek")
window.set_icon(pyglet.image.load('icon.jpg'))
image1 = pyglet.resource.image('خلفيه الاهلي.jpg')
batch = pyglet.graphics.Batch()

space = pymunk.Space()
space.gravity = (0, 0)

block_surface = pyglet.image.load('block.jpg')
j = 0
blocks = []
blocks_images = []
for y in range(5):
    i = 0
    for x in range(8):
        block = create_block(space, i + 55, window.height - 25 + j)
        blocks.append(block)
        i += 85
    j -= 40

ball = create_ball(space)
ball_image = pyglet.sprite.Sprite(pyglet.image.load('الكوره.png'), 339, 50)

stick = create_stick(space)
stick_image = pyglet.sprite.Sprite(pyglet.image.load('الخشبه.png'), stick.body.position.x - 159 / 2,
                                   stick.body.position.y - 12)

ball_on_stick = True


def const_velocity(body, gravity, damping, dt):
    ball.body.velocity = body.velocity.normalized() * 600

left_wall = create_wall(space, (-10, -10), (-10, window.height + 10))
up_wall = create_wall(space, (-10, window.height + 10), (window.width + 10, window.height + 10))
right_wall = create_wall(space, (window.width + 10, window.height + 10), (window.width + 10, -10))

down_wall = create_wall(space, (-10, -10), (window.width + 10, -10), True)
handler_bottom = space.add_collision_handler(collision_types["ball"], collision_types["bottom"])

def reset_ball(arbiter, space, data):
    reset_game()
    return True


handler_bottom.begin = reset_ball

handler = space.add_collision_handler(collision_types["block"], collision_types["ball"])
def remove_block(arbiter, space, data):
    block_shape = arbiter.shapes[0]
    space.remove(block_shape, block_shape.body)
    blocks.remove(block_shape)
handler.separate = remove_block


def reset_game():
    global stick, ball, ball_on_stick, stick_image
    ball_on_stick = True
    for constraint in space.constraints:
        space.remove(constraint)
    for shape in space.shapes:
        if shape.body != space.static_body and shape.body.body_type != pymunk.Body.STATIC:
            space.remove(shape.body, shape)
    stick = create_stick(space)
    ball = create_ball(space)
    stick_image.x = stick.body.position.x - 159 / 2
    stick_image.y = stick.body.position.y - 12



@window.event
def on_text_motion(motion):
    if motion == pyglet.window.key.MOTION_RIGHT and stick.body.position.x <= window.width - 75:
        stick.body.position += (50, 0)
        stick_image.x = stick.body.position.x - 159 / 2
        if ball_on_stick == True:
            ball.body.position = stick.body.position + (0, 15)
    elif motion == pyglet.window.key.MOTION_LEFT and stick.body.position.x >= 75:
        stick.body.position -= (30, 0)
        stick_image.x = stick.body.position.x - 159 / 2
        if ball_on_stick == True:
            ball.body.position = stick.body.position + (0, 15)


@window.event
def on_key_press(symbol, modifiers):
    global ball_on_stick
    if symbol == key.SPACE:
        if ball_on_stick:
            ball_on_stick = False
            ball.body.apply_impulse_at_local_point(Vec2d(random.choice([(50, 500), (100, 500), (-50, 500), (-100, 500)])))
    if symbol == key.R:
        reset_game()

image_winner=pyglet.image.load('eltas3a.jpg')
music_winner=pyglet.resource.media('alahly hayatna.mp3',streaming=True)
music_playing=pyglet.resource.media('eltalta shemal.mp3',streaming=True)
winner_label=pyglet.text.Label("ِWinner Al-Ahly is The Champion",font_name='Times New Roman',font_size=35,
                       x=window.width/2,y=window.height/2+100,anchor_x='center',anchor_y='center',bold=True)
winnner=False
x=y=0
def winner():
    global x,winnner,y
    if len(blocks)==0:
        x+=1
    if x==0 and y==0:
        music_playing.play()
        y+=1
    if x==1:
        winnner=True
        music_winner.play()

@window.event
def on_draw():
    window.clear()
    image1.blit(-150, -250)
    batch.draw()
    space.debug_draw(options)
    for block in range(len(blocks)):
        block_image = pyglet.sprite.Sprite(block_surface, blocks[block].body.position.x - 40,
                                           blocks[block].body.position.y - 15)
        blocks_images.append(block_image)
        block_image.draw()
    stick_image.draw()
    ball_image.draw()
    if winnner:
        image_winner.blit(-5,-5)
        winner_label.draw()



def update(dt):
    space.step(dt)
    if ball_on_stick==False:
        ball.body.velocity_func = const_velocity
    else:
        ball.body.velocity=(0,0)
    ball_image.x = ball.body.position.x - 16
    ball_image.y = ball.body.position.y - 20
    winner()

pyglet.clock.schedule_interval(update, 1.0 / 60)
pyglet.app.run()
