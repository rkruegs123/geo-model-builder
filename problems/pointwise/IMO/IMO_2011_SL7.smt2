(declare-points A B C D E F O Tab Tbc Tcd Tde Tef Tfa J Fbdf K L)

;; ABCDEF is a convex hexagon
(assert (polygon A B C D E F))
(assert (circumcenter O A C E))

;; All of the sides of ABCDEF are tangent to a circle with center O
(assert (coll Tab A B))
(assert (perp A B O Tab))

(assert (coll Tbc B C))
(assert (perp B C O Tbc))

(assert (coll Tcd C D))
(assert (perp C D O Tcd))

(assert (coll Tde D E))
(assert (perp D E O Tde))

(assert (coll Tef E F))
(assert (perp E F O Tef))

(assert (coll Tfa F A))
(assert (perp F A O Tfa))

;; J is the foot of the perpendicular from B to CD
(assert (foot J B C D))

;; The perpendicular from B to DF intersects EO at a point K
(assert (foot Fbdf B D F))
(assert (interLL K B Fbdf E O))

;; L is the foo to fthe perpendicular from K to DE
(assert (foot L K D E))

;; Prove that DJ = DL
(prove (cong D J D L))
