import numpy as np
import pickle


class Model:

    def __init__(self, prefix_len = 2) -> None:
        self.nxt: dict[str, dict[str, int]] = dict()
        self.prefix_len = prefix_len
    
    def get_next(self, n_gramm: list[str]) -> str:
        for i in range(len(n_gramm) + 1):
            prev = ' '.join(n_gramm[i:])
            if prev not in self.nxt.keys() or not len(self.nxt[prev]): continue

            p = np.array(list(self.nxt[prev].values()))
            # for t in range(i): n_gramm.pop(0)
            return np.random.choice(list(self.nxt[prev].keys()), p=p/p.sum())
    
    def fit(self, n_gramm: list[str], word: str) -> None:
        for i in range(len(n_gramm) + 1):
            prev = ' '.join(n_gramm[i:])
            if prev not in self.nxt.keys():
                self.nxt[prev] = dict()
            if word not in self.nxt[prev].keys():
                self.nxt[prev][word] = 0
            self.nxt[prev][word] += 1


def save(path: str, model: Model) -> None:
    try:
        with open(path, "wb") as f:
            pickle.dump(model, f)
    except:
        print("Can't open save path.")


def load(path: str) -> Model:
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except:
        print("Can't load model file.")
        return None
