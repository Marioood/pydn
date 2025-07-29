def main() -> int:
  #TODO: force commas
  #TODO: escape characters
  #TODO: lists
  #TODO: tuples
  #TODO: floats
  #TODO: nan
  #TODO: inf
  #TODO: single quotes
  
  #TODO: comments (both in format and code)
  #TODO: better errors
  #TODO: pass file name for errors ? ? ? ?
  
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
  cur_string = ""
  cur_key = ""
  cur_depth = starting_depth
  parsed = {}
  is_reading_string = False
  is_adding_keyvalue = False
  is_reading_dict = False
  
  #add 1 to the starting idx so we skip the first '{'
  for i in range(starting_idx + 1, len(raw_text)):
    char = raw_text[i]
    is_eof = i == len(raw_text) - 1
    
    if is_eof:
      #doing this results in no other special cases, nice!
      next_char = ''
    else:
      next_char = raw_text[i + 1]
      
    if is_reading_dict:
      #when a dict is nested inside of a dict, we do not want the child dict's data being added to the parent dict
      #skip through parsing text, only making sure to count how deep we are into the child dicts
      if char == '{':
        cur_depth += 1
        
      elif char == '}':
        cur_depth -= 1
        
      if cur_depth == starting_depth:
        print("exit skip mode")
        is_reading_dict = False
      
    elif is_reading_string:
      #parsing for strings
      if char == '"':
        is_reading_string = False
        
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
      if char == '"':
        is_reading_string = True
        
      elif char == ':':
        if is_adding_keyvalue:
          raise SyntaxError("colon found after colon")
          
        is_adding_keyvalue = True
        
      elif is_numeric_ascii(char):
        #parsing for ints (SOON FLOATS)
        #could this be combined with later code??? bool parsing
        cur_string += char
          
        if not is_numeric_ascii(next_char):
          if is_adding_keyvalue:
            try:
              parsed[cur_key] = int(cur_string)
              cur_string = ""
              is_adding_keyvalue = False
              
            except ValueError:
              raise ValueError("number parsing failed")
            
          else:
            raise SyntaxError("unexpected number found while parsing")
            
      elif char == '{':
        #start parsing a new dict (recursively, scary!!!)
        cur_depth += 1
        parsed[cur_key] = parse_pydn_leaf(raw_text, i, cur_depth)
        is_adding_keyvalue = False
        is_reading_dict = True
        
      elif char == '}':
        #return the dict n shit
        print(parsed)
        print("RAW:" + raw_text[starting_idx + 1:] + "-----")
        return parsed
      
      elif char != ' ' and char != '\n' and char != ',':
        #parsing for booleans
        cur_string += char
        
        if cur_string == "True":
          if is_adding_keyvalue:
            parsed[cur_key] = True
            is_adding_keyvalue = False
            cur_string = ""
            
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "False":
          if is_adding_keyvalue:
            parsed[cur_key] = False
            is_adding_keyvalue = False
            cur_string = ""
          
          else:
            raise SyntaxError("unexpected bool found while parsing")
        
        elif cur_string == "None":
          if is_adding_keyvalue:
            parsed[cur_key] = None
            is_adding_keyvalue = False
            cur_string = ""
          
          else:
            raise SyntaxError("unexpected None found while parsing")
      
  raise EOFError("reached end of file in parse_pydn_leaf()")

def is_numeric_ascii(string):
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