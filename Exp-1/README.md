## Comparing Text Retrieval: Cosine Similarity vs. Mixture of Logits

This experiment compares two methods for retrieving embedded text: **cosine similarity** and **mixture of logits**. The goal is to analyze whether identical queries yield different `top_k` results and to evaluate other performance metrics between the two techniques.

The text corpus is sourced from two arXiv papers:

1.  "On the theoretical limitations of embedding based retrieval"
2.  "Revisiting Neural Retrieval on Accelerators"

The concept of using a mixture of logits, as described in the second paper, prompted this comparison, so I decided to see what it yields.