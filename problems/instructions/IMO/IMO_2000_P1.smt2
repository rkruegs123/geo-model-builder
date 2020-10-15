(param C point)
(param A point)
(param M point)
(param N point (onCirc (circ C A M)))

(param B point)
(param D point (onCirc (circ N M B)))

(assert (tangentLC (line A B) (circ C A M)))
(assert (tangentLC (line A B) (circ N M B)))

(assert (onSeg M C D))
(assert (para (line C D) (line A B)))

(compute P point (interLL (line N A) (line C M)))
(compute Q point (interLL (line N B) (line M D)))
(compute E point (interLL (line C A) (line D B)))
(assert (onRay E D B))
(assert (onRay E C A))

(confirm (cong P E Q E))