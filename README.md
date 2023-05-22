# Welcome
This repository accompanies the "Elections and Psephology" chapter of Ben "LeBoot" LeBoutillier's groundbreaking book titled [*Practical Advice for a Better World*](https://benleboutillier.com/books/Practical_Advice).

# Overview
In my book, I argue that *Ranked-Choice Voting* (RCV, or *Single Transferrable Vote* (STV)) is a fantastic voting system that must be adopted as society attempts to create a better world.

### Voting Systems
The system we currently use is called *Winner Take All* or *First Past the Post* (FPTP); in it, every voter gets one vote, and the candidate with the most votes wins. This system is fraught with problems, not the least of which is that it inevitably results in a two-party system.

STV is a system in which voters *rank* the candidates on their ballots. One, two, or all candidates can be ranked. First, everyone's first choices are tallied; if a winner does not emerge, the candidate with the fewest votes is dropped, and the process repeats itself.

STV can be used for one-winner or multiple-winner elections. It does not punish voting for small-party candidates, and consequently it does not force a two-party system.

A more detailed discussion occurs in [*Practical Advice*](https://benleboutillier.com/books/Practical_Advice).

CPG Grey uses [these short videos](https://www.cgpgrey.com/politics-in-the-animal-kingdom/) to explains the process smoothly. 

### This Repository
In [*Practical Advice for a Better World*](https://benleboutillier.com/books/Practical_Advice), I make the following claim: "With the transparency of the system, you could determine the election results yourself if you had the time and some light programming skills." This repository is intended to 1) prove that point, and 2) provide a visual for those who can't quite envision what I've described.

As a professional data engineer, I don't have a good sense for what would be considered "light" programming skills, but the core of what you find here only took about an hour to write and test.

**[This file](./stv.ipynb) overviews the process** and displays results. **[This file](./Election.py) is the underlying code** and makes it happen.

# About

### For Non-Technical People
What you're looking at is a *GitHub repository*. This is a place for keeping and viewing code. Navigate it like you would a website or file explorer on your laptop. [This file](./stv.ipynb) is light on code, easy-to-read, and has a good overview of how simple the process can be.

If you dig into [this file](./Election.py), the code can look quite intimidating. Nevertheless, I've added comments throughout to help both you and me understand it better.

### For Technical People
Everything herein is written using Python. The *Election* class (defined in [Election.py](Election.py)) contains all the properties and methods needed to run the process start to finish, as demonstrated in [this Jupyter notebook](./stv.ipynb).

I used Pandas dataframes for this repo because they can be used anywhere. With potentially hundreds of millions of real-word ballots, I appreciate that spark might be a better approach.

*Election's* `__init__()` method can take an existing dataframe; but by default, it will create 10,000 randomly-generated ballots for a 8-candidate election. The particulars are described using inline comments.

The key to making this process work is this line of code from the `analyze_ballots()` method and uses [pandas.DataFrame.bfill](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.bfill.html):
```python
df = df.bfill(axis=1).dropna(axis=0, how='all')
```
`bfill(axis=1)` (alias for `fillna(method='bfill', axis=1)`) fills a `NaN` values with the nearest nonnull value to it's right.

Because the dataframe has columns `Choice_1`, `Choice_2`, etc. from left to right, if `Choice_1` is `NaN`, then `Choice_1` is replaced with the value from `Choice_2`.

Similarly, when candidates who are *not* a given voter's first choice are dropped, the next-in-line "moves up" to fill that gap. For example:
```console
Iteration 1:
Ballot: (A, B, C, D, None, ...)

Iteration 2; suppose Candidate C has been dropped:
Ballot: (A, B, D, D, None, ...)

Iteration 3: suppose Candidate A has been dropped:
Ballot: (B, B, D, D, None, ...)

Iteration 4: suppose Candidate B has been dropped:
Ballot: (D, D, D, D, None, ...)

Iteration 5: suppose Candidate D has been dropped:
Ballot: (None, None, ...)
```

The analysis itself happens in a `while` loop that breaks when the needed number of winners has emerged:
```python
while True:
    # Backfill df then drop entirely-NaN rows
    # Get value counts for Choice_1
    # Check if anyone got the necessary percentage of votes:
        # If yes, count that person as a winner then drop from remaining options
            # 'return' if needed number of winners has been met
        # If no, drop candidate(s) with count == min_count
    # (Back to top of loop)
```