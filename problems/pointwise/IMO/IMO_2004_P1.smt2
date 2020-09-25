(declare-points A B C M N O A1 O1 R Aux)

;; ABC is an acute-angled triangle with AB /= AC
(assert (triangle A B C))
(assert (acutes A B C))
(assert (not (cong A B A C)))

;; Circ with diameter BC intersects AB and AC at M and N
(assert (cycl B C M N))
(assert (onSeg M A B))
(assert (onSeg N A C))

;; O is the midpoint of BC
(assert (midp O B C))
(assert (circumcenter O B C M))

;; The bisectors of ang(BAC) and ang(MON) intersect at R
(assert (ibisector R B A C))
(assert (ibisector R M O N))

;; Prove that the circumcircles of the triangles BMR and CNR have a common point lying on the side BC
(assert (onSeg Aux B C))
(assert (cycl Aux B M R))
(prove (cycl Aux C N R))
