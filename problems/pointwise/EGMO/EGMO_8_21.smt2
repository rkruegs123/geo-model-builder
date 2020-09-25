(declare-points A B D Oabd E C O Obod F G)

;; ABDE is a quadrilateral inscribed in a circle with diameter AB whose diagonals meet at C
(assert (polygon A B D E))
(assert (cycl A B D E))
(assert (circumcenter Oabd A B D))
(assert (coll Oabd A B))
(assert (interLL C A D B E))

;; O is the midpoint of AB
(assert (midp O A B))

;; F is on (BOD) s.t. OF is a diameter of (BOD)
(assert (circumcenter Obod B O D))
(assert (cong Obod O Obod B))
(assert (coll Obod O F))

;; Ray FC meets (BOD) again at G
(assert (onRay G F C))
(assert (cycl G F B O))

;; Prove that A, O, G, E are concyclic
(prove (cycl A O G E))
