(param (A B C) triangle)
(compute I point (incenter A B C))

(param P point (inPoly A B C))
(assert (eq (add (uangle P B A) (uangle P C A)) (add (uangle P B C) (uangle P C B))))