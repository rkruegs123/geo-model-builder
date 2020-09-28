(sample (A B C) triangle)

(compute I (incenter A B C))
(compute Ia (excenter A B C))
(compute D (interLL (perpAt I B C) (line B C)))
(compute X (interLL (perpAt Ia B C) (line B C)))
(confirm (cong B X C D))
(confirm (cong B D C X))