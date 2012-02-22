# -*- coding: utf-8 -*-
from random import choice


char = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

def create_secret_key(key_file, char=char):
    """
    Create your own django project secret key.
    """

    try:
        f = open(key_file)
        key = f.read().strip()
        if len(key) == 50:
            return key
        else:
            return f.write(''.join([choice(char) for i in range(50)]))
    except IOError:
        try:
            with open(key_file, 'w') as f:
                f.write(''.join([choice(char) for i in range(50)]))
        except IOError:
            raise Exception('Can not open file `%s` for writing.' % key_file)
    finally:
        if f:
            f.close()
