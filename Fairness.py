The Fairlearn open-source package provides postprocessing and reduction unfairness mitigation algorithms:
*********************** mitigation algorithms ***********************

(1) ExponentiatedGradient - reduction - Binary classification and regression - Demographic parity, equalized odds
(2) GridSearch - reduction -Binary classification and regression - Demographic parity, equalized odds / Bounded group loss
(3) ThresholdOptimizer - postprocessing - Binary classification - Demographic parity, equalized odds

*********************** parity constraints ***********************

(1) Demographic parity: any
(2) True positive rate parity: any
(3) False-positive rate parity: any
(4) Equalized odds: any
(5) Error rate parity: reduction-based mitigation algorithms (Exponentiated Gradient and Grid Search) 
(6) Bounded group loss: reduction-based mitigation algorithms (Exponentiated Gradient and Grid Search) 
