(declare-points A B C G ABaux ACaux BCaux Oa Ob Oc)

(assert (triangle A B C))
(assert (centroid G A B C))

(assert (cong A B A ABaux))
(assert (cong A B B ABaux))
(assert (circumcenter Oc A B ABaux))
(assert (oppSides C Oc A B))

(assert (cong B C B BCaux))
(assert (cong B C C BCaux))
(assert (circumcenter Oa B C BCaux))
(assert (oppSides A Oa B C))

(assert (cong A C A ACaux))
(assert (cong A C C ACaux))
(assert (circumcenter Ob A C ACaux))
(assert (oppSides B Ob A C))

(prove (cong Oa Ob Oa Oc))
(prove (cong Oa Ob Ob Oc))

(prove (circumcenter G Oa Ob Oc))