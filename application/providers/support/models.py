class Metric:
    def __init__(self, name, value, labels={}):
        self.name = name
        self.labels = labels
        self.value = value
    
    def to_prometheus(self):
        labels = ', '.join([f"{key}=\"{val}\"" for key, val in self.labels.items()])
        return f"{self.name}{{{labels}}} {self.value}"
