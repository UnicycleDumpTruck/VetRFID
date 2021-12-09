import pyglet
import os
os.environ['DISPLAY'] = ':1'
window = pyglet.window.Window()
image = pyglet.resource.image('media/dog/xray/001.png')

label = pyglet.text.Label('Neigh/Woof/Meow',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)
    label.draw()

pyglet.app.run()