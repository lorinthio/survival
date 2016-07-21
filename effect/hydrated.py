from core.effect.base import EffectBase
from survival.tuning.effect import EffectTuning
from siege import game


class Hydrated(EffectBase):
    TUNING = EffectTuning.HYDRATED

    def __init__(self, owner, level, duration, source, isRefresh):
        super(Hydrated, self).__init__(owner, duration, isRefresh)
        self.adjustment = owner.stats.SP.getMax() / 20
        self.statUid = owner.stats.SPRegen.mod(self.adjustment)

    def onRemove(self, owner):
        owner.stats.SPRegen.unmod(self.statUid)

    @staticmethod
    def register():
        game.effects.register(Hydrated.TUNING.NAME, Hydrated)
