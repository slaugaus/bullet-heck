import pickle
try:
    file = open("../test.pkl", mode="r+b")
    vars = pickle.load(file)
    print(vars)
except FileNotFoundError:
    raise FileNotFoundError("Couldn't find test.pkl! Did you run the launcher?")
