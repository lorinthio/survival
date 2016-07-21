from functools import partial

from core.effect.base import EffectBase
from survival.tuning.effect import EffectTuning

from siege import game
from siege.network import NetworkManager


class Thirst(EffectBase):
    TUNING = EffectTuning.THIRST

    def __init__(self, owner, level, duration, source, isRefresh):
        super(Thirst, self).__init__(owner, duration, isRefresh)
        self.value = owner.stats.SP.getMax() / 20
        self.tick_max = 250
        self.tick = self.tick_max
        self.owner = owner
        owner.event['sp_regen'].listen(partial(self.handleSpRegen, owner.id))
        self.owner.combat.canRecover.set(False)

    def isPositive(self):
        return False

    def update(self, frameTime, owner):
        self.tick -= frameTime
        self.owner.combat.canRecover.set(False)
        if NetworkManager.isHost() and self.tick <= 0:
            sp = owner.stats.SP.get() - self.value
            owner.stats.SP.set(sp)
            self.tick = self.tick_max
        return True

    def handleSpRegen(self, entityId, player, results, spRegenTotal):
        if entityId == player.entity.id:
            results.spRegenTotal = 0

    def onRemove(self, owner):
        owner.event['sp_regen'].remove(partial(self.handleSpRegen, owner.id))
        self.owner.combat.canRecover.set(True)

    @staticmethod
    def register():
        game.effects.register(Thirst.TUNING.NAME, Thirst)
