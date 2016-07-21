from core.helper import AttrDict
from core.tuning.skill import DamageType, SkillTuning
from siege.util import minutes, RangeInt, seconds


class EffectTuning(object):

    FULL = AttrDict(
        NAME = "Full",
        ICON = "mods/survival/effect/hunger.png",
        DESC = "FullDesc",
    )

    HYDRATED = AttrDict(
        NAME = "Hydrated",
        ICON = "mods/survival/effect/thirst.png",
        DESC = "HydratedDesc",
    )

    HUNGER = AttrDict(
        NAME = "Hunger",
        ICON = "mods/survival/effect/hunger.png",
        DESC = "HungerDesc",
    )

    THIRST = AttrDict(
        NAME = "Thirst",
        ICON = "mods/survival/effect/thirst.png",
        DESC = "ThirstDesc",
    )
