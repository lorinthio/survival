from core.helper import sendMessage

from siege import game
from siege.component import Component, ComponentDefinition, ComponentFactory
from siege.network import NetworkManager
from siege.util import Timer, seconds
from siege.log import Log

from collections import OrderedDict

import survival.notification as Notify
from survival.tuning.effect import EffectTuning


class SurvivalComponent(Component):
    '''Component Dependencies: Physics, Stats, Combat'''

    TYPE = "survival"
    CID = 0
    VERSION = 1
    STATE_UPDATE_TIME = 3000
    DRINK_UPDATE_TIME = 500
    THIRST_RATE = 8
    HUNGER_RATE = 5
    THIRST_STATES = OrderedDict([("ThirstState_Dehydrated", 50), ("ThirstState_Parched", 200), ("ThirstState_Thirsty", 400), ("ThirstState_DryMouth", 700), ("ThirstState_Hydrated", 1000)])
    HUNGER_STATES = OrderedDict([("HungerState_Starving", 50), ("HungerState_Famished", 200), ("HungerState_Hungry", 400), ("HungerState_Content", 700), ("HungerState_Full", 1000)])

    def getType(self):
        return SurvivalComponent.TYPE

    def __init__(self, definition, player):
        Component.__init__(self)
        self.player = player
        self.hunger = definition.hunger
        self.thirst = definition.thirst
        self.hungerState = definition.hungerState
        self.thirstState = definition.thirstState
        self.stateTimer = Timer(SurvivalComponent.STATE_UPDATE_TIME)
        self.drinkTimer = Timer(SurvivalComponent.DRINK_UPDATE_TIME)
        self.eatCooldown = 0
        self.drinkCooldown = 0
        self.freeze()

    def update(self, frameTime):
        Log.info('Component update')
        # Handled host handling / timer timing
        if not NetworkManager.isHost():
            return
        self.stateTimer.update(frameTime)
        self.drinkTimer.update(frameTime)
        if self.stateTimer.expired():
            self.stateTimer.reset(SurvivalComponent.STATE_UPDATE_TIME)
            self.updatePlayerStates()
        if self.drinkTimer.expired():
            self.drinkTimer.reset(SurvivalComponent.DRINK_UPDATE_TIME)
            self.checkDrinking()
        self.eatCooldown = max(self.eatCooldown - frameTime, 0)
        self.drinkCooldown = max(self.drinkCooldown - frameTime, 0)

    def checkDrinking(self):
        if self.player.breath.isSubmerged():
            value = self.thirst + 100
            if value > 1000:
                value = 1000
            self.thirst = value

    def updatePlayerStates(self):
        # Thirst State
        self.thirst -= SurvivalComponent.THIRST_RATE
        if self.thirst <= SurvivalComponent.THIRST_STATES["ThirstState_Dehydrated"]:
            self.thirst = 0
            self.player.effects.add(EffectTuning.THIRST.NAME, level=1, duration=seconds(self.tick_max / 900.0), source=None)
        elif self.thirst >= SurvivalComponent.THIRST_STATES["ThirstState_DryMouth"]:
            self.player.effects.add(EffectTuning.HYDRATED.NAME, level=1, duration=seconds(self.tick_max / 900.0), source=None)

        for state in SurvivalComponent.THIRST_STATES.keys():
            if self.thirst < SurvivalComponent.THIRST_STATES[state]:
                if self.thirstState != state:
                    self.thirstState = state
                    self.sendState(self.player, state)
                break

        # subtract our hunger rate
        self.hunger -= SurvivalComponent.HUNGER_RATE
        # If their hunger state is starving
        if self.hunger <= SurvivalComponent.HUNGER_STATES["HungerState_Starving"]:
            self.hunger = 0
            self.player.effects.add(EffectTuning.HUNGER.NAME, level=1, duration=seconds(self.tick_max / 900.0), source=None)
        # If their hunger state is full
        elif self.hunger >= SurvivalComponent.HUNGER_STATES["HungerState_Content"]:
                self.player.effects.add(EffectTuning.FULL.NAME, level=1, duration=seconds(self.tick_max / 900.0), source=None)

        # for each of the different hunger states
        for state in SurvivalComponent.HUNGER_STATES.keys():
            if self.hunger < SurvivalComponent.HUNGER_STATES[state]:
                if self.hungerState != state:
                    self.hungerState = state
                    self.sendState(self.player, state)
                break

    def sendState(self, player, state_msg):
        Notify.sendSurvivalMessage(player, state_msg)
        sendMessage('general', 'Survival', state_msg, player.networkId)

    def pack(self, stream):
        self.write(stream)

    def unpack(self, stream):
        self.read(stream, SurvivalComponent.VERSION)
        self.updatePlayerStates()

    def write(self, stream):
        self.current.write(stream)
        stream.writeUint16(self.hunger)
        stream.writeUint16(self.thirst)

    def read(self, stream, version):
        self.current.read(stream)
        self.hunger = stream.readUint16()
        self.thirst = stream.readUint16()

    @staticmethod
    def factory(entity, componentType, definition):
        if entity.isContentEntity():
            entity.add(SurvivalComponent(definition, None))
            comp = None  # Set breath to None here so that the BasicSystem does not manage the component
        else:
            comp = SurvivalComponent(definition, entity)
            entity.add(comp)
            Log.info(str(definition))
            Log.info('player has survival component')
        return comp

    @staticmethod
    def register():
        SurvivalComponent.CID = game.entity.requestCid(SurvivalComponent.TYPE, Survival)
        game.registerComponent(SurvivalComponent.TYPE, ComponentFactory.create(SurvivalComponent.factory))


class Survival(ComponentDefinition):
    def __init__(self, hunger=1000, thirst=1000, hungerState="HungerState_Full", thirstState="ThirstState_Hydrated"):
        ComponentDefinition.__init__(self)
        self.hunger = hunger
        self.thirst = thirst
        self.hungerState = hungerState
        self.thirstState = thirstState
        self.freeze()

    def getType(self):
        return SurvivalComponent.TYPE
