from survival.effect.hunger import Hunger
from survival.effect.thirst import Thirst
from survival.effect.full import Full
from survival.effect.hydrated import Hydrated


def register():
    Hunger.register()
    Thirst.register()
    Full.register()
    Hydrated.register()
