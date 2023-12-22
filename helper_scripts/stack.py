class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pull(self):
        value = self.stack[-1]
        self.stack = self.stack[:-1]
        return value
        
    def len(self):
        return len(self.stack)
    
    def __str__(self):
        return str(self.stack)
