# Topsis-Rohit-102016087

This package has been created based on Project 1 of the course **UCS654** by: **Rohit Banyal** Roll No: **102016087** Group: **3CS11**

Topsis-Rohit-102016087 is a Python package implementing Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS) method used for Multiple Criteria Decision Making(MCDM) problems.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Topsis-Rohit-102016087.

```bash
$ pip install Topsis-Rohit-102016087
```
## Usage

topsis 102016087-data.csv "1,1,1,1,1" "+,+,-,+,+" 102016087-result.csv

* To run python program in command line
```bash
$ python 102016087.py 102016087-data.csv "1,1,1,1,1" "+,+,-,+,+" 102016087-result.csv
```
## Input(102016087-data.csv)

| Fund Name	|  P1	|  P2	| P3  |  P4	  |  P5   |
| --------- | ----  | ----  | --- | ----  | ----- |
| M1	    | 0.63	| 0.4	| 6.2 | 53.2  | 15.11 |
| M2	    | 0.71	| 0.5	| 5.8 | 68.2  | 18.8  |
| M3	    | 0.94	| 0.88	| 6.5 | 50.2  | 14.63 |
| M4	    | 0.94	| 0.88	| 4.2 | 68	  | 18.51 |
| M5	    | 0.82	| 0.67	| 4.4 | 56.9  | 15.7  |
| M6	    | 0.74	| 0.55	| 4.9 | 50.2  | 14.1  |
| M7	    | 0.87	| 0.76	| 6	  | 49.4  | 14.26 |
| M8	    | 0.7	| 0.49	| 4.8 | 63.8  | 17.45 |

weights  = [1, 1, 1, 1, 1]
impacts  = [+, +, -, +, +]

## Output(102016087-result.csv)

| Fund Name	|  P1	|  P2	| P3  |  P4	  |  P5   |    Topsis Score     | Rank |
| --------- | ----  | ----  | --- | ----  | ----- | ------------------- | ---- |
| M1	    | 0.63	| 0.4	| 6.2 | 53.2  | 15.11 | 0.09927269186907668 | 8    |
| M2	    | 0.71	| 0.5	| 5.8 | 68.2  | 18.8  | 0.4094342419051654  | 6    |
| M3	    | 0.94	| 0.88	| 6.5 | 50.2  | 14.63 | 0.5833838463228931  | 3    |
| M4	    | 0.94	| 0.88	| 4.2 | 68	  | 18.51 | 0.9823224290605094  | 1    |
| M5	    | 0.82	| 0.67	| 4.4 | 56.9  | 15.7  | 0.5862483969896158  | 2    |
| M6	    | 0.74	| 0.55	| 4.9 | 50.2  | 14.1  | 0.35787822513830764 | 7    |
| M7	    | 0.87	| 0.76	| 6	  | 49.4  | 14.26 | 0.51976734282583    | 4    |
| M8	    | 0.7	| 0.49	| 4.8 | 63.8  | 17.45 | 0.41390792806103543 | 5    |

## License
[MIT](https://choosealicense.com/licenses/mit/)