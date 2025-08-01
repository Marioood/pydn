import math

def main() -> int:
  #maybe??????
  #TODO: complex numbers
  #TODO: sets
  #TODO: data skeletons, to verify that the data is correct
  
  #definitely do
  #TODO: force commas
  #TODO: escape characters
  #TODO: tuples
  #TODO: single quotes
  
  #TODO: better errors
  #TODO: pass file name for errors ? ? ? ?
  #TODO: whitespace errors.... arise from starting end points spaces tabs
  
  #REMINDER: comments (for the code)
  #REMINDER: this is gonna be a module; functions will look like pydn.function()
  """
  { -- 0 (ROOT)
    dict1 { -- 1
      dict2 { -- 2
        dict3 { -- 3
          shit here
        }
      }
      dict4 { -- 2
        other shit here
      }
    }
  }
  """
  
  f = open("test.pydn")
  raw_text = f.read()
  parse_pydn_leaf(raw_text, 0, 0)
  
  f.close()
  return 0

def parse_pydn_leaf(raw_text, starting_idx, starting_depth) -> dict:
  #sort of a combined lexer and parser. should be fine for such a simple format.
  cur_depth = starting_depth
  cur_string = ""
  cur_key = ""
  parsed = {}
  #yknow... the dict parsing could also be rewritten to use a stack
  #parse lists using a stack. top of the stack contains the parent list, later indices are the children of the parent/the parent's children
  list_stack = []
  cur_list_idx = -1
  is_reading_string = False
  is_adding_keyvalue = False
  is_reading_another_dict = False
  is_reading_list = False
  is_reading_comment = False
  is_reading_float = False
  
  #add 1 to the starting idx so we skip the first '{'
  for i in range(starting_idx + 1, len(raw_text)):
    char = raw_text[i]
    is_eof = i == len(raw_text) - 1
    
    if is_eof:
      #doing this results in no other special cases, nice!
      next_char = ''
    else:
      next_char = raw_text[i + 1]
      
    #parsing with individual characters
    if is_reading_comment:
      if char == '\n':
        is_reading_comment = False
      
    elif is_reading_another_dict:
      #when a dict is nested inside of a dict, we do not want the child dict's data being added to the parent dict
      #skip through parsing text, only making sure to count how deep we are into the child dicts
      if char == '{':
        cur_depth += 1
        
      elif char == '}':
        cur_depth -= 1
        
      if cur_depth == starting_depth:
        print("exit skip mode")
        is_reading_another_dict = False
      
    elif is_reading_string:
      #parsing for strings
      if char == '"':
        is_reading_string = False
        if is_reading_list:
          list_stack[cur_list_idx].append(cur_string)
          
        else:
          if is_adding_keyvalue:
            parsed[cur_key] = cur_string
            is_adding_keyvalue = False
            
          else:
            cur_key = cur_string
          
        cur_string = ""
        
      else:
        cur_string += char
    
    else:
      #parsing in whitespace
      if char == '#':
        is_reading_comment = True
      
      elif char == '"':
        is_reading_string = True
        
      elif char == ':':
        if is_adding_keyvalue:
          raise SyntaxError("PYDN parsing error: colon found after colon")
          
        is_adding_keyvalue = True
        
      elif is_numeral_ascii(char) or (char == '-' and is_numeral_ascii(next_char)):
        #parsing for ints and floats
        #could this be combined with later code??? bool parsing
        #TODO: check with commas or something
        cur_string += char
          

        if next_char == '.' or next_char == 'e' or next_char == '+':
          is_reading_float = True
          
        elif not is_numeral_ascii(next_char):
          if is_reading_float:
            is_reading_float = False
            
            if is_adding_keyvalue:
              try:
                if is_reading_list:
                  list_stack[cur_list_idx].append(float(cur_string))
                  
                else:
                  parsed[cur_key] = float(cur_string)
                  is_adding_keyvalue = False
                  
                cur_string = ""
              
              except ValueError:
                raise ValueError("float parsing failed")
              
            else:
              raise SyntaxError("unexpected float found while parsing")
          
          else:
            #reading int
            if is_adding_keyvalue:
              try:
                if is_reading_list:
                  list_stack[cur_list_idx].append(int(cur_string))
                  
                else:
                  parsed[cur_key] = int(cur_string)
                  is_adding_keyvalue = False
                  
                cur_string = ""
              
              except ValueError:
                raise ValueError("int parsing failed at {}".format(i))
              
            else:
              raise SyntaxError("unexpected int found while parsing")
        
      elif char == '{':
        #start parsing a new dict (recursively, scary!!!)
        cur_depth += 1
        is_reading_another_dict = True
        if is_reading_list:
          list_stack[cur_list_idx].append(parse_pydn_leaf(raw_text, i, cur_depth))
          
        else:
          parsed[cur_key] = parse_pydn_leaf(raw_text, i, cur_depth)
          is_adding_keyvalue = False
        
      elif char == '}':
        #return the dict n shit
        print(parsed)
        print("RAW:" + raw_text[starting_idx + 1:] + "-----")
        return parsed
        
      elif char == '[':
        list_stack.append([])
        cur_list_idx += 1
        is_reading_list = True
        
      elif char == ']':
        cur_list_idx -= 1
        
        if cur_list_idx < 0:
          is_reading_list = False
          is_adding_keyvalue = False
          parsed[cur_key] = list_stack.pop()
          
        else:
          list_stack[cur_list_idx].append(list_stack.pop())
        
      elif char != ' ' and char != '\n' and char != ',':
        #parsing for booleans, None, inf, -inf and nan
        cur_string += char
        
        if cur_string == "True":
          if is_adding_keyvalue:
            parsed[cur_key] = True
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(True)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "False":
          if is_adding_keyvalue:
            parsed[cur_key] = False
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(False)
            cur_string = ""
          
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "None":
          if is_adding_keyvalue:
            parsed[cur_key] = None
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(None)
            cur_string = ""
            
        elif cur_string == "inf":
          if is_adding_keyvalue:
            parsed[cur_key] = math.inf
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(math.inf)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected inf found while parsing")
            
        elif cur_string == "-inf":
          if is_adding_keyvalue:
            parsed[cur_key] = -math.inf
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(-math.inf)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected -inf found while parsing")
            
        elif cur_string == "nan":
          if is_adding_keyvalue:
            parsed[cur_key] = math.nan
            is_adding_keyvalue = False
            cur_string = ""
            
          elif is_reading_list:
            list_stack[cur_list_idx].append(math.nan)
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected nan found while parsing")
      
  raise EOFError("reached end of file in parse_pydn_leaf()")

def encode(raw_dict) -> str:
  #leave comment at the top of the output?
  raise NotImplementedError()
#  for key in raw_dict:

def is_numeral_ascii(string):
  #the vanilla isnumeric() counts weird unicode characters (like exponent signs) as numerals for some reason.
  #this function only counts the ascii 0-9 numerals as numeric.
  for char in string:
    #why do they have to murder chars in every programming language? god, i love chars in C.
    #there's none of this conversion bullshit in C when you want to check/parse numeric text. you just type char - '0'.
    char_codepoint = ord(char)
    
    if not (char_codepoint >= ord('0') and char_codepoint <= ord('9')):
      return False
      
  return True

if __name__ == "__main__":
  error = main()
  
  print("")
  if error == 0:
    print("main successfully executed")
    
  else:
    print("main failed with error code {}".format(error))