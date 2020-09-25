(declare-points A B C O P D E)

(assert (triangle A B C))
(assert (perp A B B C))
(assert (circumcenter O A B C))

(assert (perp P A O A))

(assert (cycl A B C D))
(assert (onRay D P B))

(assert (coll E C D))
(assert (para A E B C))

(prove (coll P O E))