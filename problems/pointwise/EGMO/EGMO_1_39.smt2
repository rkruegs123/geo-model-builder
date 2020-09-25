(declare-points A B C I D E O)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I A B))
(assert (foot E I A C))
(assert (circumcenter O B C I))

(prove (eqangle O D D B C E E O))

(watch (coll O A I))
(watch (ibisector I B A C))
(watch (cong A D A E))