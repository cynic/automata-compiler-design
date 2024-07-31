import NFA

class DPDA:
  def __init__(self, states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states):
    self.states = states
    self.input_alphabet = input_alphabet
    self.stack_alphabet = stack_alphabet
    self.transitions = transitions
    self.start_state = start_state
    self.start_stack_symbol = start_stack_symbol
    self.accept_states = accept_states
    self.current_state = start_state
    self.stack = [start_stack_symbol]

  def reset(self):
    self.current_state = self.start_state
    self.stack = [self.start_stack_symbol]

  def accepts(self, input_string):
    # print(f"\n*** Checking: {input_string}; starting at {self.current_state}")
    self.__input_string = input_string
    self.__skip = 0
    self.__count = 0
    for symbol in input_string:
      self.__count += 1
      if self.__skip > 0:
        self.__skip -= 1
        # print(f"Skipping: {symbol}")
        continue
      # print(f"Processing: {symbol}, stack = {self.stack}")
      if not self.step(symbol):
        return False
      # print(f"At the end of the step, state = {self.current_state}, stack = {self.stack}")
    # print("Doing any remaining transitions.")
    # There might be an epsilon-transition at the end; check for it
    while (self.current_state in self.transitions and
           None in self.transitions[self.current_state]):
      # If there is such a transition, but I can't follow it, I must reject
      if not self.accept_stack(self.transitions[self.current_state][None]):
        return False
    # print(f"Done with: {input_string}; ended at {self.current_state}")
    return self.current_state in self.accept_states

  def step(self, symbol):
    return self.accept_current_state(symbol)

  def accept_current_state(self, symbol):
    if self.current_state in self.transitions:
      return self.accept_symbol(self.transitions[self.current_state], symbol)
    # else:
    #   print(f"State {self.current_state} not in transitions")
    #   return False

  def accept_symbol(self, symbol_dict, symbol):
    return self.accept_input_symbol(symbol_dict, symbol) or \
           self.accept_epsilon_symbol(symbol_dict, symbol)

  def accept_input_symbol(self, symbol_dict, symbol):
    if symbol in symbol_dict:
      return self.accept_stack(symbol_dict[symbol])

  def accept_epsilon_symbol(self, symbol_dict, symbol):
    if None in symbol_dict:
      # If an epsilon-transition is taken, the original symbol
      # remains valid and must be processed after the epsilon-transition.
      # This is why we call self.step(symbol) afterwards.
      return self.accept_stack(symbol_dict[None]) and \
             self.step(symbol)

  def accept_stack(self, stack_dict):
    if self.stack[-1] in stack_dict:
      to, pushed = stack_dict[self.stack[-1]]
      self.stack.pop()
      return self.transition(to, pushed)
    elif None in stack_dict:
      # The '*' will "unpack" the tuple into arguments.
      return self.transition(*stack_dict[None])
    # else:
    #   # print(f"Symbol {self.stack[-1]} does not match required key {stack_dict.keys()}")
    #   return False

  def transition(self, to, pushed):
    self.current_state = to
    if pushed:
      for sym in pushed:
        # print(f"Pushing: {sym}")
        self.stack.append(sym)

    # We have ended up… somewhere.
    # If we now need to recognize something with a custom recognizer, do it.
    if self.current_state in self.transitions and \
       'recognizer' in self.transitions[self.current_state]:
      # print(f"Using custom recognizer.")
      custom = self.transitions[self.current_state]['recognizer']
      result = custom.accepts(self.__input_string[self.__count-1:])
      if not result:
        # print(f"Rejected by inner recognizer: {input_string[self.__count-1:]}")
        return False
      else:
        self.__skip = custom.accepted_length() - 1
        return True
    else:
      return True

