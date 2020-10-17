(param (A B C) triangle)

(compute A1 point (foot (excenter A B C) (line B C)))
(compute B1 point (foot (excenter B A C) (line C A)))
(compute C1 point (foot (excenter C B A) (line A B)))

(assert (on-circ (circumcenter A1 B1 C1) (circumcircle A B C)))

;; (confirm (rightTri A B C))
