(param (A B C D) polygon)
(assert (not (onLine D (ibisector A B C))))
(assert (not (onLine B (ibisector C D A))))

(param P point (inPoly A B C D))
(assert (eq (uangle P B C) (uangle D B A)))
(assert (eq (uangle P D C) (uangle B D A)))

(assert (cycl A B C D))
(confirm (cong A P C P))