class ArithmeticExpressionRecognizer:
  def __init__(self):
    num_recognizer = NFA.NumberRecognizer()
    states = {'S', 'Operand', 'Open', 'Num', 'Close', 'End'}
    # union of alphabets
    input_alphabet = num_recognizer.nfa.alphabet | {'(', ')'}
    stack_alphabet = {'B', '1'}
    transitions = {
        # From -> Symbol -> Stack -> (To, StackOperation)
        'S':        { None: { None: ('Operand', None ) } },
        'Operand':  { ' ':  { None: ('Operand', None ) },
                      '0':  { None: ('Num'    , None ) },
                      '1':  { None: ('Num'    , None ) },
                      '2':  { None: ('Num'    , None ) },
                      '3':  { None: ('Num'    , None ) },
                      '4':  { None: ('Num'    , None ) },
                      '5':  { None: ('Num'    , None ) },
                      '6':  { None: ('Num'    , None ) },
                      '7':  { None: ('Num'    , None ) },
                      '8':  { None: ('Num'    , None ) },
                      '9':  { None: ('Num'    , None ) },
                      '-':  { None: ('Num'    , None ) },
                      '(':  { None: ('Open'   , ['1']) },
                    },
        'Open':     { ' ':  { None: ('Open'   , None ) },
                      '(':  { None: ('Open'   , ['1']) },
                      '0':  { None: ('Num'    , None ) },
                      '1':  { None: ('Num'    , None ) },
                      '2':  { None: ('Num'    , None ) },
                      '3':  { None: ('Num'    , None ) },
                      '4':  { None: ('Num'    , None ) },
                      '5':  { None: ('Num'    , None ) },
                      '6':  { None: ('Num'    , None ) },
                      '7':  { None: ('Num'    , None ) },
                      '8':  { None: ('Num'    , None ) },
                      '9':  { None: ('Num'    , None ) },
                      '-':  { None: ('Num'    , None ) }
                    },
        'Num':      { None: { 'B':  ('End'    , None ) },
                      '+':  { None: ('Operand', None ) },
                      '-':  { None: ('Operand', None ) },
                      '*':  { None: ('Operand', None ) },
                      '/':  { None: ('Operand', None ) },
                      '%':  { None: ('Operand', None ) },
                      ' ':  { None: ('Close'  , None ) },
                      ')':  { '1':  ('Close'  , None ) },
                      'recognizer': num_recognizer
                    },
        'Close':    { None: { 'B':  ('End'    , None ) },
                      ' ':  { None: ('Close'  , None ) },
                      ')':  { '1':  ('Close'  , None ) },
                      '+':  { None: ('Operand', None ) },
                      '-':  { None: ('Operand', None ) },
                      '*':  { None: ('Operand', None ) },
                      '/':  { None: ('Operand', None ) },
                      '%':  { None: ('Operand', None ) }
                    }
        }
    start_state = 'S'
    start_stack_symbol = 'B'
    accept_states = {'End'}

    # Create DPDA instance
    self.dpda = DPDA(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states)

  def accepts(self, string):
    self.dpda.reset()
    return self.dpda.accepts(string)

# TESTING:
# states = {'q0', 'Add', 'Sub', 'End'}
# input_alphabet = {'(', ')'}
# stack_alphabet = {'B', '1'}
# transitions = {
#     # From -> Symbol -> Stack -> (To, StackOperation)
#     'q0':   { None: { None: ('Add', None)    } },
#     'Add':  { '(':  { None: ('Add', ['1']) },
#               ')':  { '1':  ('Sub', None)  } },
#     'Sub':  { '(':  { None: ('Add', ['1']) },
#               ')':  { '1':  ('Sub', None)  },
#               None: { 'B':  ('End', None)  } }
#     }
# start_state = 'q0'
# start_stack_symbol = 'B'
# accept_states = {'End'}

# # Create DPDA instance
# dpda = DPDA(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states)

# # Test the DPDA
# test_inputs = [
#   "()", "(())", "((()))", "(()())", "()()", "()(())()", "(", "())", "((())",
#   "(()))", "()(", ")(())()", ")", "(()", "(()))", "(()()", ")()", "(())()"
#   ]

# for input_string in test_inputs:
#   dpda.reset()
#   if dpda.accepts(input_string):
#     print(f"{input_string} is accepted.")
#   else:
#     print(f"{input_string} is rejected.")

arithmetic = ArithmeticExpressionRecognizer()
test_inputs = [
  "1",
  "(1)",
  "(1+3)",
  "((2-5)+1-8)",
  "((2-5)+(1-8))",
  "((2-5)+(1-8))*(3)",
  "((2-5)+(1-8)+2)",
  "6+(8-7)+4/(9*0)%2",
  " 6 + ( 8 - 7 ) + 4 / ( 9 * 0 ) % 2 ",
  "  6  +  (  8  -  7  )  +  4  /  (  9  *  0  )  %  2  ",
  "6+((8-7)+4)/9*(0%2))"
  ]
for input_string in test_inputs:
  if arithmetic.accepts(input_string):
    print(f"{input_string} is accepted.")
  else:
    print(f"{input_string} is rejected.")