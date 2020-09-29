;; Oi is the center of circle i (denoted Ci)
;; C1 intersects C2 at A and B
;; C1 intersects C3 at C and D
;; C2 intersects C3 at E and F

(declare-points O1 O2 O3 A B C D E F X)

;; Helper
(assert (triangle O1 O2 O3))

;; C1
(assert (cycl A B C D))
;; (assert (circumcenter O1 A B C))
(assert (cong O1 A O1 B))
(assert (cong O1 A O1 C))

;; C2
(assert (cycl A B E F))
;; (assert (circumcenter O2 A B E))
(assert (cong O2 A O2 B))
(assert (cong O2 A O2 E))

;; C3
(assert (cycl C D E F))
;; (assert (circumcenter O3 C D E))
(assert (cong O3 C O3 D))
(assert (cong O3 C O3 E))

;; The common chords AB, CD, and EF are concurrent
(assert (interLL X A B C D))
(confirm (coll X E F))