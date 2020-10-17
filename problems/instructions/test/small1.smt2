(param (A B C) triangle)
(param D point)
(assert (oppSides D B (line A C)))
(assert (not (coll D A C)))

(param X point (onRayOpp A B))
(param Y point (onRayOpp C B))

(compute omega_O point (interLL (perpAt X (line A B)) (perpAt Y (line B C))))
(compute omega circle (coa omega_O X))

(assert (onCirc Y omega))
(assert (tangentLC (line A D) omega))
(assert (tangentLC (line C D) omega))
