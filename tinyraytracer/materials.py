from . import Material, Vec4f, Vec3f


ivory = Material(
    color=Vec3f(0.4, 0.4, 0.3),
    albedo=Vec4f(0.6, 0.3, 0.1, 0.0),
    specular=50,
    refractive_index=1
)
red_rubber = Material(
    color=Vec3f(0.3, 0.1, 0.1),
    albedo=Vec4f(0.9, 0.1, 0.0, 0.0),
    specular=10,
    refractive_index=1
)
mirror = Material(
    albedo=Vec4f(0.0, 10.0, 0.8, 0.0),
    color=Vec3f(1.0, 1.0, 1.0),
    specular=1425,
    refractive_index=1
)
glass = Material(
    albedo=Vec4f(0.0,  0.5, 0.1, 0.8),
    refractive_index=1.5,
    color=Vec3f(0.6, 0.7, 0.8),
    specular=125,
)