class Country:
    def __init__(self, name, ruler_name, strength, relationship, status, position):
        self.name = name
        self.ruler_name = ruler_name
        self.strength = strength
        self.relationship = relationship
        self.status = status
        self.position = position

    def set_relationship(self, value):
        self.relationship = value

    def set_strength(self, new_strength):
        self.strength = new_strength

    def update_relationship(self, value):
        self.relationship += value

    def update_strength(self, value):
        self.strength += value

    def update_status(self, new_status):
        self.status = new_status
        if self.status == 'Ally':
            self.relationship = 70
        if self.status == 'War':
            self.relationship = 25