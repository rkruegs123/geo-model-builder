(declare-points A B C I D E F X)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I C A))
(assert (foot F I A B))

;; Prove that AD, BE, and CF concur
(assert (interLL X A D B E))
(prove (coll X C F))