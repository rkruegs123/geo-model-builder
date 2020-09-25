;; (a) - P, Q, R are the poles of QR, RP, PQ, respectively
;; (b) - O is the orthocenter of PQR

(declare-points A B C D O P Q R)

(assert (polygon A B C D))
(assert (cycl A B C D))
(assert (circumcenter O A B C))

(assert (interLL P A B C D))
(assert (interLL Q B C D A))
(assert (interLL R A C B D))

(prove (orthocenter O P Q R))