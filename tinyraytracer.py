from geometry import Vec2f, Vec3f, Vec3i, Vec4f
from PIL import Image
from numpy import reshape, array


class Renderer:
    def __init__(self, width=1024, height=768):
        self.width = width
        self.height = height
        self.framebuffer = [Vec3f()] * (width * height)

    def render(self):
        for j in range(self.height):
            for i in range(self.width):
                self.framebuffer[i+j*self.width] = Vec3f(j/self.height, i/self.width, 0)

        arr = []
        for i in range(self.height * self.width):
            for j in range(3):
                arr.append(int(255 * max(0, self.framebuffer[i][j])))

        arr = reshape(arr, (self.height, self.width, 3))
        im = Image.fromarray(arr.astype('uint8'), mode='RGB')
        #ar = array(im)
        im.show()


if __name__ == '__main__':
    r = Renderer()
    r.render()
