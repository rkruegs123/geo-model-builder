(declare-points A B C I D E F P Q R X)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))

(assert (cycl P A B C))
(assert (cycl Q A B C))
(assert (cycl R A B C))

(assert (cycl P A E F))
(assert (cycl Q B D F))
(assert (cycl R C D E))

(assert (interLL X P D Q E))
(assert (coll X R F))