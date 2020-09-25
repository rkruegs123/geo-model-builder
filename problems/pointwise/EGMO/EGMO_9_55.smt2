(declare-points A B C D E F O Tab Tbc Tcd Tde Tef Tfa X)

;; ABCDEF is a hexagon circumscribed about a circle
(assert (polygon A B C D E F))
(assert (insidePolygon O A B C D E F))

(assert (foot Tab O A B))
(assert (foot Tbc O B C))
(assert (foot Tcd O C D))
(assert (foot Tde O D E))
(assert (foot Tef O E F))
(assert (foot Tfa O F A))

(assert (cong O Tab O Tbc))
(assert (cong O Tab O Tcd))
(assert (cong O Tab O Tde))
(assert (cong O Tab O Tef))
(assert (cong O Tab O Tfa))

;; Prove that AD, BE, CF are concurrent
(assert (interLL X A D B E))
(prove (coll X C F))