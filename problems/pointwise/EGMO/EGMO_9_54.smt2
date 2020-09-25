(declare-points A B C O O1 D E G H L M X)

(assert (triangle A B C))
(assert (circumcenter O A B C))

;; A circle passing through A and C meets BC and BA at D and E, respectively
(assert (cong O1 A O1 C))
(assert (cong O1 B O1 D))
(assert (cong O1 A O1 E))
;; Note we use collinearity rather than onSeg. Correct?
(assert (coll D B C))
(assert (coll E B A))

;; The lines AD and CE meet Gamma again at G and H
(assert (coll G A D))
(assert (coll H C E))
(assert (cycl G A B C))
(assert (cycl H A B C))

;; The tangent lines to Gamma at A and C meet the line DE at L and M, respectively
(assert (perp A L O A))
(assert (perp C M O C))
(assert (coll L D E))
(assert (coll M D E))

;; Prove that the lines LH and MG meet at Gamma
(assert (interLL X L H M G))
(prove (cycl X A B C))