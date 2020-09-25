(declare-points A B O P A1 B1)

(assert (inverse A1 A O P))
(assert (inverse B1 B O P))

(prove (eqangle O A A B A1 B1 B1 O))
