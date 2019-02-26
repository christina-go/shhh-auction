from app import ALLOWED_EXTENSIONS

def text_len(text):
  textLength = len(text)

  if textLength < 3:
    return False

  else:
    return True

def no_spaces(text):
  
  if ' ' in text:
    return False
  else:
    return True


def input_validation(input):
    
  if text_len(input) and no_spaces(input) == True:
      
    return True
  else:
  
    return False
    
def password_match(password, passwordConfirmation):
    if passwordConfirmation == '':
        return False 
    
    elif password == passwordConfirmation:
        return True   

    else:
        return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  