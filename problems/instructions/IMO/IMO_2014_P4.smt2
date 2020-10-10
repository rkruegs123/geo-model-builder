(param (A B C) acuteTri)
(param P point (onSeg B C))
(param Q point (onSeg B C))
(assert (eqangle P A A B B C C A))
(assert (eqangle C A A Q A B B C))

(compute M point (midpFrom P A))
(compute N point (midpFrom Q A))

(confirm (onCirc (interLL B M C N) (circumcircle A B C)))