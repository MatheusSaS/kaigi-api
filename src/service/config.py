modo = 'teste'

def domain():
    
    if modo == 'teste':
        return 'http://127.0.0.1:5173/'
    else:
        return ''

def urlapi():

    if modo == 'teste':
        return 'sk_test_51LpCQ1ER7RGDPAz0TIUvMc7l8AU8bwA0dByAQfxfX0ZtOWQ7joPv0OMrHQ5nLqaqyOSff9xwEM9bAD9tEMfIA2Pe00IHFavsEb'
    else:
        return ''
