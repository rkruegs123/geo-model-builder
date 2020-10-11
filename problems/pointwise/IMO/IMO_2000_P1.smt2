(declare-points A B C D M N Ocmn Odmn P Q E)

(assert (triangle A B C))
(assert (para D C A B))
(assert (onSeg M C D))

(assert (onSeg P N A))
(assert (onSeg P C M))

(assert (onSeg Q N B))
(assert (onSeg Q M D))

(assert (onRay E C A))
(assert (onRay E D B))

(assert (circumcenter Ocmn C M N))
(assert (circumcenter Odmn D M N))

(assert (cycl A C M N))
(assert (cycl B D M N))

(assert (perp A B A Ocmn))
(assert (perp B A B Odmn))

(confirm (cong P E Q E))
