from core.helper import sendMessage, callEvent
from core.util import DamageSource
from core.tuning.effect import EffectTuning as cTuning

import survival.talent.survival_talent
from survival.effect.hunger import Hunger
from survival.effect.thirst import Thirst

from siege import game
from siege.network import NetworkManager


def useFood(food, args, stats=None):
    player = args["player"]

    if game.survival.canUseFood(player):
        game.survival.PlayerEat(player, food)
        if stats is not None:
            entity = player.entity
            for stat in stats.keys():
                amount = stats[stat]
                if stat == 'HP':
                    amount = int(callEvent("heal_entity", player, player.entity, amount=amount).amount)
                if amount:
                    amount = int(entity.stats.get(stat).adjust(amount))
                    # Only use potion if it had an affect
                    game.combat.showCombatNumber(entity, amount, False)
                    args["decrement"] = 1
    else:
        if game.survival.getFoodState(player) == "HungerState_Full":
            sendMessage('general', 'System', "CannotEat_Full", player.networkId)
        else:
            sendMessage('general', 'System', "CannotEat", player.networkId, time=str(game.survival.getFoodTimer(player)))
        args["cancel"] = True


class SurvivalSystem(object):
    NAME = "survival"
    FILE_VERSION = 1

    def __init__(self):
        DamageSource.add("Hunger")

    def getName(self):
        return self.NAME

    def getFoodState(self, player):
        return player.survival.hungerState

    def getDrinkState(self, player):
        return player.survival.thirstState

    def getFoodTimer(self, player):
        return player.survival.eatCooldown / 1000

    def getDrinkTimer(self, player):
        return player.survival.drinkCooldown / 1000

    def canUseDrink(self, player):
        if self.getDrinkTimer(player) > 0:
            return False
        else:
            if self.getDrinkState(player) != "ThirstState_Hydrated":
                return True
            else:
                return False

    def canUseFood(self, player):
        if self.getFoodTimer(player) > 0:
            return False
        else:
            if self.getFoodState(player) != "HungerState_Full":
                return True
            else:
                return False

    def PlayerEat(self, player, amount):
        if self.canUseFood(player):
            value = player.survival.hunger + amount
            if value > 1010:
                value = 1010
            player.survival.hunger = value
            player.survival.eatCooldown = 5000

    def PlayerDrink(self, player, amount):
        if self.canUseDrink(player):
            value = player.survival.thirst + amount
            if value > 1010:
                value = 1010
            player.survival.thirst = value
            player.survival.drinkCooldown = 3000
        pass

    def PlayerJoin(self, player):
        player.entity.effects.remove(Hunger.TUNING.NAME)
        player.entity.effects.remove(Thirst.TUNING.NAME)
        player.entity.effects.remove(cTuning.POISON.NAME)

    def PlayerDeath(self, player, results, damageSource, message):
        # If our player died from starving, set the message accordingly
        if damageSource == DamageSource.Hunger:
            results.message = player.entity.name + " has starved to death"

        # Remove old effects
        player.entity.effects.remove(Hunger.TUNING.NAME)
        player.entity.effects.remove(Thirst.TUNING.NAME)

        # Reset survival data
        player.survival.hunger = 1000
        player.survival.thirst = 1000
        player.survival.updatePlayerStates()

    def createTalent(self, template, identifier):
        template.talents.talents.append(survival.talent.survival_talent.getTalent())

    @staticmethod
    def register():
        survival = SurvivalSystem()
        game.registerSystem(survival.getName(), survival)
        if NetworkManager.isHost():
            game.events['player_joined'].listen(survival.PlayerJoin)
            game.events['player_death'].listen(survival.PlayerDeath)
            game.events['setup_body'].listen(survival.createTalent)

    @staticmethod
    def unregister():
        if NetworkManager.isHost():
            game.events['player_joined'].remove(survival.PlayerJoin)
            game.events['player_death'].remove(survival.PlayerDeath)
            game.events['setup_body'].listen(survival.createTalent)
