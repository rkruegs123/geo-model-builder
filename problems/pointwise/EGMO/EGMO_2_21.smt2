(declare-points X Y O1 O2 P Q R S)

(assert (cycl P Q X Y))
(assert (cycl R S X Y))

(assert (cycl P Q R S))

(assert (cong O1 X O1 Y))
(assert (cong O1 X O1 S))

(assert (cong O2 X O2 Y))
(assert (cong O2 X O2 P))

(assert (coll O1 P Q))
(assert (coll O2 R S))
