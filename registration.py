from siege import game

import survival.effect
import survival.tuning
from survival.component.survivalComp import Survival, SurvivalComponent
import survival.system.registration


def addComp(player):
    player.entity.add(Survival())


def register():
    game.events['player_joined'].listen(addComp)
    survival.effect.register()
    survival.system.registration.register()
    SurvivalComponent.register()


def unregister():
    game.events['player_joined'].remove(addComp)
    survival.system.registration.unregister()
