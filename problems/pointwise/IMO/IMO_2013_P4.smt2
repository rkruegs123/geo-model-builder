;; Note: O1 is the center of omega_1
(declare-points A B C H M N W O1 X O2 Y)

(assert (triangle A B C))
(assert (acutes A B C))

(assert (orthocenter H A B C))
(assert (foot M B A C))
(assert (foot N C A B))

;; W lies on BC, lying strictly between B and C
(assert (onSeg W B C))

;; omega_1 is the circumcircle of BWN (circumcenter is O1)
(assert (circumcenter O1 B W N))

;; X is on the circumcircle of BWN s.t.  WX is a diameter of omega_1 (workaround)
(assert (cycl B W N X))
(assert (coll W X O1))

;; omega_2 is the circumcircle of CWM (circumcenter is O2)
(assert (circumcenter O2 C W M))

;; Y is on the circumcircle of CWM s.t. WY is a diameter of omega_2
(assert (cycl C W M Y))
(assert (coll W Y O2))

(prove (coll X Y H))
