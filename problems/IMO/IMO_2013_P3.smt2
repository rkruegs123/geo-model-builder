(param (A B C) triangle)

(let A1 point (foot (excenter A B C) (line B C)))
(let B1 point (foot (excenter B A C) (line C A)))
(let C1 point (foot (excenter C B A) (line A B)))

(assert (on-circ (circumcenter A1 B1 C1) (circumcircle A B C)))

(eval (right-tri A B C))
