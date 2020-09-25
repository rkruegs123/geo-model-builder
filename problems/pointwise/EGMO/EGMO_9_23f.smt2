(declare-points O1 P1 X X1 XP Y Y1 YP)

;; The polar of X is the line passing through X1 perpendicular to (O1, X)
;; (X1, XP) is the polar of X
(assert (inverse X1 X O1 P1))
(assert (perp X1 XP O1 X))

;; If Y lies on the polar of X, then X lies on the polar of Y
(assert (coll Y X1 XP))

;; (Y1, YP) is the polar of Y
(assert (inverse Y1 Y O1 P1))
(assert (perp Y1 YP O1 Y))

(prove (coll X Y1 YP))