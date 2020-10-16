(param C point)
(param D point)
(param M point (onSeg C D))

(param A point)
(param N point (onCirc (circ C A M)))
(compute B point (interLC (paraAt A (line C D)) (circ N M D) rsArbitrary))

(assert (tangentLC (line A B) (circ C A M)))
(assert (tangentLC (line A B) (circ N M B)))

(compute P point (interLL (line N A) (line C M)))
(compute Q point (interLL (line N B) (line M D)))
(compute E point (interLL (line C A) (line D B)))
(assert (onRay E D B))
(assert (onRay E C A))

(confirm (cong P E Q E))