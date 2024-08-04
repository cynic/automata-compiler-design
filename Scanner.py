import NFA
import DAWG
from enum import Enum

Token = Enum("Token", "FUNCTION IDENTIFIER BOOL_RELATION VALUE TYPE_SPECIFIER IF ELSE PARAMLIST ASSIGN COLON COMPARE BODY_OPEN BODY_CLOSE GROUP_OPEN GROUP_CLOSE OPERATOR".split())
TokenMeta = Enum("TokenMeta", "STRING NUMBER BOOLEAN AND OR EQUAL NOT_EQUAL LESS_OR_EQUAL GREATER_OR_EQUAL LESS_THAN GREATER_THAN MULTIPLY ADD SUBTRACT DIVIDE REMAINDER".split())
Space = Enum("Space", "IGNORED WANTED".split())

class KeywordTokenizer:
  def __init__(self, words):
    self.__data = words
    self.dawg = DAWG.DAWG(list(words.keys()))
    
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
    
class RecognizerToTokenizer:
  def __init__(self, recognizer, token, extract):
    self.__recognizer = recognizer
    self.__token = token
    self.__extract = extract
    
  def accepts(self, text):
    self.__accepted_length = 0
    if self.__recognizer.accepts(text):
      self.__accepted_length = self.__recognizer.accepted_length()
      if self.__extract:
        self.__extra = self.__extract(text[:self.__accepted_length])
      else:
        self.__extra = None
      return True
    
  def accepted_length(self):
    return self.__accepted_length
  
  def token(self):
    return self.__token
  
  def extra(self):
    return self.__extra
    
class Scanner:
  def __init__(self):
    # in order from MOST to LEAST specific
    self.tokenizers = \
      [ KeywordTokenizer(
            { "function": (Token.FUNCTION      , Space.WANTED  , None ),
              "string":   (Token.TYPE_SPECIFIER, Space.WANTED  , lambda x: {'kind': TokenMeta.STRING} ),
              "num":      (Token.TYPE_SPECIFIER, Space.WANTED  , lambda x: {'kind': TokenMeta.NUMBER} ),
              "bool":     (Token.TYPE_SPECIFIER, Space.WANTED  , lambda x: {'kind': TokenMeta.BOOLEAN} ),
              "if":       (Token.IF            , Space.WANTED  , None ),
              "else":     (Token.ELSE          , Space.WANTED  , None ),
              "takes":    (Token.PARAMLIST     , Space.WANTED  , None ),
              "or":       (Token.BOOL_RELATION , Space.WANTED  , lambda x: {'relation': TokenMeta.OR} ),
              "and":      (Token.BOOL_RELATION , Space.WANTED  , lambda x: {'relation': TokenMeta.AND} ),
              ":=":       (Token.ASSIGN        , Space.IGNORED , None ),
              ":":        (Token.COLON         , Space.IGNORED , None ),
              "=":        (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.EQUAL} ),
              "!=":       (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.NOT_EQUAL} ),
              "<=":       (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.LESS_OR_EQUAL} ),
              ">=":       (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.GREATER_OR_EQUAL} ),
              "<":        (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.LESS_THAN} ),
              ">":        (Token.COMPARE       , Space.IGNORED , lambda x: {'cmp': TokenMeta.GREATER_THAN} ),
              "{":        (Token.BODY_OPEN     , Space.IGNORED , None ),
              "}":        (Token.BODY_CLOSE    , Space.IGNORED , None ),
              "(":        (Token.GROUP_OPEN    , Space.IGNORED , None ),
              ")":        (Token.GROUP_CLOSE   , Space.IGNORED , None ),
              "*":        (Token.OPERATOR      , Space.IGNORED , lambda x: {'op': TokenMeta.MULTIPLY} ),
              "+":        (Token.OPERATOR      , Space.IGNORED , lambda x: {'op': TokenMeta.ADD} ),
              "-":        (Token.OPERATOR      , Space.IGNORED , lambda x: {'op': TokenMeta.SUBTRACT} ),
              "/":        (Token.OPERATOR      , Space.IGNORED , lambda x: {'op': TokenMeta.DIVIDE} ),
              "%":        (Token.OPERATOR      , Space.IGNORED , lambda x: {'op': TokenMeta.REMAINDER} ),
              "true":     (Token.VALUE         , Space.WANTED  , lambda x: {'kind': TokenMeta.BOOLEAN, 'value': True} ),
              "false":    (Token.VALUE         , Space.WANTED  , lambda x: {'kind': TokenMeta.BOOLEAN, 'value': False} )
            })
      , RecognizerToTokenizer(NFA.StringRecognizer()    , Token.VALUE    , lambda x: {'kind': TokenMeta.STRING, 'value': x} )
      , RecognizerToTokenizer(NFA.NumberRecognizer()    , Token.VALUE    , lambda x: {'kind': TokenMeta.NUMBER, 'value': int(x)} )
      , RecognizerToTokenizer(NFA.IdentifierRecognizer(), Token.IDENTIFIER, lambda x: {'text': x})
      ]
      
  def ellipsis(self, text):
    if len(text) < 15:
      return text
    else:
      return text[:14] + '...'
      
  def scan(self, text):
    tokens = []
    col = 1
    line = 1
    while len(text) > 0:
      if text[0] in [" ", "\n"]:
        if text[0] == "\n":
          line += 1
          col = 1
        else:
          col += 1
        text = text[1:]
        continue
      
      for tokenizer in self.tokenizers:
        if tokenizer.accepts(text):
          datum = \
            { 'token': tokenizer.token()
            , 'line': line
            , 'start': col
            , 'end': col + tokenizer.accepted_length() - 1
            } | ( tokenizer.extra() or {} )
          tokens.append(datum)
          col += tokenizer.accepted_length()
          text = text[tokenizer.accepted_length():]
          break
      else:
        print(f"Unexpected text '{self.ellipsis(text)}' at line {line} column {col}")
        return []
    return tokens
  
# Testing!
with open('test0.pal') as f: a = f.read()
s = Scanner()
print(f'Parsing "{a}"\n', s.scan(a))