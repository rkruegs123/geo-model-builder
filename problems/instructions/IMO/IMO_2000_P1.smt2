(param C point)
(param A point)
(param M point)
(param N point (onCirc (circ C A M)))

(param B point)
(param D point (onCirc (circ N M B)))

(assert (tangent (line A B) (circ C A M)))
(assert (tangent (line A B) (circ N M B)))

(assert (onSeg M C D))
(assert (para C D A B))

(compute P point (interLL N A C M))
(compute Q point (interLL N B M D))
(compute E point (interLL C A D B))
(assert (onRay E D B))
(assert (onRay E C A))

(confirm (cong P E Q E))