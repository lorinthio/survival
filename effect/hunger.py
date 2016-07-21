from functools import partial

from core.combat import applyDamage
from core.effect.base import EffectBase
from survival.tuning.effect import EffectTuning
from core.util import DamageSource

from siege import game
from siege.network import NetworkManager


class Hunger(EffectBase):
    TUNING = EffectTuning.HUNGER

    def __init__(self, owner, level, duration, source, isRefresh):
        super(Hunger, self).__init__(owner, duration, isRefresh)
        self.value = owner.stats.HP.getMax() / 20
        self.tick_max = 500
        self.tick = self.tick_max

        game.events['heal_entity'].listen(partial(self.handleHeal, owner.id))
        owner.event['hp_regen'].listen(partial(self.handleHpRegen, owner.id))

    def update(self, frameTime, owner):
        self.tick -= frameTime
        if NetworkManager.isHost() and self.tick <= 0:
            hp = owner.stats.HP.get() - self.value
            if hp <= 0:
                applyDamage(owner, self.value, origin=None, knockback=None, damageSource=DamageSource.Hunger)
            else:
                owner.stats.HP.set(hp)
            self.tick = self.tick_max
        return True

    def isPositive(self):
        return False

    def handleHeal(self, entityId, player, results, user, target, amount):
        if entityId == target.id:
            results.amount = 0

    def handleHpRegen(self, entityId, player, results, hpRegenTotal):
        if entityId == player.entity.id:
            results.hpRegenTotal = 0

    def onRemove(self, owner):
        game.events['heal_entity'].remove(partial(self.handleHeal, owner.id))
        owner.event['hp_regen'].remove(partial(self.handleHpRegen, owner.id))

    @staticmethod
    def register():
        game.effects.register(Hunger.TUNING.NAME, Hunger)
