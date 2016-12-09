=========================
 PySlices
=========================

This package provides users with a simple Python object to track how the shares of a small company are allocated through founding, hiring, and investing, as well as how those shares translate to a payout upon acquisition.

This package is not meant to legally track the exact number of shares in your company. It is relatively simple and won't be able to accurately handle all cases where shares are allocated.

Use cases:
	- As a founder or potential hire, track how your shares may be diluted during the fundraising process, and how the presence of preferred stock affects your outcomes upon acquisition at various prices.
	- As a potential investor, determine how your returns depend on future dilutions and acquisition prices.

Project Setup
=============

Dependancies
------------

Full support for Python 3. Will not work for earlier versions.

Requires tabulate (tested on version 0.7.7). Installation instructions `here<https://pypi.python.org/pypi/tabulate>`_ .

Installation
------------

1. Either download and extract the zipped file, or clone directly from github using::

    git clone https://github.com/calvinschmdt/PySlices.git PySlices

   This should create a new directory containing the required files.
    
2. Install the dependancies manually or by running this command while in the easy_tensorflow directory::

    sudo pip3 install -r requirements.txt

3. Install the project by running this command while in the easy_tensorflow directory::

    sudo python3 setup.py install
    
Usage
=====

Company Object
------------------

This package uses the Company object to maintain a ledger of share changes over the life of the company. This ledger can be directly changed by adding to the Company.ledger list, or by using custom functions that represent events that would change the ownership makeup of the company. The information for these functions can be entered into the console in response to prompts, or into the function directly during calling.

Instantiation
-------------

Instantiate the object by assigning it to a variable. The only required argument for instantiation is a string that gives the name of the company::

    from PySlices.company import Company
    from datetime import datetime

    new_corp = Company('Nights Watch Security')
        
Founding
--------

Founders are assigned shares. These shares may vest monthly over a specific amount of months and with a cliff after a certain amount of months, starting at the founding date. The arguments to pass into the founding function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - founding_date: Datetime value denoting the date of founding.
    - share_value: Float value denoting the nominal value of each share.
    - founders_list: List of tuples denoting the information on each founder. Each tuple should have 4 values: name (string), number of shares (integer), months of vesting (integer), and months until vesting cliff (integer).
Ex - Two founders, one recieves 60% of the company, the other recieves 40%. Both have their shares vest over 4 years with a 1 year cliff. The nominal price per share is $0.001::

    new_corp.founding(False, datetime(2000, 1, 1, 0, 0), 0.001, [('Jon', 6000, 48, 12), ('Sam', 4000, 48, 12)]) 
    
Hiring
--------

New hires are assigned options. These options may vest monthly over a specific amount of months and with a cliff after a certain amount of months, starting at the date of hiring. The arguments to pass into the hiring function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - date: Datetime value denoting the date of hiring.
    - option_pool: String of y or n denoting if the shares will be taken from a pre-allocated option pool. If there is no option pool, or not enough shares in the option pool, then any extra shares that cannot be taken from the option pool will be issued from the company.
    - strike_price: Float value denoting the strike price of the shares.
    - employee: Tuple denoting information on employee. Should have 4 values: name (string), number of shares (integer), months of vesting (integer), and months until vesting cliff (integer).
Ex - Hiring a new employee, to recieve 1,000 shares vesting over 4 years with a 1 year cliff. The strike price on these options is $0.01::

    new_corp.hiring(False, datetime(2000, 2, 1, 0, 0), 'y', .01, ('Davos', 1000, 48, 12)) 
    
Exercising options
--------

Conversion of oustanding options to common shares. Will make sure that the number of shares being converted is an allowable number, passed on how many options have vested and been exercised previously. The arguments to pass into the exercising function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - date: Datetime value denoting the date of exercising.
    - name: String denoting the name of the employee exercising options.
    - shares: Integer value denoting how many options to be exercised.
    - issue_date: Datetime value denoting the date of the options were originally issued.
Ex - Employee exercises 200 of options::

    new_corp.exercising(False, datetime(2001, 2, 1, 0, 0), 'Davos', 200, datetime(2000, 2, 1, 0, 0))

Leaving
--------

Retiring of shares that have not vested. The arguments to pass into the leaving function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - date: Datetime value denoting the date of leaving.
    - employee: String denoting name of employee leaving.
Ex - Employee leaves and exercises the rest of their options::

    new_corp.leaving(False, datetime(2002, 2, 1, 0, 0), 'Davos')
    new_corp.exercising(False, datetime(2002, 2, 1, 0, 0), 'Davos', 300, datetime(2000, 2, 1, 0, 0))

Raising a convertible note
--------

