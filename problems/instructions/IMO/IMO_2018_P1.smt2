(param (A B C) acuteTri)

(compute gamma circle (circumcircle A B C))

(param D point (onSeg A B))
(param E point (onSeg A C))
(assert (cong A D A E))

(compute F point (interLC (perpBis B D) gamma (rsOppSides C (line A B))))
(compute G point (interLC (perpBis C E) gamma (rsOppSides B (line A C))))

(confirm (para (line D E) (line F G)))
