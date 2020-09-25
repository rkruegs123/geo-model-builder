(declare-points P Q R S H K M)

;; PQRS isa cyclic quadrilateral
(assert (polygon P Q R S))
(assert (cycl P Q R S))

;; <PSR = 90
(assert (perp P S S R))

;; H and K are the feet of the altitudes from Q to lines PR and PS
(assert (foot H Q P R))
(assert (foot K Q P S))

;; Prove that HK bisects QS
(assert (interLL M H K Q S))
(prove (cong M Q M S))