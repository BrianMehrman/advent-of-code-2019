import math

class FuelCounter:
    @classmethod
    def calculate_fuel(cls, mass):
        return (mass // 3) - 2

    @classmethod
    def for_list(cls, masses):
        return sum([cls.calculate_fuel(mass) for mass in masses])

data = open("./data/day1.txt")
masses = [int(line.rstrip()) for line in data.readlines()]
print(FuelCounter.for_list(masses))
