(param (A B C) triangle)

(compute A1 point (foot (excenter A B C) B C))
(compute B1 point (foot (excenter B A C) C A))
(compute C1 point (foot (excenter C B A) A B))

(assert (onCirc (circumcenter A1 B1 C1) (circumcircle A B C)))

;; (confirm (rightTri A B C))
