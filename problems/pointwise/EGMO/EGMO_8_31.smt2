(declare-points A B C O Oc Aux P Q Q1)

(assert (triangle A B C))
(assert (circumcenter O A B C))
(assert (mixtilinearIncenter Oc C A B))

(assert (foot Aux Oc A C))
(assert (cong Oc P Oc Aux))
(assert (cong O P O A))
(assert (coll P O Oc))

(assert (insidePolygon Q A B C))
(assert (cong Oc P Oc Q))
(assert (para Q Q1 A B))
(assert (perp Q Q1 Oc Q))

(prove (eqangle A C C P Q C C B))