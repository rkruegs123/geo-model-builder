(declare-points A B C D Mab Mdc P)

(assert (polygon A B C D))

;; In convex quadrilateral ABCD, AC and BD are perpendicular and AB and DC are not parallel
(assert (perp A C B D))
(assert (not (para A B D C)))

;; The point P, where the perpendicular bisectors of AB and DC meet, is inside ABCD
(assert (midp Mab A B))
(assert (midp Mdc D C))
(assert (perp P Mab A B))
(assert (perp P Mdc D C))
(assert (insidePolygon P A B C D))

;; FIXME: Prove that ABCD is cyclic iff triangles ABP and CDP have equal areas
