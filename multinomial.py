from __future__ import division
__author__ = 'Sarper'

from itertools import imap
from math import log
import sys


class MultinomialObject:

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __str__(self):
        return self.name

    def __hash__(self):
        hash(self.name)


class Multinomial:

    def __init__(self, identifier, counts):
        self.identifier = MultinomialObject(identifier, -1)
        self.objects = {key: MultinomialObject(key, counts[key])
                        for key in counts.iterkeys()}
        self.probs = {}

    def __getitem__(self, identifier):
        return self.probs.get(identifier, 0.0)

    def log_prob(self, identifier):
        return log(self.probs.get(identifier, sys.float_info.epsilon))

    def estimate(self):
        total = sum(x.count for x in self.objects.itervalues())
        self.probs = {key: self.objects[key].count/total
                      for key in self.objects.iterkeys()}

    def increment(self, item, amount=1):
        self.objects[item].count += amount

    def __iter__(self):
        return self.objects.iterkeys()


class TableOfMultinomial:

    def __init__(self):
        self.multinomials = {}

    def create(self, identifier, counts):
        self.multinomials[identifier] = Multinomial(identifier, counts)
        self.multinomials[identifier].estimate()

    def create_all(self, multinomials):
        for identifier, count in multinomials:
            self.create(identifier, count)

    def estimate(self):
        for x in self.multinomials.itervalues():
            x.estimate()

    def __getitem__(self, item):
        return self.multinomials[item]

    def __iter__(self):
        return self.multinomials.iterkeys()