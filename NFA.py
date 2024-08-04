import unicodedata

class NFA:
  def __init__(self, states, alphabet, transition_function, start_state, accept_states):
    self.states = states # Q
    self.alphabet = alphabet # Σ
    self.transition_function = transition_function # δ = (q, σ, {q'})
    self.start_state = start_state # q0
    self.accept_states = accept_states # F
    self.accepted_length = 0;

  def accepts(self, input_string, verbose=False):
    current_states = {self.start_state}
    self.accepted_length = 0;
    for symbol in input_string:
      if not (symbol in self.alphabet):
        if verbose:
          print(f"Ending recognition: did not find {symbol} in alphabet")
        return any(state in self.accept_states for state in current_states)
      next_states = set()
      if verbose:
        print(f"Current states: {current_states}")
        print(f"Symbol: {symbol}")
      for state in current_states:
        if (state, symbol) in self.transition_function:
          next_states.update(self.transition_function[(state, symbol)])
        elif (state, None) in self.transition_function:
          next_states.update(self.transition_function[(state, None)])
        else:
          if verbose:
            print(f"Ending recognition: no valid transition involving {symbol}")
          return any(state in self.accept_states for state in current_states)
      self.accepted_length += 1
      if verbose:
        print(f"Next states: {next_states}")
        print("----")
      current_states = next_states
    if verbose:
      print(f"Done with: {input_string}\n")
    return any(state in self.accept_states for state in current_states)

class StringRecognizer:
  def __init__(self):
    # Define the NFA for recognizing strings
    states = {'S', 'Q', 'ESC', 'ACC'}
    alphabet = set(chr(i) for i in range(0x110000)
                   if len(unicodedata.name(chr(i), "")) > 0
                      and unicodedata.category(chr(i)) != 'Cc'
                  )
    transition_function = {
      ('S', '"'): {'Q'},
      ('Q', '\\'): {'ESC'},
      ('ESC', '"'): {'Q'},
      ('ESC', '\\'): {'Q'},
      ('Q', '"'): {'ACC'}
    }
    # Add transitions for all printable characters except " and \
    for char in alphabet - {'"', '\\'}:
      transition_function[('Q', char)] = {'Q'}

    start_state = 'S'
    accept_states = {'ACC'}

    self.nfa = NFA(states, alphabet, transition_function, start_state, accept_states)

  def accepts(self, string):
    return self.nfa.accepts(string)

  def accepted_length(self):
    return self.nfa.accepted_length

class IdentifierRecognizer:
  def __init__(self):
    # Define the NFA for recognizing strings
    states = {'S', 'Mid', 'End'}
    alphabet = set(chr(i) for i in range(0x110000)
                   if len(unicodedata.name(chr(i), "")) > 0
                      and unicodedata.category(chr(i)) not in ['Cc', 'Zl', 'Zp', 'Zs']
                  )
    only_letters = set(chr(i) for i in range(0x110000)
                   if len(unicodedata.name(chr(i), "")) > 0
                      and unicodedata.category(chr(i)) in ['Ll', 'Lm', 'Lo', 'Lt', 'Lu']
                  )
    transition_function = { }
    # Add transitions so that we end 
    for char in only_letters:
      transition_function[('S', char)] = {'End'}
      transition_function[('Mid', char)] = {'End'}
      transition_function[('End', char)] = {'End'}
    for char in alphabet - only_letters:
      transition_function[('End', char)] = {'Mid'}
      transition_function[('Mid', char)] = {'Mid'}

    start_state = 'S'
    accept_states = {'End'}

    self.nfa = NFA(states, alphabet, transition_function, start_state, accept_states)
    
  def accepts(self, string):
    return self.nfa.accepts(string)

  def accepted_length(self):
    return self.nfa.accepted_length

