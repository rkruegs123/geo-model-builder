(declare-points A B C D X K L M)

(assert (triangle A B C))
(assert (perp B C C A))

(assert (foot D C A B))

(assert (onSeg X C D))

(assert (onSeg K A X))
(assert (cong B K B C))

(assert (onSeg L B X))
(assert (cong A L A C))

(assert (interLL M A L B K))

(prove (cong M K M L))
