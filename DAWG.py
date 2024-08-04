from enum import Enum
Space = Enum("Space", "IGNORED WANTED".split())

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

class KeywordAndPunctuationRecognizer:
  def __init__(self, words):
    self.dawg = DAWG(list(words))

  def accepts(self, string):
    return self.dawg.accepts(string)
    
  def accepted_length(self):
    return self.dawg.accepted_length()

class KeywordAndPunctuationTokenizer:
  def __init__(self, words):
    self.__data = words
    self.dawg = DAWG(list(words.keys()))
    
  def accepts(self, text):
    self.__accepted_length = 0
    if self.dawg.accepts(text):
      word = text[:self.dawg.accepted_length()]
      # print(f'accepted: "{word}"')
      (tok, space, extract) = self.__data[word]
      space_ignored = space == Space.IGNORED
      if len(text) == len(word) or space_ignored or text[len(word)] in [" ", "\n", ")"]:
        self.__accepted_length = len(word)
        self.__token = tok
        if extract:
          self.__extra = extract(word)
        else:
          self.__extra = None
        return True
      
  def accepted_length(self):
    return self.__accepted_length
  
  def token(self):
    return self.__token
  
  def extra(self):
    return self.__extra

# keywords = {"function", "takes", "num", "bool", "if", "else"}
# tokens = {":", "<", ">", "=", "<=", ">=", ":=", "{", "}", "(", ")"}
# keyword_acceptor = KeywordAndTokenRecognizer(keywords | tokens)
# test_keywords = [
#   "function", "hailstone", ":", "num",
#   "takes", "initial-value", "look-forward-by", "if"
# ]
# results = {w: keyword_acceptor.accepts(w) for w in test_keywords}
# for word, result in results.items():
#   print(f"Keyword {word} is accepted: {result}")