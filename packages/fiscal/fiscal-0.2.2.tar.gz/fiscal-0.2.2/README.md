# Fiscal
## A simple, systematic tax liability calculator

Fiscal is a simple, systematic tax calculator with soft-coded rate bands.  Specifically, Fiscal aims to side-step the commonly-seen behaviour of using 'if' statements in tax calculators, and relying on hard-coded tax bands. 

### Fiscal, broken down

There are two key elements to Fiscal.

1) Bands - a stream of pairwise tuples (a threshold, a percentage) with an 'allocator'. The allocator dictates the manner in which taxable amounts are allocated between the threshold element of each band - the two predominant forms of allocator are provided:
    - 'step', which reflects the most common allocation; and 
    - 'slab', which represents taxes for which the sole applicable rate is determined by the taxable amount (as in old stamp duty and early SDLT).

2) Liabilities - a calculation of liability stored in a 'breakdown' - a three-element tuple made up of: 
    - the amount allocated to the band;
    - the percentage referable to that band; and
    - the product of the amount and the percentage.

## Allocators - examples
To draw an example from Stamp Duty Land Tax (SDLT), a land transfer tax in England (and previously throughout the UK).

### SDLT - stepped calculation

The applicable bands for a commercial transaction were, after 17 March 2017, as follows:

| Threshold | Percentage |
|-----------|------------|
| £150,000  | 0%         |
| £100,000  | 2%         |
| Surplus   | 5%         |

This can be represented by a band as follows:

``` python-console
stepped_bands = SteppedBands(((150_000, 0),(100_000, 2),("Infinity", 5)))
```


The bands are allocated on the step basis, so £1m would be allocated as follows:

| Threshold | Percentage | Liability |
|-----------|------------|-----------|
| £150,000  | 0%         | £0        |
| £100,000  | 2%         | £2,000    |
| £750,000  | 5%         | £37,500   |

``` python-console
allocation = stepped_bands.allocate(1_000_000)
assert allocation == (
    (Decimal("150000"), Decimal("0")),
    (Decimal("100000"), Decimal("2")),
    (Decimal("750000"), Decimal("5")),
) # True

```


The allocation is intended to be called within an instance of the Liability object.


### SDLT - slabbed calculation

Prior to 17 March 2017, the applicable SDLT rates for a commercial transaction were as follows:

| Threshold | Percentage |
|-----------|------------|
| £150,000  | 0%         |
| £100,000  | 1%         |
| £250,000  | 3%         |
| Surplus   | 4%         |

The bands were allocated on the 'slab' basis. This means that the taxable amount is compared with the __cumulative__ thresholds, which are as follows:

| Cumulative Threshold | Percentage |
|----------------------|------------|
| £150,000             | 0%         |
| £250,000             | 1%         |
| £500,000             | 3%         |
| Surplus              | 4%         |

The first cumulative threshold to equal or exceed the taxable amount determines the applicable percentage.  So where the taxable amount was £200,000, the applicable percentage was **1%**.

| Cumulative Threshold | Amount   | Percentage |
|----------------------|----------|------------|
| £150,000             |          | 0%         |
| £250,000             | £200,000 | 1%         |
| £500,000             |          | 3%         |
| Surplus              |          | 4%         |

Where the taxable amount was £300,000, the applicable percentage was **3%**.

| Cumulative Threshold | Amount   | Percentage |
|----------------------|----------|------------|
| £150,000             |          | 0%         |
| £250,000             |          | 1%         |
| £500,000             | £300,000 | 3%         |
| Surplus              |          | 4%         |

Thresholds were inclusive, so where the taxable amount was £500,000, the applicable percentage was still **3%**.

| Cumulative Threshold | Amount   | Percentage |
|----------------------|----------|------------|
| £150,000             |          | 0%         |
| £250,000             |          | 1%         |
| £500,000             | £500,000 | 3%         |
| Surplus              |          | 4%         |

But where the taxable amount was £500,001, the applicable percentage was **4%**.

| Cumulative Threshold | Amount   | Percentage |
|----------------------|----------|------------|
| £150,000             |          | 0%         |
| £250,000             |          | 1%         |
| £500,000             |          | 3%         |
| Surplus              | £500,001 | 4%         |

## Liabilities - examples

Liabilities represent the calculation the follows the allocation of a taxable amount into the correct bands. 

Those liabilities are then aggregated into a total liability.
So by way of example, if calculating the current (9 February 2022) SDLT liability (non-residential property) for a £1m sum, the steps would be as follows.

``` python-console
bands = SteppedBands((150_000, 0),(100_000, 2),("Infinity", 5))
liab = Liability(bands=bands, amount=1_000_000)
```
The breakdown of liability would look as below:

``` python-console
assert liab.breakdown == (
        (Decimal("150000"), Decimal("0"), Decimal("0")),
        (Decimal("100000"), Decimal("2"), Decimal("2000")),
        (Decimal("750000"), Decimal("5"), Decimal("37500")),
    ) # True
assert liab.total == Decimal("39500") # True
```
