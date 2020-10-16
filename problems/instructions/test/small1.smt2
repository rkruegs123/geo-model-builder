(param (A B C) triangle)

(param E point (onLine (line A B)))
(assert (onRay E A B))
(assert (not (onSeg E A B)))