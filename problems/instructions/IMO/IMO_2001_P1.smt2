(param (A B C) acute-tri)
(compute O point (circumcenter A B C))
(compute P point (foot A (line B C)))

(assert (gte (uangle B C A) (add (uangle A B C) (div pi 6))))

(confirm (lt (add (uangle C A B) (uangle C O P)) (div pi 2)))