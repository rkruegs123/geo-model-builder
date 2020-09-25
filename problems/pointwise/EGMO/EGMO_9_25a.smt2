;; (a) - P, Q, R are the poles of QR, RP, PQ, respectively
;; (b) - O is the orthocenter of PQR

(declare-points A B C D O P Q R P1 Q1 R1)

(assert (polygon A B C D))
(assert (cycl A B C D))
(assert (circumcenter O A B C))

(assert (interLL P A B C D))
(assert (interLL Q B C D A))
(assert (interLL R A C B D))

;; Prove that P, Q, R are the poles of QR, RP, PQ, respectively

;; Ex. P is the point that has QR as its polar: QR passes through P* perpendicular to OP
;; Note: Do we need to assert that QR does not pass through O?
(assert (inverse P1 P O A))
(prove (coll P1 Q R))
(prove (perp Q R O P))

(assert (inverse Q1 Q O A))
(prove (coll Q1 R P))
(prove (perp R P O Q))

(assert (inverse R1 R O A))
(prove (coll R1 P Q))
(prove (perp P Q O R))