(declare-points A B C D E F LA1 LA2 MA1 MA2 A1 LB1 LB2 MB1 MB2 B1 LC1 LC2 MC1 MC2 C1)

(assert (triangle A B C))
(assert (amidpOpp D B C A))
(assert (amidpOpp E C A B))
(assert (amidpOpp F A B C))

;; Line la passes through the feet of the perpendiculars from A to DB and DC
(assert (foot LA1 A D B))
(assert (foot LA2 A D C))

;; Line ma passes through the feet of the perpendiculars from D to AB and AC
(assert (foot MA1 D A B))
(assert (foot MA2 D A C))

;; Let A1 denote the intersection of lines la and ma
(assert (interLL A1 LA1 LA2 MA1 MA2))

;; Define B1 and C1 similarly
(assert (foot LB1 B E A))
(assert (foot LB2 B E C))

(assert (foot MB1 E A B))
(assert (foot MB2 E B C))

(assert (interLL B1 LB1 LB2 MB1 MB2))

(assert (foot LC1 C F A))
(assert (foot LC2 C F B))

(assert (foot MC1 F A C))
(assert (foot MC2 F B C))

(assert (interLL C1 LC1 LC2 MC1 MC2))

;; Prove that triangles DEF and A1B1C1 are similar
(prove (simtri D E F A1 B1 C1))