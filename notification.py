from collections import deque

from core.util import enum
from core.system.notification import Notification, NotificationType

from siege import game, Locale, InventoryItem
from siege.io import DataStream
from siege.network import Message, MessageHandler, NetworkManager
from siege.util import GameEvent, seconds
from siege.world import World

NotificationType.add("Hunger", "Thirst")

def sendSurvivalMessage(player, message):
    if not NetworkManager.isStandalone() and World.get().isActivePlayer(player):
        if "HungerState" in message:
            game.notification.add(HungerNotification(message))
        elif "ThirstState" in message:
            game.notification.add(ThirstNotification(message))
    else:
        # Send notification data to player
        packet = DataStream(Message.NOTIFICATION_SYSTEM)
        if "HungerState" in message:
            packet.writeUint8(NotificationType.Hunger)
            packet.writeString(message)
            game.network.getServer().send(player.networkId, packet)
        elif "ThirstState" in message:
            packet.writeUint8(NotificationType.Thirst)
            packet.writeString(message)
            game.network.getServer().send(player.networkId, packet)

class HungerNotification(Notification):
    DURATION_TIME = seconds(10)

    def __init__(self, message):
        self.locale = message
        self.duration = 0

    def getText(self):
        return Locale.get(self.locale)

    def getIcon(self):
        return "mods/survival/effect/hunger.png"

    def onInteract(self):
        return

class ThirstNotification(Notification):
    DURATION_TIME = seconds(10)

    def __init__(self, message):
        self.locale = message
        self.duration = 0

    def getText(self):
        return Locale.get(self.locale)

    def getIcon(self):
        return "mods/survival/effect/thirst.png"

    def onInteract(self):
        return
