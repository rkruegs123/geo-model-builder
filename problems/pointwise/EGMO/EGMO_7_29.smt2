(declare-points A B C M N P D E F)

;; ABC is an acute, scalene triangle
(assert (triangle A B C))
(assert (acutes A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong B C A C)))

;; M, N, and P are the midpoints of BC, CA, and AB
(assert (midp M B C))
(assert (midp N C A))
(assert (midp P A B))

;; Let the perpendicular bisectors of AB and AC intersect ray AM in points D and E, respectively
(assert (onRay D A M))
(assert (onRay E A M))
(assert (perp P D A B))
(assert (perp N E A C))

;; Let lines BD and CE intersect in points F, inside triangle ABC
(assert (interLL F B D C E))
(assert (insidePolygon F A B C))

;; Prove that points A, N, F and P all lie in one circle
(prove (cycl A N F P))
