(declare-points A B C D O1 O2 CX E F X Y)

;; Choose a point D inside triangle ABC
(assert (triangle A B C))
(assert (insidePolygon D A B C))

;; omega_1 is a circle passing through B and D
(assert (cong O1 B O1 D))

;; omega_2 is a circle passing through C and D
(assert (cong O2 C O2 D))

;; the other point of intersection of the two circles (CX) lies on AD
(assert (onSeg CX A D))
(assert (cong O1 D O1 CX))
(assert (cong O2 D O2 CX))

;; let omega_1 and omega_2 intersect side BC at E and F, respectively
(assert (cycl E B D CX))
(assert (onSeg E B C))

(assert (cycl F C D CX))
(assert (onSeg F B C))

;; Denote by X the intersection of lines DF and AB
(assert (interLL X D F A B))

;; Y is the intersection of DE and AC
(assert (interLL Y D E A C))

;; Prove that XY is parallel to BC
(prove (para X Y B C))