class NumberRecognizer:
  def __init__(self):
    states = {'S', 'Sign', 'Pre' 'Int', 'Frac', 'Zero', 'Digit', 'FracDigit', 'Trailing'}
    alphabet = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-'}
    transition_function = {
      ('S', '1'): {'Int'},
      ('S', '2'): {'Int'},
      ('S', '3'): {'Int'},
      ('S', '4'): {'Int'},
      ('S', '5'): {'Int'},
      ('S', '6'): {'Int'},
      ('S', '7'): {'Int'},
      ('S', '8'): {'Int'},
      ('S', '9'): {'Int'},
      ('S', '-'): {'Sign'},
      ('S', '+'): {'Sign'},
      ('S', '0'): {'Zero'},
      ('Sign', '1'): {'Int'},
      ('Sign', '2'): {'Int'},
      ('Sign', '3'): {'Int'},
      ('Sign', '4'): {'Int'},
      ('Sign', '5'): {'Int'},
      ('Sign', '6'): {'Int'},
      ('Sign', '7'): {'Int'},
      ('Sign', '8'): {'Int'},
      ('Sign', '9'): {'Int'},
      ('Sign', '0'): {'Pre'},
      ('Pre', '.'): {'Frac'},
      ('Int', '.'): {'Frac'},
      ('Int', '1'): {'Digit'},
      ('Int', '2'): {'Digit'},
      ('Int', '3'): {'Digit'},
      ('Int', '4'): {'Digit'},
      ('Int', '5'): {'Digit'},
      ('Int', '6'): {'Digit'},
      ('Int', '7'): {'Digit'},
      ('Int', '8'): {'Digit'},
      ('Int', '9'): {'Digit'},
      ('Int', '0'): {'Digit'},
      ('Digit', '0'): {'Digit'},
      ('Digit', '1'): {'Digit'},
      ('Digit', '2'): {'Digit'},
      ('Digit', '3'): {'Digit'},
      ('Digit', '4'): {'Digit'},
      ('Digit', '5'): {'Digit'},
      ('Digit', '6'): {'Digit'},
      ('Digit', '7'): {'Digit'},
      ('Digit', '8'): {'Digit'},
      ('Digit', '9'): {'Digit'},
      ('Digit', '.'): {'Frac'},
      ('Frac', '1'): {'FracDigit'},
      ('Frac', '2'): {'FracDigit'},
      ('Frac', '3'): {'FracDigit'},
      ('Frac', '4'): {'FracDigit'},
      ('Frac', '5'): {'FracDigit'},
      ('Frac', '6'): {'FracDigit'},
      ('Frac', '7'): {'FracDigit'},
      ('Frac', '8'): {'FracDigit'},
      ('Frac', '9'): {'FracDigit'},
      ('Frac', '0'): {'Trailing'},
      ('FracDigit', '1'): {'FracDigit'},
      ('FracDigit', '2'): {'FracDigit'},
      ('FracDigit', '3'): {'FracDigit'},
      ('FracDigit', '4'): {'FracDigit'},
      ('FracDigit', '5'): {'FracDigit'},
      ('FracDigit', '6'): {'FracDigit'},
      ('FracDigit', '7'): {'FracDigit'},
      ('FracDigit', '8'): {'FracDigit'},
      ('FracDigit', '9'): {'FracDigit'},
      ('FracDigit', '0'): {'Trailing'},
      ('Trailing', '0'): {'Trailing'},
      ('Trailing', '1'): {'FracDigit'},
      ('Trailing', '2'): {'FracDigit'},
      ('Trailing', '3'): {'FracDigit'},
      ('Trailing', '4'): {'FracDigit'},
      ('Trailing', '5'): {'FracDigit'},
      ('Trailing', '6'): {'FracDigit'},
      ('Trailing', '7'): {'FracDigit'},
      ('Trailing', '8'): {'FracDigit'},
      ('Trailing', '9'): {'FracDigit'},
      ('Zero', '.'): {'Frac'}
    }
    start_state = 'S'
    accept_states = {'Int', 'FracDigit', 'Digit', 'Zero'}

    self.nfa = NFA(states, alphabet, transition_function, start_state, accept_states)

  def accepts(self, string):
    return self.nfa.accepts(string)

  def accepted_length(self):
    return self.nfa.accepted_length

# USAGE / TESTING:
# string_acceptor = StringRecognizer()
# test_strings = [
#   '"hello"', '"he said \\"hello\\""', '"escaped \\" quote"',
#   '"\\""', '"\\\\"', 'invalid', 'another "invalid" test',
#   '"Vعry 🥳 vαlid!"'
#   ]
# results = {string: string_acceptor.accepts(string) for string in test_strings}

# # Output results
# for string, result in results.items():
#   print(f"String {string} is accepted: {result}")

# # (45 * (3 + 2) - (54 + 2)) / 2

# num_acceptor = NumberRecognizer()
# # Test number
# test_nums = ['0', '1', '123', '+123', '-123', '+0', '-0', '+', '-', '0', '123.45', '123.450', '0123', '.45', '34.', '34.056', '304.56']
# results = {num: (True, num_acceptor.accepted_length()) if num_acceptor.accepts(num) else (False, None) for num in test_nums}

# # Output results
# for num, result in results.items():
#   print(f"Number {num} is accepted: {result[0]}, accepted length = {result[1]}")