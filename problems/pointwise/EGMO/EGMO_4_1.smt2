(declare-points A B C P X Y Z H K L)

;; P is a point on the circumcircle of triangle ABC
(assert (triangle A B C))
(assert (cycl P A B C))

;; X, Y, and Z are the feet of the perpendiculars from P onto lines BC, CA, and AB, respectively
;; Note: XYZ is the Simson line of P w.r.t. ABC
(assert (foot X P B C))
(assert (foot Y P C A))
(assert (foot Z P A B))

;; H is the orthocenter of ABC
(assert (orthocenter H A B C))

;; PX meets the circumcircle of ABC again at a point K
(assert (coll K P X))
(assert (cycl K P A B))

;; AH intersects the Simson line at the point L
(assert (interLL L A H X Y))

;; Prove that the Simson line is parallel to AK
(prove (para X Y A K))
