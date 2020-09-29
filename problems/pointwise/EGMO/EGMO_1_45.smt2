(declare-points A B C I D E F M N K)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))
(assert (foot E I A C))
(assert (foot F I A B))

(assert (midp M B C))
(assert (midp N A C))

;; Ray BI meets line EF at K
(assert (interLL K B I E F))
(assert (onRay K B I))

;; Show that BK is perp to CK
(confirm (perp B K C K))

;; Then show K lies on line MN
(confirm (coll K M N))