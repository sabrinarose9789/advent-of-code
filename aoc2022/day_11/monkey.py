import math
class Monkey:
    def __init__(self, items, operation, value, rule, true_monkey, false_monkey):
        self.items = items
        self.operation = operation
        self.value = value
        self.rule = rule
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspected = 0
    
    def throw_items(self, mod_val):
        throw_to = {}
        throw_to[self.true_monkey] = []
        throw_to[self.false_monkey] = []
        for item in self.items:
            if self.value == 'old' and self.operation == '*':
                item *= item
            elif self.value == 'old' and self.operation == '+':
                item += item
            elif self.operation == '*':
                item *= int(self.value)
            else:
                item += int(self.value)
            if item % self.rule == 0:
                throw_to[self.true_monkey].append(item % mod_val)
            else:
                throw_to[self.false_monkey].append(item % mod_val)
            self.inspected += 1
        self.items = []
        return throw_to

    def __str__(self):
        lines = []
        lines.append(f"Items: {self.items}")
        lines.append(f"Operation: new = old {self.operation} {self.value}")
        lines.append(f"If true: throw to monkey {self.true_monkey}")
        lines.append(f"If false: throw to monkey {self.false_monkey}")
 
        return '\n'.join(lines)