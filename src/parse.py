"""
Copyright (c) 2020 Ryan Krueger. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Ryan Krueger, Jesse Michael Han, Daniel Selsam
"""

from typing import List
import pdb

def parse_sexprs(lines):
    def parse_sexpr(s :str):
        return read_from_tokens(tokenize(s))

    def tokenize(s :str):
        result = s.replace('(',' ( ').replace(')',' ) ').split()

        # discard comments
        for i, tk in enumerate(result):
          # if tk == ";;":
          if tk[0] == ";":
            return result[:i]

        return result

    def read_from_tokens(tokens :List[str]):
        "Read an expression from a sequence of tokens."
        if len(tokens) == 0:
          return
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(read_from_tokens(tokens))
            tokens.pop(0) # pop off ')'
            return tuple(L)
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return token

    try:
        result = list()
        for l in lines:
            sexp = parse_sexpr(l)
            if sexp:
                result.append(sexp)
        return result
    except:
        raise RuntimeError("Could not parse s-expressions")

    '''
    with open(filename, 'r') as f:
      result = []
      for l in f.readlines():
        sexp = parse_sexpr(l)
        if sexp:
          result.append(sexp)
      return result
    '''

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("arg")
  opts = parser.parse_args()
  result = parse_sexprs(opts.arg)
  print(result)
