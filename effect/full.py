from core.effect.base import EffectBase
from survival.tuning.effect import EffectTuning
from siege import game


class Full(EffectBase):
    TUNING = EffectTuning.FULL

    def __init__(self, owner, level, duration, source, isRefresh):
        super(Full, self).__init__(owner, duration, isRefresh)
        self.adjustment = owner.stats.HP.getMax() / 50.0
        self.statUid = owner.stats.HPRegen.mod(self.adjustment)

    def onRemove(self, owner):
        owner.stats.HPRegen.unmod(self.statUid)

    @staticmethod
    def register():
        game.effects.register(Full.TUNING.NAME, Full)
