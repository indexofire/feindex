# -*- coding: utf-8 -*-

def create_secret_key(key_file):
    """
    Create your own django project secret key.
    """
    char = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    try:
        f = open(key_file)
        return f.read().strip()
    except IOError:
        try:
            with open(key_file, 'w') as f:
                f.write(''.join([choice(char) for i in range(50)]))
        except IOError:
            raise Exception('Can not open file `%s` for writing.' % key_file)
    finally:
        if f:
            f.close()
