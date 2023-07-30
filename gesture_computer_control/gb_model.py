import pickle

model = pickle.load(open("pima.pickle.dat", "rb"))
def pred (X):
    return model.predict(X)
