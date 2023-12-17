from models.entities.tanks_physics import *


class TankModel1(TankFast):
    def __init__(self, *args, **kwargs):
        kwargs.update({"color": ARMYGREEN,
                       "image_name": "test2_tank_model1.png",
                       "vrt_hull": (
                           (60, 0), (80, -10), (80, -40), (20, -40), (-20, -40), (-80, -40), (-80, -10), (-60, -0)),
                       "vrt_tower": ((20, -40), (30, -50), (30, -70), (-30, -70), (-30, -50), (-20, -40)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)


class TankModel2(TankSlow):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": KHAKI,
                       "image_name": "test2_tank_model2.png",
                       "vrt_hull": (
                           (60, 0), (80, -12), (80, -30), (60, -38), (55, -48), (-80, -48), (-75, -8), (-60, -0)),
                       "vrt_tower": ((30, -48), (30, -66), (-10, -72), (-30, -69), (-30, -48)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)


class TankModel3(TankMiddle):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": RED_VINE,
                       "image_name": "test2_tank_model3.png",
                       "vrt_hull": (
                           (-60, -40), (-70, -20), (-60, 0), (52, 0), (62, -20), (52, -40)
                       ),
                       "vrt_tower": ((-24, -40), (-34, -48), (-29, -60), (26, -60), (9, -40)),
                       "gun_pos": (10, -50)})
        super().__init__(*args, **kwargs)


class CruiserWithMinigun(TankFast):
    def __init__(self, *args, **kwargs):
        kwargs.update({"color": ARMYGREEN,
                       "image_name": "cruiser_with_minigun.png",
                       "vrt_hull": (
                           (-40, -7), (34, -8), (34, -24), (-39, -24)
                       ),
                       "vrt_tower": ((-8, -32), (-5, -38), (-5, -45), (-9, -51)),
                       "gun_pos": (-6, -41)})
        super().__init__(*args, **kwargs)
        self.gun = MiniGun(self.screen, self.color, self.rev, self.gun_x, self.gun_y)