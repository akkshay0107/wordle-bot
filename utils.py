from collections import Counter

import numpy as np


def simulate_guess(guess: str, answer: str) -> np.ndarray:
    result = np.ndarray((5,), dtype='u1')
    a_count = Counter(answer)
    left_to_check = []
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = 2
            a_count[guess[i]] -= 1
        else:
            left_to_check.append(i)
    for i in left_to_check:
        if a_count[guess[i]] != 0:
            result[i] = 1
            a_count[guess[i]] -= 1
        else:
            result[i] = 0
    return result


def reduce_sample_space(guess, result, wl) -> list[str]:
    exact_matches = []
    char_matches = []
    for i, x in enumerate(result):
        if x == 2:
            exact_matches.append(i)
        elif x == 1:
            char_matches.append(i)
    words_to_be_removed = set()
    # remove words that are not exact matches
    for idx in exact_matches:
        for word in wl:
            if word[idx] != guess[idx]:
                words_to_be_removed.add(word)
    filtered_wl = [word for word in wl if word not in words_to_be_removed]
    # remove words that don't satisfy the non matches
    gchars = {c: 0 for c in guess}
    for i in exact_matches:
        gchars[guess[i]] += 1
    for i in char_matches:
        gchars[guess[i]] += 1
    for word in filtered_wl:
        wc = Counter(word)
        for i, c in enumerate(guess):
            if gchars[c] == 0 and wc[c] != 0:
                words_to_be_removed.add(word)
            elif gchars[c] != 0 and wc[c] < gchars[c]:
                words_to_be_removed.add(word)
    second_filter = [word for word in filtered_wl if word not in words_to_be_removed]
    # remove words that are off by location
    for idx in char_matches:
        for word in second_filter:
            if guess[idx] == word[idx]:
                words_to_be_removed.add(word)
    reduced_possibilities = [word for word in second_filter if word not in words_to_be_removed]
    return reduced_possibilities


def mask(res: np.ndarray) -> int:
    m = 0
    for i, x in enumerate(res):
        m += x * (3 ** i)
    return m


def inv_mask(mask: int) -> np.ndarray:
    if mask == 0:
        return np.zeros((5,), dtype='u1')
    inv = np.ndarray((5,), dtype='u1')
    j = 0
    while mask:
        mask, r = divmod(mask, 3)
        inv[j] = r
        j += 1
    for _ in range(j, 5):
        inv[_] = 0
    return inv
