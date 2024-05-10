class Space:
    def __init__(self, id, owner, name, description, price_per_night, active):
        self.id = id
        self.owner = owner
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.active = active


    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Space({self.id}, {self.owner}, {self.name}, {self.description}, {self.price_per_night}, {self.active})"