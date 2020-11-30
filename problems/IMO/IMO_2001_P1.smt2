(param (A B C) acute-tri)
(define O point (circumcenter A B C))
(define P point (foot A (line B C)))

(assert (gte (uangle B C A) (add (uangle A B C) (div pi 6))))

(eval (lt (add (uangle C A B) (uangle C O P)) (div pi 2)))