(declare-points A B C O A1 B1 C1 X Y Z)

(assert (triangle A B C))
(assert (circumcenter O A B C))

(assert (perp A A1 O A))
(assert (perp B B1 O B))
(assert (perp C C1 O C))

(assert (interLL X A A1 B C))
(assert (interLL Y B B1 C A))
(assert (interLL Z C C1 A B))

(prove (coll X Y Z))