from tinyraytracer import Renderer, Sphere, Vec3f, Light
from tinyraytracer.materials import ivory, mirror, glass, red_rubber


if __name__ == '__main__':
    r = Renderer()

    spheres = [
        Sphere(Vec3f(-3,    0,   -16), 2,      ivory),
        Sphere(Vec3f(-1.0, -1.5, -12), 2,     mirror),
        Sphere(Vec3f(-1.0, -1.5, -12), 2,      glass),
        Sphere(Vec3f( 1.5, -0.5, -18), 3, red_rubber),
        Sphere(Vec3f( 7,    5,   -18), 4,     mirror),
    ]

    lights = [
        Light(Vec3f(-20, 20, 20), 2),
    ]

    r.render(spheres, lights)
