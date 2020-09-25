(declare-points A B C P Q M N Aux)

(assert (triangle A B C))
(assert (acutes A B C))

;; P and Q lie on side BC of ABC s.t. ang(PAB) = ang(BCA) and ang(CAQ) = ang(ABC)
(assert (onSeg P B C))
(assert (onSeg Q B C))
(assert (eqangle P A A B B C C A))
(assert (eqangle C A A Q A B B C))

;; M lies on the line AP s.t. M is the midpoint of AM
(assert (midp P A M))

;; N lies on the line AQ s.t. Q is the midpoint of AN
(assert (midp Q A N))

;; Prove that lines BM and CN intersect on the circumcircle of triangle ABC
(assert (interLL Aux B M C N))
(prove (cycl Aux A B C))
