(sample (A B C) triangle)

(let I (incenter A B C))
(let Ia (excenter A B C))
(let D (interLL (perpAt I B C) (line B C)))
(let X (interLL (perpAt Ia B C) (line B C)))
(confirm (cong B X C D))
(confirm (cong B D C X))
