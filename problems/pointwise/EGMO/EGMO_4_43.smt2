(declare-points A B C O A1 B1 C1 A2 B2 C2 Aux)

;; ABC is a nonisosceles, nonright triangle
;; FIXME: We are currently filtering the equilateral case
(assert (triangle A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong A C B C)))
(assert (not (perp A B B C)))
(assert (not (perp B A A C)))
(assert (not (perp B C C A)))

;; O is the circumcenter if ABC
(assert (circumcenter O A B C))

;; A1, B1, and C1 are the midpoints of sides BC, CA, and AB, respectively
(assert (midp A1 B C))
(assert (midp B1 C A))
(assert (midp C1 A B))

;; Point A2 is located on the ray OA1 s.t. OAA1 is similiar to OA2A
(assert (onRay A2 O A1))
(assert (simtri O A A1 O A2 A))

;; Point B2 is on the ray OB1 s.t. OBB1 is similar to OB2B
(assert (onRay B2 O B1))
(assert (simtri O B B1 O B2 B))

;; Point C2 is on the ray OC1 s.t. OCC1 is similar to OC2C
(assert (onRay C2 O C1))
(assert (simtri O C C1 O C2 C))

;; Prove that th elines AA2, BB2, and CC2 are concurrent
(assert (interLL Aux A A2 B B2))
(prove (coll Aux C C2))