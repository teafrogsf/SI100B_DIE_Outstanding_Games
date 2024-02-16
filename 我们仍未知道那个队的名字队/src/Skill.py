class Skill():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


@staticmethod
def predefined_weapon_templates():
    return [
        (("合金护盾"),1),
        (("超载冲击"),2),
        (("毒素注射"),3)
    ]
