class RMI_Registry:
    def __init__(self):
        self.registry = {}
    
    def rebind(self, name, obj):
        if obj not in self.registry.values():
            raise ValueError("Remote object not already in registry")
        self.registry[name] = obj

    def bind(self, name, obj):
        self.registry[name] = obj

    def unbind(self, name):
        self.registry.pop(name, None)

    def lookup(self, name):
        return self.registry[name]

    def list_objects(self):
        return self.registry.keys()
    