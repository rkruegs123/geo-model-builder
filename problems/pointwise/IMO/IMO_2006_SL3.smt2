(declare-points A B C D E P Aux)

;; ABCDE is a convex pentagon
(assert (polygon A B C D E))

;; <BAC = <CAD = <DAE
(assert (eqangle B A A C C A A D))
(assert (eqangle B A A C D A A E))

;; <ABC = <ACD = <ADE
(assert (eqangle A B B C A C C D))
(assert (eqangle A B B C A D D E))

;; BD and CE meet at P
(assert (interLL P B D C E))

;; Prove that the line AP bisects the side CD
(assert (interLL Aux A P C D))
(prove (cong C Aux D Aux))