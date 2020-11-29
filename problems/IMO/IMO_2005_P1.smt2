(param (A B C) equi-tri)

(param A1 point (on-seg B C))
(param A2 point (on-seg A1 C))

(param B1 point (on-seg C A))
(param B2 point (on-seg B1 A))

(param C1 point (on-seg A B))
(param C2 point (on-seg C1 B))

(assert (cong A1 A2 A2 B1))
(assert (cong A1 A2 B1 B2))
(assert (cong A1 A2 B2 C1))
(assert (cong A1 A2 C1 C2))
(assert (cong A1 A2 C2 A1))

(eval (concur (line A1 B2) (line B1 C2) (line C1 A2)))