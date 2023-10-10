from random import random
import pandas as pd
import numpy as np


def stoch_sir(XYZ, N, tend, beta, gamma, mu):
    # Columns: SIR, Rows: Events [infect, recovery, birth, death S, death I, death R]
    change_matrix = np.array(
        [[-1, 1, 0],
         [0, -1, 1],
         [1,  0, 0],
         [-1, 0, 0],
         [0, -1, 0],
         [0,  0, -1]
         ])
    current_t = 0
    ts = 0.1
    T = [0]
    S = [XYZ[0]]
    I = [XYZ[1]]
    R = [XYZ[2]]

    while T[current_t] < tend:
        T.append(T[-1] + ts)
        S.append(XYZ[0])
        I.append(XYZ[1])
        R.append(XYZ[2])

        event_rates = ([(beta * XYZ[0] * XYZ[1])/N, gamma * XYZ[1],
                        mu * N,  mu * XYZ[0], mu * XYZ[1], mu * XYZ[2]])

        rand_1 = random()
        rand_2 = random()
        ts = -np.log(rand_1)/(np.sum(event_rates))

        p = rand_2 * np.sum(event_rates)
        event_index = min(np.nonzero(np.ravel(np.cumsum(event_rates) >= p))[0])

        XYZ = XYZ + change_matrix[event_index, :]

        current_t = current_t + 1
    return [T, S, I, R]


def run_simulations(number_of_runs, name, param, kwargs):
    seed = np.random.get_state()
    for i in range(number_of_runs):
        with open(f"seeds/seed{name}{i}", "w") as f:
            f.write(str(seed))
        df = pd.DataFrame(stoch_sir(**kwargs)).transpose()
        df.columns = ["T", "S", "I", "R"]
        df.to_csv(
            f"seeddata/{name.capitalize()}{param:.2f}stochasticSIR{i+1}.csv", index=False)

runs = 100
# Varying Beta
for beta in np.linspace(0, 4, 20):
    XYZ = np.array((10000, 1, 0))
    run_simulations(runs, "beta", beta,
                    {"XYZ": XYZ,
                     "N": np.sum(XYZ),
                     "tend": 365,
                     "beta": beta,
                     "gamma": 1/14,
                     "mu": 1/200})

