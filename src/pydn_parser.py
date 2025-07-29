def main() -> int:
  f = open("test.pydn")
  raw_text = f.read()
  #TODO: force commas
  #TODO: comments (both in format and code)
  #TODO: lists
  #TODO: tuples
  #TODO: floats
  #TODO: dicts
  #TODO: bools
  #TODO: None
  #TODO: nan
  #TODO: inf
  parsed = {}
  #dict_stack = []
  
  cur_string = ""
  cur_key = ""
  cur_dict = {}
  is_reading_string = False
  is_adding_keyvalue = False
  is_reading_number = False
  is_reading_dict = False
  #sort of a combined lexer and parser. should be fine for such a simple format.
  for i in range(len(raw_text)):
    char = raw_text[i]
    is_eof = i == len(raw_text) - 1
    
    if is_eof:
      #doing this results in no other special cases, nice!
      next_char = ''
    else:
      next_char = raw_text[i + 1]
      
    if is_reading_string:
      #parsing for strings
      if char == '"':
        is_reading_string = False
        
        if is_adding_keyvalue:
          cur_dict[cur_key] = cur_string
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
        is_adding_keyvalue = True
        
      elif is_numeric_ascii(char):
        cur_string += char
          
        if not is_numeric_ascii(next_char):
          if is_adding_keyvalue:
            try:
              cur_dict[cur_key] = int(cur_string)
              cur_string = ""
              is_adding_keyvalue = False
              
            except ValueError:
              print("number parsing failed")
              return 1
            
          else:
            print("unexpected number found while parsing")
            return 1
            
      elif char == '{':
        is_reading_dict = True
      
      elif char == '}':
        is_reading_dict = False
        parsed = cur_dict
        cur_dict = {}
        
  print(parsed)
  
  f.close()
  return 0

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