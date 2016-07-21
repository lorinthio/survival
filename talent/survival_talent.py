from siege import game, Talent
from core.talent import addSkill, PassiveSkill
from survival.tuning.skill import SkillTuning

def getTalent():
    talent = Talent("survival", "survival_talent/icon.png", [1000] * 50)

    addSkill(talent, PassiveSkill.create(SkillTuning.HEALTH_BOOST))
    addSkill(talent, PassiveSkill.create(SkillTuning.STAMINA_BOOST))

    game.events['create_talent'].invoke(talent)
    return talent
