from loaders import InstanceLoader

loader = InstanceLoader()

instance = loader.load("./instances/ali535.tsp")

print(instance.dimension)
print(instance.vertices[4])
