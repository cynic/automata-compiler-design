class DAWGNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class DAWG:
    def __init__(self):
        self.root = DAWGNode()

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = DAWGNode()
            current = current.children[char]
        current.is_terminal = True

    def build_from_words(self, words):
        for word in words:
            self.insert(word)

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_terminal

    def longest_prefix(self, text):
        current = self.root
        longest_match = ""
        current_match = ""
        for char in text:
            if char in current.children:
                current = current.children[char]
                current_match += char
                if current.is_terminal:
                    longest_match = current_match
            else:
                break
        return longest_match

class KeywordDecider:
    def __init__(self, keywords):
        self.dawg = DAWG()
        self.dawg.build_from_words(keywords)

    def accepts(self, string):
        return self.dawg.search(string)

keywords = ["function", "takes", "num", "if", "else"]
keyword_acceptor = KeywordDecider(keywords)
test_keywords = [
        "function", "hailstone", ":", "num",
        "takes", "initial-value", "look-forward-by", "if"
    ]
results = {w: keyword_acceptor.accepts(w) for w in test_keywords}
for word, result in results.items():
    print(f"Keyword {word} is accepted: {result}")