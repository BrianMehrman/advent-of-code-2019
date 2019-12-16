
class PasswordCracker():

    def __init__(self, min_value, max_value):
        super().__init__()

        self.min_value = min_value
        self.max_value = max_value

    def never_decreases(self, value):
        return ''.join(sorted(value[:])) == ''.join(value)

    def two_adjacent(self, value):
        counts = {}

        for i in value:
            if counts.get(i):
                counts[i] += 1
            else:
                counts[i] = 1
        return bool([i for i in counts.values() if i == 2])

    def crack(self):
        passwords = []
        for value in range(self.min_value, self.max_value):
            value = list(str(value))
            if self.never_decreases(value) and self.two_adjacent(value):
                passwords.append(value)

        return passwords

if __name__ == "__main__":
    cracker = PasswordCracker(172851,675869)
    print(len(cracker.crack()))
