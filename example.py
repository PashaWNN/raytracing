from tinyraytracer import Renderer, Sphere, Vec3f, Light
from tinyraytracer.materials import ivory, mirror, glass, red_rubber


if __name__ == '__main__':
    r = Renderer()

    spheres = [
        Sphere((-3,    0,   -16.0), 2,      ivory),
        Sphere((-1.0, -1.5, -12.0), 2,     mirror),
        Sphere((-1.0, -1.5, -12.0), 2,      glass),
        Sphere(( 1.5, -0.5, -18.0), 3, red_rubber),
        Sphere(( 7,    5,   -18.0), 4,     mirror),
    ]

    lights = [
        Light((-20, 20, 20), 2),
    ]

    im = r.render(spheres, lights)
    im.show()
