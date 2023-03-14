import csv

import numpy as np

from utils import reduce_sample_space

with open('word_lists/all_words.txt', 'r') as fp1:
    all_words = fp1.read().splitlines()
with open('word_lists/valid_words.txt', 'r') as fp2:
    valid_words = fp2.read().splitlines()
with open('./word_lists/one_step_entropies.csv', 'r') as fp1:
    reader = csv.reader(fp1)
    ranked = dict(reader)


def is_invalid(guess: str) -> bool:
    l, r = 0, len(all_words) - 1
    # 15 = log_2(r) + 1
    for _ in range(15):
        if l > r:
            break
        m = (l + r) // 2
        if all_words[m] == guess:
            return False
        elif guess < all_words[m]:
            r = m - 1
        else:
            l = m + 1
    return True


def main():
    starting_guide = """
Welcome to Wordle Bot!
When the computer asks for a result, input it as 5 separate numbers with a space in between each
0 = grey square
1 = yellow square
2 = green square
eg: ⬛⬛🟩🟨🟨 ("BBGYY") should be inputted as 0 0 2 1 1 in the program
"""
    print(starting_guide)
    print("Start a new game ? (Y/n)")
    flag = input().strip()[0].lower() == 'y'
    if not flag:
        return 0
    wl = list(ranked.keys())
    for i in range(1, 7):
        while True:
            guess = input("Enter guess : ").strip().lower()
            if len(guess) != 5:
                print("Length of word must be 5")
            elif is_invalid(guess):
                print("Not a valid input in Wordle")
            else:
                break
        while True:
            res = list(map(int, input("Enter result : ").strip().split()))
            if len(res) != 5:
                print("Length of result must be 5")
            elif min(res) < 0 or max(res) > 2:
                print("Invalid result")
            else:
                break
        res = np.array(res)
        if np.all(res == 2):
            print("Your guess is the correct answer")
            return 0
        wl = reduce_sample_space(guess, res, wl)
        print(f'Suggested word : {wl[0]}')


if __name__ == "__main__":
    main()
