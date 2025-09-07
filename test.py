class Cat:
    def __init__(self, name: str, breed: str):
        self.name = name
        self.breed = breed
    
    def CatName(self, lastname: str):
        return f"This is {self.name} {lastname}"

naming = Cat(name="Tyler", breed="Random")
print(naming.name)