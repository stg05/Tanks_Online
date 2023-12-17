from models.entities.tanks_physics import *


class TankModel1(TankFast):
    def __init__(self, *args, **kwargs):
        kwargs.update({"color": ARMYGREEN,
                       "image_name": "test_tank_model1.png",
                       "vrt_hull": (
                           (60, 0), (80, -10), (80, -40), (20, -40), (-20, -40), (-80, -40), (-80, -10), (-60, -0)),
                       "vrt_tower": ((20, -40), (30, -50), (30, -70), (-30, -70), (-30, -50), (-20, -40)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)


class TankModel2(TankSlow):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": KHAKI,
                       "image_name": "test_tank_model2.png",
                       "vrt_hull": (
                           (60, 0), (80, -12), (80, -30), (60, -38), (55, -48), (-80, -48), (-75, -8), (-60, -0)),
                       "vrt_tower": ((30, -48), (30, -66), (-10, -72), (-30, -69), (-30, -48)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)
