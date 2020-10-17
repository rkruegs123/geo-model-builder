(param (A B C D) polygon)
(assert (not (on-line D (i-bisector A B C))))
(assert (not (on-line B (i-bisector C D A))))

(param P point (in-poly A B C D))
(assert (= (uangle P B C) (uangle D B A)))
(assert (= (uangle P D C) (uangle B D A)))

(assert (cycl A B C D))
(confirm (cong A P C P))
