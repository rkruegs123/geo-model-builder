;; Oa is the center of the A-mixtilinear circle
;; Oabc is the incenter of ABC

(declare-points A B C I Oa L K)

;; ABC is a triangle
(assert (triangle A B C))
(assert (incenter I A B C))
(assert (mixtilinearIncenter Oa A B C))

;; K and L are the tangency points on AB and AC of the A-mixtilinear circle
(assert (perp Oa L A C))
(assert (onSeg L A C))
(assert (perp Oa K A B))
(assert (onSeg K A B))

;; We know I lies on KL from Lemma 4.36 -- adding this here is training wheels
(assert (coll I K L))

;; Check that I is in fact the midpoint of KL
(prove (midp I K L))