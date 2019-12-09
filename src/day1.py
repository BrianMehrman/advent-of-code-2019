import math

class FuelCounter1:
    @classmethod
    def calculate_fuel(cls, mass):
        return (mass // 3) - 2

    @classmethod
    def for_list(cls, masses):
        return sum([cls.calculate_fuel(mass) for mass in masses])


class FuelCounter:
    @classmethod
    def calculate_fuel(cls, mass):
        fuel = (mass // 3) - 2
        if fuel <= 0:
            return 0
        fuel += cls.calculate_fuel(fuel)
        return fuel

    @classmethod
    def for_list(cls, masses):
        return sum([cls.calculate_fuel(mass) for mass in masses])


if __name__ == "__main__":
    data = open("./data/day1.txt")
    masses = [int(line.rstrip()) for line in data.readlines()]
    print(FuelCounter.for_list(masses))
