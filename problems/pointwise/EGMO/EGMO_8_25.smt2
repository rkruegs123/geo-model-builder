(declare-points A B C P Opab Opbc Opca)

(assert (coll A B C))
(assert (not (coll P A B)))

(assert (circumcenter Opab P A B))
(assert (circumcenter Opbc P B C))
(assert (circumcenter Opca P C A))

(prove (cycl P Opab Opbc Opca))
