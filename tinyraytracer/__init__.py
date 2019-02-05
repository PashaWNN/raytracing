from .geometry import Vec3f, Vec4f
from PIL import Image
from sys import stderr
from numpy import reshape, sqrt, tan, pi
from typing import Union, Iterable


vec3ftype = Union[Vec3f, Iterable[float]]
vec4ftype = Union[Vec4f, Iterable[float]]


class Light:
    def __init__(self, position: vec3ftype, intencity: float):
        self.position = Vec3f(position)
        self.intencity = intencity


class Material:
    def __init__(self, color: vec3ftype, albedo: vec4ftype = Vec4f(1,0,0,0), specular=1.5, refractive_index=1.0):
        self.diffuse_color = Vec3f(color)
        self.albedo = Vec4f(albedo)
        self.specular = specular
        self.refractive_index = refractive_index


class Sphere:

    def __init__(self, center: vec3ftype, radius: float, material: Material):
        self.center = Vec3f(center)
        self.r = radius
        self.material = material

    def ray_intersect(self, origin: Vec3f, direction: Vec3f):
        L = self.center - origin
        tca = L * direction
        d2 = L * L - tca * tca
        if d2 > self.r * self.r:
            return False, None
        thc = sqrt(self.r * self.r - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        return (t0 >= 0), t0


class Renderer:
    def __init__(self, width=int(1024/2), height=int(768/2)):
        self.width = width
        self.height = height
        self.fov = pi / 2
        self.framebuffer = [Vec3f()] * (width * height)

    def render(self, spheres, lights):
        for j in range(self.height):
            stderr.write(f'\r{j/self.height*100:.1f}%  ')
            stderr.flush()
            for i in range(self.width):
                x = (2*(i + 0.5)/self.width - 1) * tan(self.fov/2) * self.width/self.height
                y = (2*(j + 0.5)/self.height - 1) * tan(self.fov/2)
                dir = Vec3f(x, y, -1).normalize()
                self.framebuffer[i+j*self.width] = self._cast_ray(Vec3f(0,0,0), dir, spheres, lights)
        stderr.write('\r      ')
        stderr.flush()
        arr = []
        for i in range(self.height * self.width):

            c = self.framebuffer[i]
            m = max(c[0], max(c[1], c[2]))
            if m > 1:
                self.framebuffer[i] = c * (1/m)

            for j in range(3):
                arr.append(int(255 * max(0, self.framebuffer[i][j])))

        arr = reshape(arr, (self.height, self.width, 3))
        im = Image.fromarray(arr.astype('uint8'), mode='RGB')
        im.show()

    def _cast_ray(self, origin: Vec3f, direction: Vec3f, spheres, lights, depth=0):
        intersection, hit, N, material = self._scene_intersect(origin, direction, spheres)
        if depth > 2 or not intersection:
            return Vec3f(0.2, 0.7, 0.8)

        reflect_dir = self.reflect(direction, N).normalize()
        refract_dir = self.refract(direction, N, material.refractive_index).normalize()
        reflect_orig = hit - N*1e-3 if reflect_dir*N < 0 else hit + N*1e-3
        refract_orig = hit - N*1e-3 if reflect_dir*N < 0 else hit + N*1e-3
        reflect_color = self._cast_ray(reflect_orig, reflect_dir, spheres, lights, depth + 1)
        refract_color = self._cast_ray(refract_orig, refract_dir, spheres, lights, depth + 1)

        diffuse_light_intencity = 0
        specular_light_intencity = 0
        for light in lights:
            light_dir = (light.position - hit).normalize()
            light_distance = (light.position - hit).norm()
            shadow_orig = hit - N*1e-3 if light_dir * N < 0 else hit + N*1e-3
            shadow_i, shadow_pt, *_ = self._scene_intersect(shadow_orig, light_dir, spheres)
            if shadow_i and (shadow_pt - shadow_orig).norm() < light_distance:
                continue
            diffuse_light_intencity += light.intencity * max(0, light_dir*N)
            specular_light_intencity += (max(0, -self.reflect(-light_dir, N)*direction) ** material.specular) * \
                light.intencity

        return material.diffuse_color * diffuse_light_intencity * material.albedo[0] + Vec3f(1,1,1) * \
               specular_light_intencity * material.albedo[1] + reflect_color * material.albedo[2] + \
               refract_color * material.albedo[3]

    @staticmethod
    def _scene_intersect(origin: Vec3f, direction: Vec3f, spheres):
        spheres_dist = float('+inf')
        hit = Vec3f()
        N = Vec3f()
        material = Material(Vec3f())
        for sphere in spheres:
            intersect, dist_i = sphere.ray_intersect(origin, direction)
            if intersect and dist_i < spheres_dist:
                spheres_dist = dist_i
                hit = origin + direction * dist_i
                N = (hit - sphere.center).normalize()
                material = sphere.material
        checkerboard_dist = float('+inf')
        if abs(direction.y) > 1e-3:
            d = (-origin.y + 4) / direction.y
            pt = origin + direction * d
            if (d > 0 and abs(pt.x) < 10 and pt.z < -10 and pt.z > -30 and d < spheres_dist):
                checkerboard_dist = d
                hit = pt
                N = Vec3f(0,1,0)
                material.diffuse_color = Vec3f(1,1,1) if (int(0.5 * hit.x + 1000) + int(0.5 * hit.z)) & 1 else \
                    Vec3f(1, 0.7, 0.3)
                material.diffuse_color = material.diffuse_color * 0.3
        return min(spheres_dist, checkerboard_dist) < 1000, hit, N, material

    @staticmethod
    def reflect(I: Vec3f, N: Vec3f):
        return I - N * 2 * (I * N)

    @staticmethod
    def refract(I: Vec3f, N: Vec3f, refractive_index: float):
        cosi = -max(-1, min(1, I*N))
        etai = 1
        etat = refractive_index
        n = N
        if cosi < 0:
            cosi = -cosi
            etai, etat = etat, etai
            n = -N
        eta = etai / etat
        k = 1 - eta*eta*(1-cosi*cosi)
        return Vec3f(0,0,0) if k < 0 else I*eta + n*(eta*cosi-sqrt(k))
