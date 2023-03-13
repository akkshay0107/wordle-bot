import csv

import numpy as np

from utils import simulate_guess, mask


def get_entropies() -> dict:
    with open('word_lists/valid_words.txt', 'r') as fp1:
        all_words = fp1.read().splitlines()
    # all_words = all_words[:100]
    N = len(all_words)
    one_step_entropy = dict()
    for i, g in enumerate(all_words):
        prob = np.zeros((243,), dtype='f8')
        for a in all_words:
            res = simulate_guess(g, a)
            idx = mask(res)
            prob[idx] += 1
        prob = prob / N
        partials = prob * (-np.log2(prob, out=np.zeros_like(prob), where=(prob != 0)))
        one_step_entropy[g] = np.sum(partials)
        print(f'{i}/{N}')
    return one_step_entropy


if __name__ == "__main__":
    entropies = get_entropies()
    ranked = dict(sorted(entropies.items(), key=lambda item: item[1], reverse=True))
    # print(entropies)
    with open('word_lists/one_step_entropies.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        for k, v in ranked.items():
            writer.writerow([k, v])
