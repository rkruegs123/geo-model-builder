(declare-points A B C D P Q E)

;; ABCD is a convex quadrilateral
(assert (polygon A B C D))

;; P and Q are points in ABCD s.t. PQDA and QPBC are cyclic quadrilaterals
(assert (insidePolygon P A B C D))
(assert (insidePolygon Q A B C D))
(assert (cycl P Q D A))
(assert (cycl Q P B C))

;; E is on the line segment PQ s.t. <PAE = <QDE and <PBE = <QCE
(assert (onSeg E P Q))
(assert (eqangle P A A E Q D D E))
(assert (eqangle P B B E Q C C E))

;; Show that ABCD is cyclic
(prove (cycl A B C D))