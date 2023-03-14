import csv
import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import simulate_guess, reduce_sample_space

with open('./word_lists/one_step_entropies.csv', 'r') as fp1:
    reader = csv.reader(fp1)
    ranked = dict(reader)
with open('./word_lists/valid_words.txt', 'r') as fp2:
    all_words = fp2.read().splitlines()


def simul_random() -> int:
    ans = random.choice(all_words)
    wl = list(ranked.keys())
    for cnt in range(1, 7):
        guess = wl[0]
        res = simulate_guess(guess, ans)
        if np.all(res == 2):
            return cnt
        wl = reduce_sample_space(guess, res, wl)
    return 7

def simul_sequential(ans:str) -> int:
    wl = list(ranked.keys())
    for cnt in range(1, 7):
        guess = wl[0]
        res = simulate_guess(guess, ans)
        if np.all(res == 2):
            return cnt
        wl = reduce_sample_space(guess, res, wl)
    return 7

def plot_results_random(n: int):
    data = []
    for i in range(n):
        score = simul_random()
        if score == 7:
            continue
        data.append(score)
    failure_rate = 1 - len(data) / n
    data = np.array(data)
    mu = np.mean(data)
    stddev = np.std(data)
    print(f'Mean Score = {mu}')
    print(f'Standard Deviation = {stddev}')
    print(f'Failure rate = {failure_rate * 100}%')
    unique, counts = np.unique(data, return_counts=True)
    sns.barplot(x=unique, y=counts, color="#94c0e0", width=0.98)
    plt.axvline(x=mu - 1, linestyle='--')
    plt.xlabel("Number of attempts")
    plt.ylabel("Count")
    plt.show()

def plot_results_sequential():
    data = []
    for word in all_words:
        score = simul_sequential(word)
        if score == 7:
            continue
        data.append(score)
    failure_rate = 1 - len(data) / len(all_words)
    data = np.array(data)
    mu = np.mean(data)
    stddev = np.std(data)
    print(f'Mean Score = {mu}')
    print(f'Standard Deviation = {stddev}')
    print(f'Failure rate = {failure_rate * 100}%')
    unique, counts = np.unique(data, return_counts=True)
    sns.barplot(x=unique, y=counts, color="#94c0e0", width=0.98)
    plt.axvline(x=mu - 1, linestyle='--')
    plt.xlabel("Number of attempts")
    plt.ylabel("Count")
    plt.show()


if __name__ == "__main__":
    plot_results_random(15000)
    #plot_results_sequential()
