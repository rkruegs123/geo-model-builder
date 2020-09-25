(declare-points A B C H Oabh Obch Ocah)

(assert (triangle A B C))
(assert (orthocenter H A B C))
(assert (circumcenter Oabh A B H))
(assert (circumcenter Obch B C H))
(assert (circumcenter Ocah C A H))

;; Prove that the above circumcenters are verticies of a triangle that is congruent to ABC
(prove (contri A B C Obch Ocah Oabh))
