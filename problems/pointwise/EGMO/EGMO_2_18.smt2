(declare-points A B C Ia X B1 C1 I)

;; Let the external bisectors of B and C in a triangle ABC intersect at Ia
(assert (triangle A B C))
(assert (ebisector Ia A B C))
(assert (ebisector Ia B C A))

;; Show that Ia is the center of a circle tangent to BC, thfe extensiono f AB through B, and the extension of AC through C
(assert (foot X Ia B C))
(assert (foot B1 Ia A B))
(assert (foot C1 Ia A C))
(prove (circumcenter Ia X B1 C1))

;; Note: The below are commented out but may but may be required
;; (prove (onRay B1 A B))
;; (prove (not (onSeg B1 A B)))

;; (prove (onRay C1 A C))
;; (prove (not (onSeg C1 A C)))

;; Furthermore, show that Ia lies on ray AI
(assert (incenter I A B C))
(prove (onRay Ia A I))