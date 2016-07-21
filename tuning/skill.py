from core.helper import AttrDict
from core.util import enum
from siege.graphic import Color
from siege.util import minutes, seconds

class SkillTuning(object):

    HEALTH_BOOST = AttrDict(
        NAME = "HealthBoost",
        DESCRIPTION = "HealthBoostDesc",
        ICON = "mods/core/talent/explore/stamina_boost_icon.png",
        UNLOCK_LEVELS = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39],
        LEVEL_COSTS = [375, 400, 400, 400, 400, 450, 450, 500, 550, 600],
        STAT = 'HP',
        STAT_AMOUNTS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    )

    STAMINA_BOOST = AttrDict(
        NAME = "StaminaBoost",
        DESCRIPTION = "StaminaBoostDesc",
        ICON = "mods/core/talent/explore/stamina_boost_icon.png",
        UNLOCK_LEVELS = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39],
        LEVEL_COSTS = [375, 400, 400, 400, 400, 450, 450, 500, 550, 600],
        STAT = 'SP',
        STAT_AMOUNTS = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
    )
