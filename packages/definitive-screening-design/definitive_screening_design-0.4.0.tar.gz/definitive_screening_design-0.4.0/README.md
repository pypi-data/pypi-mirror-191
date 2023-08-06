# Definitive Screening Design (DSD)

## Main References

- Bradley Jones and Christopher J. Nachtsheim. "A Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects" Journal of Quality Technology 43, no. 1 (January 2011): 1–15. https://doi.org/10.1080/00224065.2011.11917841.
- Bradley Jones and Christopher J. Nachtsheim. "Definitive screening designs with added two-level categorical factors" Journal of Quality Technology 45.2 (2013): 121-129. https://doi.org/10.1080/00224065.2013.11917921

## Further References about the practical use of this design

- Bradley Jones. ["Proper and Improper use of Definitive Screening Designs"](https://community.jmp.com/t5/JMP-Blog/Proper-and-improper-use-of-Definitive-Screening-Designs-DSDs/ba-p/30703?trMode=source)
- Douglas Motngomery. [Coursera lesson on "General Structure of a DSD with m Factors"](https://www.coursera.org/lecture/response-surfaces-mixtures-model-building/general-structure-of-a-definitive-screening-design-with-m-factors-N1Ebc)
- Paul Nelson. ["The Evolution of Definitive Screening Designs from Optimal (Custom) DoE"](https://www.prismtc.co.uk/resources/blogs-and-articles/article-the-evolution-of-definitive-screening-designs-from-optimal-custom-design-of-experiments)

## Installation
```
pip install definitive_screening_design
```

## Example
Generate a Definitive Design screening with three numerical and two 2-levels categoricals factors,
using the protocol presented in the 2013 paper.
The result is a Pandas DataFrame.

```
import definitive_screening_design as dsd
dsd.generate(n_num=3, n_cat=2)
```
|    |   X01 |   X02 |   X03 |   C01 |   C02 |
|---:|------:|------:|------:|------:|------:|
|  1 |     0 |     1 |     1 |     2 |     2 |
|  2 |    -0 |    -1 |    -1 |     1 |     1 |
|  3 |     1 |     0 |    -1 |     2 |     2 |
|  4 |    -1 |    -0 |     1 |     1 |     1 |
|  5 |     1 |    -1 |     0 |     1 |     2 |
|  6 |    -1 |     1 |    -0 |     2 |     1 |
|  7 |     1 |     1 |    -1 |     2 |     1 |
|  8 |    -1 |    -1 |     1 |     1 |     2 |
|  9 |     1 |     1 |     1 |     1 |     2 |
| 10 |    -1 |    -1 |    -1 |     2 |     1 |
| 11 |     1 |    -1 |     1 |     2 |     1 |
| 12 |    -1 |     1 |    -1 |     1 |     2 |
| 13 |     0 |     0 |     0 |     1 |     1 |
| 14 |     0 |     0 |     0 |     2 |     2 |

Check the `notebooks` folder for further examples and explainations.