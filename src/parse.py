from typing import List


def parse_sexprs(filename):
    def parse_sexpr(s :str):
        return read_from_tokens(tokenize(s))

    def tokenize(s :str):
        result = s.replace('(',' ( ').replace(')',' ) ').split()

        # discard comments
        for i, tk in enumerate(result):
          if tk == ";;":
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

    with open(filename, 'r') as f:
      result = []
      for l in f.readlines():
        sexp = parse_sexpr(l)
        if sexp:
          result.append(sexp)
      return result

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("arg")
  opts = parser.parse_args()
  result = parse_sexprs(opts.arg)
  print(result)
