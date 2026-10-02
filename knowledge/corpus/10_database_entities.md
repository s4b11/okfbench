# Data Model Sketch

Useful tables in the demo mental model include infants, parents, clinicians, visits, immunization schedule rows, nutrition plans, and growth risk assessments.

Relationships keep each chart tied to the correct family and care team. Nutrition assessment rows may store simple scores that the risk module reads. Integrity constraints matter because alerts and plans should never point at the wrong infant.
