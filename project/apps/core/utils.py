import os
import random
import string
from rest_framework.exceptions import ParseError

# http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
from uuid import uuid4
from django.utils.deconstruct import deconstructible


def get_random_string(length=10):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))

def delete_file_local(path):
    print "%s deleted" % (path,)
    os.remove(path)


@deconstructible
class GenerateRandomFilename(object):

    def __init__(self, sub_path, allowed_ext=None):
        self.path = sub_path
        self.allowed_ext = allowed_ext

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        ext = ext.lower()
        if self.allowed_ext and (ext not in self.allowed_ext):
            raise ParseError(detail="this file is not proper.")
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)