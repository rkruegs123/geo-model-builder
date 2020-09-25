(declare-points A B C D M P Q X Y)

(assert (polygon A C B D))
(assert (cycl A B C D))
(assert (interLL M A B C D))

(assert (cycl P A B C))
(assert (cycl Q P B C))
(assert (coll M P Q))

(assert (interLL X P Q A D))
(assert (interLL Y P Q B C))

;; If MP = MQ, then MX = MY
(assert (cong M P M Q))
(prove (cong M X M Y))
