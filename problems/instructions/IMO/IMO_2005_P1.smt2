(param (A B C) equiTri)

(param A1 point (onSeg B C))
(param A2 point (onSeg A1 C))

(param B1 point (onSeg C A))
(param B2 point (onSeg B1 A))

(param C1 point (onSeg A B))
(param C2 point (onSeg C1 B))

(assert (cong A1 A2 A2 B1))
(assert (cong A1 A2 B1 B2))
(assert (cong A1 A2 B2 C1))
(assert (cong A1 A2 C1 C2))
(assert (cong A1 A2 C2 A1))

(confirm (concur (line A1 B2) (line B1 C2) (line C1 A2)))