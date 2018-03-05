import pickle
import random
try:
    file = open("test.pkl", mode="r+b")
    vars = pickle.load(file)
except FileNotFoundError:
    file = open("test.pkl", mode="w+b")
    file = open("test.pkl", mode="r+b")
file = open("test.pkl", mode="w+b")
int = random.randint(0, 100)
str = "String"
float = random.random()
bool = False
vars = [int, str, float, bool]
pickle.dump(vars, file)
