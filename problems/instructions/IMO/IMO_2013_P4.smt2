(param (A B C) acuteTri)
(compute H point (orthocenter A B C))
(param W point (onSeg B C))
(compute M point (foot B C A))
(compute N point (foot C A B))

(compute omega_1 circle (circumcircle B W N))
(param X point (onCirc omega_1))
(assert (eq (diam omega_1) (dist W X)))

(compute omega_2 circle (circumcircle C W M))
(param Y point (onCirc omega_2))
(assert (eq (diam omega_2) (dist W Y)))

(confirm (coll X Y H))