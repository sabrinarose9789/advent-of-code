class Queue:
    def __init__(self):
        self.elements = []

    def enqueue(self, value):
        self.elements.append(value)

    def dequeue(self):
        if self.elements:
            item = self.elements[0]
            self.elements = self.elements[1:]
            return item
    
    def notempty(self):
        return len(self.elements) > 0
    
    def __str__(self):
        return str(self.elements)