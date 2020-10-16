(param (A B C) acuteTri)

(compute Gamma circle (circumcircle A B C))

(param D point (onSeg A B))
(param E point (onSeg A C))
(assert (cong A D A E))

(compute F point (interLC (perpBis B D) Gamma (rsOppSides C (line A B))))
(compute G point (interLC (perpBis C E) Gamma (rsOppSides B (line A C))))

(confirm (para (line D E) (line F G)))
