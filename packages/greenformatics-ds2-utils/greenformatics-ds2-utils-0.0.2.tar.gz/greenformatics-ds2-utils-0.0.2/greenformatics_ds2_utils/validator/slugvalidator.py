# coding=utf-8

from greenformatics_ds2_utils import Singleton


class SlugValidator(metaclass=Singleton):
    slugs = set()

    def __init__(self):
        # Put your code here: initial load of the set of the unique values. The initial values are for a database maybe
        return

    def add_slug(self, slug):
        self.slugs.add(slug)

    def has_slug(self, slug):
        if slug in self.slugs:
            return True
        else:
            return False
