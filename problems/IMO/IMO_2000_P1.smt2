(param C point)
(param D point)
(param M point (on-seg C D))

(param A point)
(param N point (on-circ (circ C A M)))
(define B point (inter-lc (para-at A (line C D)) (circ N M D) rs-arbitrary))

(assert (tangent-lc (line A B) (circ C A M)))
(assert (tangent-lc (line A B) (circ N M B)))

(define P point (inter-ll (line N A) (line C M)))
(define Q point (inter-ll (line N B) (line M D)))
(define E point (inter-ll (line C A) (line D B)))
(assert (on-ray E D B))
(assert (on-ray E C A))

(eval (cong P E Q E))