;; Simson Line
(declare-points A B C P X Y Z)

(assert (triangle A B C))

;; Note that P is ANY point on (ABC)
(assert (cycl P A B C))

;; X, Y, Z are the feet of the perpendiculars from P onto lines BC, CA, and AB
(assert (foot X P B C))
(assert (foot Y P C A))
(assert (foot Z P A B))

;; Prove that X, Y, and Z are collinear
(confirm (coll X Y Z))