Raising money that will convert to equity upon the next equity round. The arguments to pass into the convertible_note function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - investment_amount: Float value denoting the amount of money being invested during that round.
    - date: Datetime value denoting the date of investment.
    - discount: Float decimal value denoting the discount on share price the note recieves when it converts.
    - valuation cap: Float value denoting the maximum pre-money valuation the note can convert at.
    - interest_rate: Float decimal value denoting the annual interest rate on the note, to be compounded continuously.
    - investor_list: List of tuples denoting information on each investor in the round. Tuples should have 2 values: name of investor (string), amount of money that investor is contributing (integer).
Ex - Raising $2,000 on a convertible note from one investor. This note will convert at a discount of 20% on the next equity round with a pre-money valuation cap of $40,000 and an annual interest rate of 7%::

    new_corp.convertible_note(False, 2000, datetime(2003, 1, 1, 0, 0), 0.20, 40000, 0.07, [('Iron Bank Ventures', 2000)])

Raising an equity round
--------

Raising money by issuing shares. Will first calculate the number of shares to issue based on the funders in the equity round, followed by the conversion of any outstanding notes, based on the price paid for each new share by the equity investors. The arguments to pass into the equity_funding function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - pre_money_valuation: Float value denoting the pre-money valuation of the company for the round being raised.
    - investment_amount: Float value denoting the amount of money being invested during that round.
    - date: Datetime value denoting the date of investment.
    - preference: String of Common or Preferred denoting what type of shares will be issued.
    - participation: String of y or n denoting whether the shares have participation after preference.
    - option_pool: Integer denoting percentage of the shares that will be reserved for an option pool.
    - investor_list: List of tuples denoting information on each investor in the round. Tuples should have 2 values: name of investor (string), amount of money that investor is contributing (integer).
Ex - Raising $10,000 on from two investors at a pre-money valuation of $50,000 and a 15% option pool. The issued shares will be preferred with participation::

    new_corp.equity_funding(False, 50000, 10000, datetime(2004, 1, 1, 0, 0), 'Preferred', 'y', 15, [('Iron Bank Ventures', 6000), ('Golden Lion Capital', 4000)])
    
Capitalization table
--------

Determining how much of the company each shareholder owns. May not be the percentage paid back during a liquidation depending on the preference of shares and how many are unassigned (in the option pool).
 The arguments to pass into the cap_table function:
    - show_sorted: Sorts the table by desired parameter. Currently sorts by ownership.
Ex::

    print(new_corp.cap_table())
    
    Shareholder            Shares  % of Nights Watch Security    Cost of shares    Value of shares
    -------------------  --------  ----------------------------  ----------------  -----------------
    Jon                      6000  37.38%                        $6.0              $22429.91
    Sam                      4000  24.92%                        $4.0              $14953.27
    Option Pool              2304  14.36%                        $0                $8613.08
    Iron Bank Ventures       2222  13.84%                        $7997.71          $8306.54
    Golden Lion Capital      1024  6.38%                         $3998.48          $3828.04
    Davos                     500  3.12%                         $5.0              $1869.16    

Liquidation through acquisition
--------

Liquidating the company in return for a specific amount of money, to be paid in a lump sum. Will disburse money to shareholder based on order of preference and participation, returning a table showing how much each shareholder is recieving. The arguments to pass into the acquisition function:
    - verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    - sale_price: Float value denoting the price paid to acquire all shares of the company.
Ex - Selling the company for $100,000::

    print(new_corp.acquisition(False, 100000))

    Shareholder          Cost of shares ($)    Payout ($)    Return (%)
    -------------------  --------------------  ------------  ------------
    Jon                  $6.0                  $38411.17     640086.24%
    Sam                  $4.0                  $25607.45     640086.24%
    Iron Bank Ventures   $7997.71              $22224.94     177.89%
    Golden Lion Capital  $3998.48              $10555.51     163.99%
    Davos                $5.0                  $3200.93      63918.62%

Licenses
========

The code which makes up this Python project template is licensed under the MIT/X11 license. Feel free to use it in your free software/open-source or proprietary projects.

Issues
======

Please report any bugs or requests that you have using the GitHub issue tracker!

Development
===========

If you wish to contribute, first make your changes. Then run the following from the project root directory::

    source internal/test.sh

This will copy the template directory to a temporary directory, run the generation, then run tox. Any arguments passed will go directly to the tox command line, e.g.::

    source internal/test.sh -e py27

This command line would just test Python 2.7.

Acknowledgements
================

Thank you to the tabulate team for creating such an easy-to-use package.

This package was set up using Sean Fisk's Python Project Template package.

Authors
=======

* Calvin Schmidt
