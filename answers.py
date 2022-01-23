if __name__ == "__main__":
    with open("words.txt") as file:
        text = file.read()
        words = text.split("\n")

    letters_known_position = {1: '', 2: '', 3: '', 4: '', 5: ''}
    letters_not_in_position = {1: [], 2: [], 3: [], 4: [], 5: []}
    letters_in_word = list(set(
        [letter for letter in letters_known_position.values() if letter] +
        [letter
         for letters in letters_not_in_position.values()
         for letter in letters]
    ))
    letters_not_in_word = []

    def is_possible(word):
        # there's at least one known letter not in word: not possible
        if not all(map(lambda letter: letter in word, letters_in_word)):
            return False
        for i, letter in enumerate(word):
            # letter already known as not in word: not possible
            if letter in letters_not_in_word:
                return False
            # letter already known to not be in this position: not possible
            if letter in letters_not_in_position[i+1]:
                return False
            # letter already known to be different from the right one: not possible
            if letter != letters_known_position[i+1] and letters_known_position[i+1]:
                return False
        # otherwise: possible
        return True

    for word in filter(is_possible, words):
        print(word)
