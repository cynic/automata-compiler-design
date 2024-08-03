class DAWGNode:
  def __init__(self):
    self.children = {}
    self.is_terminal = False

class DAWG:
  def __init__(self, words):
    self.root = DAWGNode()
    self.build_from_words(words)

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
            
  def accepts(self, text):
    current = self.root
    longest_match = ""
    current_match = ""
    self.__accepted_length = 0
    for char in text:
      if char in current.children:
        current = current.children[char]
        current_match += char
        if current.is_terminal:
          # print(f'matched: "{current_match}"')
          longest_match = current_match
          self.__accepted_length = len(current_match)
      else:
        break
    if len(longest_match) > 0:
      return True
    return False
    
  def accepted_length(self):
    return self.__accepted_length

class KeywordAndTokenRecognizer:
  def __init__(self, words):
    self.dawg = DAWG(list(words))

  def accepts(self, string):
    return self.dawg.accepts(string)
    
  def accepted_length(self):
    return self.dawg.accepted_length()

keywords = {"function", "takes", "num", "bool", "if", "else"}
tokens = {":", "<", ">", "=", "<=", ">=", ":=", "{", "}", "(", ")"}
keyword_acceptor = KeywordAndTokenRecognizer(keywords | tokens)
test_keywords = [
  "function", "hailstone", ":", "num",
  "takes", "initial-value", "look-forward-by", "if"
]
results = {w: keyword_acceptor.accepts(w) for w in test_keywords}
for word, result in results.items():
  print(f"Keyword {word} is accepted: {result}")