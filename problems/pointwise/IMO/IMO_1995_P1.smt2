(declare-points A B C D OAC OBD X Y Z P M N Aux)

;; A, B, C, and D are four distinct points on a line, in that order
(assert (onSeg B A C))
(assert (onSeg C B D))

;; (Note: OAC and OBD are the centers of the circles with diameters AC and BD, respectively)
(assert (midp OAC A C))
(assert (midp OBD B D))

;; The circles with diameters AC and BD intersect at X and Y
(assert (cong OAC C OAC X))
(assert (cong OAC C OAC Y))
(assert (cong OBD D OBD X))
(assert (cong OBD D OBD Y))

;; XY meets BC at Z
(assert (interLL Z X Y B C))

;; P is a point on XY other than Z
(assert (coll P X Y))

;; CP intersects the circle with diameter AC at C and M
(assert (coll C P M))
(assert (cong OAC C OAC M))

;; BP intersects the circle with diameter BD at B and N
(assert (coll B P N))
(assert (cong OBD B OBD N))

;; AM, DN, XY are concurrent
(assert (interLL Aux A M D N))
(prove (coll Aux X Y))
