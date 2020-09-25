(declare-points A B C D E F G H Oegh)

;; ABCD is a cyclic quadrilateral
(assert (polygon A B C D))
(assert (cycl A B C D))

;; AC and BD meet at E
(assert (interLL E A C B D))

;; AD and BC meet at F
(assert (interLL F A D B C))

;; The midpoints of AB and CD are G and H, respectively
(assert (midp G A B))
(assert (midp H C D))

;; Show that EF is tangent at E to the circle through the points E, G, and H
(assert (circumcenter Oegh E G H))
(prove (perp E F Oegh E))