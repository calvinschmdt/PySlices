from datetime import datetime
from dateutil import relativedelta
from tabulate import tabulate
import numpy

class Company():
  
  def __init__(self, company_name):
    self.ledger = []
    self.valuation = 0
    self.company_name = company_name
  
  def get_total_shares(self, classes = ['Common', 'Preferred', 'Option']):
    '''
    Adds up the shares of all the shareholders.
    :param classes: List of strings denoting which classes of shares to get information on.
    :return: Returns integer denoting the number of outstanding shares.
    '''
    
    total_shares = 0
    # Cconsolidates the shares of the shareholders into one list.
    for transaction in self.ledger:
      if transaction['share class'] in classes:
        total_shares += transaction['change in shares']
          
    return total_shares
    
  def get_shareholder_dict(self, classes = ['Common', 'Preferred', 'Option']):
    '''
    Gets the number of shares that each shareholder owns.
    :param classes: List of strings denoting which classes of shares to get information on.
    :returns: Dictionary with shareholder names as keys and the number of shares owned as values.
    '''
    
    shareholder_dict = {}
    # Gets the number of shares each shareholder owns.
    for transaction in self.ledger:
      if transaction['share class'] in classes:
        
        if transaction['shareholder'] in shareholder_dict:
          shareholder_dict[transaction['shareholder']] += transaction['change in shares']
        else:
          shareholder_dict[transaction['shareholder']] = transaction['change in shares']
          
    return shareholder_dict
    
  def get_share_price_dict(self, classes = ['Common', 'Preferred', 'Option']):
    '''
    Gets the amount of money each shareholder paid for their shares.
    :param classes: List of strings denoting which classes of shares to get information on.
    :returns: Dictionary with shareholder names as keys and the amount paid as values.
    '''
    
    shareprice_dict = {}
    # Gets the amount each shareholder paid for their shares.
    for transaction in self.ledger:
      if transaction['share class'] in classes and transaction['shareholder'] != 'Option Pool':
        
        if transaction['shareholder'] in shareprice_dict:
          shareprice_dict[transaction['shareholder']] += transaction['change in shares'] * transaction['share price']
        else:
          shareprice_dict[transaction['shareholder']] = transaction['change in shares'] * transaction['share price']
    
    shareprice_dict['Option Pool'] = 0
          
    return shareprice_dict
          
  def cap_table(self, show_sorted = 'ownership'):
    '''
    Prints a summary of the cap table, giving the share number, % ownership, and value of shares for each shareholder. Will show multiple entries for the same shareholder if they have recieved multiple sets of shares.
    :param show_sorted: Sorts the table by desired parameter. Currently sorts by ownership.
    :return: Does not return anything, but prints to the console.
    '''
    
    total_shares = self.get_total_shares()
    shareholder_dict = self.get_shareholder_dict()
    shareprice_dict = self.get_share_price_dict()
    
    # Assembles and prints the table.
    headers = ['Shareholder', 'Shares', '% of ' + self.company_name, 'Cost of shares', 'Value of shares']
    table = []
    for shareholder in sorted(shareholder_dict.items(), key=lambda x: x[1], reverse = True):
      table.append([shareholder[0], 
        str(shareholder_dict[shareholder[0]]), 
        str(round(shareholder_dict[shareholder[0]] / total_shares * 100, 2)) + '%',
        '$' + str(round(shareprice_dict[shareholder[0]], 2)),
        '$' + str(round(shareholder_dict[shareholder[0]] / total_shares * self.valuation, 2))])
    
    return tabulate(table, headers, tablefmt="simple")
      
  def founding(self, verbose = True, founding_date = datetime(2016, 1, 1, 0, 0), share_value = 0.001, founders_list = []):
    '''
    Records the founders and their equity.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param founding_date: Datetime value denoting the date of founding.
    :param share_value: Float value denoting the nominal value of each share.
    :param founders_list: List of tuples denoting the information on each founder. Each tuple should have 4 values: name (string), number of shares (integer), months of vesting (integer), and months until vesting cliff (integer).
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets values from console and enters them into the shareholders dictionary.
    if verbose:
      self.founding_date = datetime.strptime(input('Date of founding (ex: January 1 2016): '), '%B %d %Y')
      share_value = float(input('Nominal price of share: '))
      
      founders_list = []
      n_founders = int(input('Number of founders: '))
      for i in range(n_founders):
        name = input('Founder name: ').strip()
        n_shares = int(input('Shares issued to ' + name + ': '))
        n_vesting_months = int(input('Shares vesting over X months: '))
        vesting_cliff = int(input('Vesting cliff at X months: '))
        
        founders_list.append((name, n_shares, n_vesting_months, vesting_cliff))
        
    else:
      self.founding_date = founding_date
    
    # Enters founders shares into the ledger. 
    for founder in founders_list:
      
      share_info = {
        'shareholder': founder[0],
        'change in shares': founder[1],
        'share class': 'Common',
        'issue date': self.founding_date,
        'vesting length': founder[2],
        'vesting cliff': founder[3],
        'share price': share_value
        }
        
      self.ledger.append(share_info)
      
  def hiring(self, verbose = True, date = datetime(2016, 1, 1, 0, 0), option_pool = 'y', strike_price = 0.1, employee = ()):
    '''
    Records the disbursement of shares to a new hire.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param date: Datetime value denoting the date of hiring.
    :param option_pool: String of y or n denoting if the shares will be taken from a pre-allocated option pool.
    :param strike_price: Float value denoting the strike price of the shares.
    :param employee: Tuple denoting information on employee. Should have 4 values: name (string), number of shares (integer), months of vesting (integer), and months until vesting cliff (integer).
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets information from console.
    if verbose:
      name = input('Name of hire: ').strip()
      date = datetime.strptime(input('Date of hiring (ex: January 1 2016): '), '%B %d %Y')
      n_shares = int(input('Options issued to ' + name + ': '))
      option_pool = input('Options issued from option pool? (y/n): ')
      n_vesting_months = int(input('Options vesting over X months: '))
      vesting_cliff = int(input('Vesting cliff at X months: '))
      strike_price = float(input('Strike price: '))
    
    # Gets information from passed in variables.
    else:
      name, n_shares, n_vesting_months, vesting_cliff = employee[0], employee[1], employee[2], employee[3]
    
    # Subtracts shares from option pool if necessary.
    shareholder_dict = self.get_shareholder_dict()
    if option_pool == 'y':
      if 'Option Pool' in shareholder_dict:
        if shareholder_dict['Option Pool'] > n_shares:
          share_info = {
            'shareholder': 'Option Pool',
            'change in shares': -n_shares,
            'share class': 'Option',
            }
          
          self.ledger.append(share_info)
        else:
            share_info = {
              'shareholder': 'Option Pool',
              'change in shares': -shareholder_dict['Option Pool'],
              'share class': 'Option',
              }
            
            self.ledger.append(share_info)
    
    # Adds the employee to the ledger.
    share_info = {
      'shareholder': name,
      'change in shares': n_shares,
      'share class': 'Option',
      'issue date': date,
      'vesting length': n_vesting_months,
      'vesting cliff': vesting_cliff,
      'share price': strike_price,
      'options exercised': 0
      }
    
    self.ledger.append(share_info)
    
  def exercising(self, verbose = True, date = datetime(2016, 1, 1, 0, 0), name = '', shares = 0, issue_date = datetime(2016, 1, 1, 0, 0)):
    '''
    Records the exercising of options.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param date: Datetime value denoting the date of exercising.
    :param name: String denoting the name of the employee exercising options.
    :param shares: Integer value denoting how many options to be exercised.
    :param issue_date: Datetime value denoting the date of the options were originally issued.
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets information from console.
    shareholder_dict = self.get_shareholder_dict()
    if verbose:
      name = input('Name of leaver: ')
      while name not in shareholder_dict:
        name = input('Name not recognized. Please input correct name: ')
        
      date = datetime.strptime(input('Date of exercising (ex: January 1 2016): '), '%B %d %Y')
      shares = int(input('Number of shares to exercise: '))
      issue_date = datetime.strptime(input('Date shares were issued (ex: January 1 2016): '), '%B %d %Y')
      
    correct_info = False
    while not correct_info:
      
      # Calculates how many of the employees shares have vested.
      date_found = False
      for e, i in enumerate(self.ledger):
        
        if i['shareholder'] == name and i['share class'] == 'Option' and i['change in shares'] >= 0 and i['issue date'] == issue_date: 
        
          months_worked = relativedelta.relativedelta(date, i['issue date']).months + relativedelta.relativedelta(date, i['issue date']).years * 12
          
          if months_worked < i['vesting cliff']:
            n_shares = 0
          elif months_worked >= i['vesting cliff'] and months_worked < i['vesting length']:
            n_shares = int(months_worked / i['vesting length'] * i['change in shares'])
          elif months_worked >= i['vesting length']:
            n_shares = i['change in shares']
          
          if n_shares - i['options exercised'] >= shares:
            correct_info = True
          else:
            shares = int(input('Invalid number of shares (' + str(n_shares - i['options exercised']) + ' available for exercise). Please input correct number: '))
            break
          
          # Records the how many shares the company is taking back.
          share_info = {
            'shareholder': name,
            'change in shares': -shares,
            'share class': 'Option',
            'share price': i['share price'],
            'leaving date': date
            }
            
          self.ledger.append(share_info)
          
          share_info = {
            'shareholder': name,
            'change in shares': shares,
            'share class': 'Common',
            'share price': i['share price'],
            'exercise date': date
            }
            
          self.ledger.append(share_info)
          
          self.ledger[e]['options exercised'] += shares
    
  def leaving(self, verbose = True, date = datetime(2016, 1, 1, 0, 0), name = ''):
    '''
    Records the leaving of an employee and calculates how many shares have vested.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param date: Datetime value denoting the date of leaving.
    :param employee: String denoting name of employee leaving.
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets information from console.
    shareholder_dict = self.get_shareholder_dict()
    if verbose:
      name = input('Name of leaver: ')
      while name not in shareholder_dict:
        name = input('Name not recognized. Please input correct name: ')
        
      date = datetime.strptime(input('Date of leaving (ex: January 1 2016): '), '%B %d %Y')
    
    # Calculates how many of the employees shares have vested.
    for e, i in enumerate(self.ledger):
      
      if i['shareholder'] == name and 'leaving date' not in i.keys() and 'vesting length' in i.keys(): 
      
        months_worked = relativedelta.relativedelta(date, i['issue date']).months + relativedelta.relativedelta(date, i['issue date']).years * 12
        
        if months_worked < i['vesting cliff']:
          n_shares = 0
        elif months_worked >= i['vesting cliff'] and months_worked < i['vesting length']:
          n_shares = int(months_worked / i['vesting length'] * i['change in shares'])
        elif months_worked >= i['vesting length']:
          n_shares = i['change in shares']
    
        # Records the how many shares the company is taking back.
        share_info = {
          'shareholder': name,
          'change in shares': - (i['change in shares'] - n_shares),
          'share class': i['share class'],
          'share price': i['share price'],
          'leaving date': date
          }
          
        i['leaving date'] = date
          
        self.ledger.append(share_info)

  def convertible_note(self, verbose = True, investment_amount = 0, date = datetime(2016, 1, 1, 0, 0), discount = 0.2, valuation_cap = 0, interest_rate = 0, investor_list = []):
    '''
    Records an convertible note investment.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param investment_amount: Float value denoting the amount of money being invested during that round.
    :param date: Datetime value denoting the date of investment.
    :param discount: Float decimal value denoting the discount on share price the note recieves when it converts.
    :param valuation cap: Float value denoting the maximum pre-money valuation the note can convert at.
    :param interest_rate: Float decimal value denoting the annual interest rate on the note, to be compounded continuously.
    :param investor_list: List of tuples denoting information on each investor in the round. Tuples should have 2 values: name of investor (string), amount of money that investor is contributing (integer).
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets information from the console.
    if verbose:
      date = datetime.strptime(input('Date of investment (ex: January 1 2016): '), '%B %d %Y')
      investment_amount = float(input('Amount invested: '))
      discount = float(input('Discount (%): ')) / 100
      valuation_cap = float(input('Valuation cap: '))
      interest_rate = float(input('Interest rate (%): ')) / 100
      
      investor_list = []
      n_investors = int(input('Number of investors: '))
      for i in range(n_investors):
        name = input('Investor name: ').strip()
        n_invested = float(input('Amount invested by ' + name + ': '))
        
        investor_list.append(name, n_invested)
    
    # Enters info about note into ledger.   
    for investor in investor_list:
      
      share_info = {
        'shareholder': investor[0],
        'share class': 'Note',
        'invested': investor[1],
        'discount': discount,
        'valuation cap': valuation_cap,
        'issue date': date,
        'interest rate': interest_rate
        }
      
      self.ledger.append(share_info)

  def equity_funding(self, verbose = True, pre_money_valuation = 0, investment_amount = 0, date = datetime(2016, 1, 1, 0, 0), preference = 'Preferred', participation = 'y', option_pool = 0, investor_list = []):
    '''
    Records an equity investment.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param pre_money_valuation: Float value denoting the pre-money valuation of the company for the round being raised.
    :param investment_amount: Float value denoting the amount of money being invested during that round.
    :param date: Datetime value denoting the date of investment.
    :param preference: String of Common or Preferred denoting what type of shares will be issued.
    :param participation: String of y or n denoting whether the shares have participation after preference.
    :param option_pool: Integer denoting percentage of the shares that will be reserved for an option pool.
    :param investor_list: List of tuples denoting information on each investor in the round. Tuples should have 2 values: name of investor (string), amount of money that investor is contributing (integer).
    :return: Returns nothing, but modifies the shareholders variable.
    '''
    
    # Gets information from the console.
    if verbose:
      pre_money_valuation = float(input('Pre-money valuation: '))
      investment_amount = float(input('Amount invested: '))
      date = datetime.strptime(input('Date of investment (ex: January 1 2016): '), '%B %d %Y')
      preference = input('Share type (Common/Preferred): ')
      while not (preference == 'Common' or preference == 'Preferred'):
        preference = input('Please input Common or Preferred: ')
        
      if preference == 'Preferred':
        participation = input('Participation? (y/n): ')
      else:
        participation = 'n'
      
      option_pool = float(input('Size of option pool increase (%): '))
    
    # Zero out the option pool, to be filled in later.
    shareholder_dict = self.get_shareholder_dict()
    if 'Option Pool' in shareholder_dict:
      share_info = {
        'shareholder': 'Option Pool',
        'change in shares': -shareholder_dict['Option Pool'],
        'share class': 'Option',
        }
      
      self.ledger.append(share_info)
    
    # Calculates the amount of shares going to new investors and to the option pool.
    investor_fraction = investment_amount / (investment_amount + pre_money_valuation)
    existing_fraction = 1 - investor_fraction - (option_pool / 100)
    
    investor_shares = self.get_total_shares() * investor_fraction / existing_fraction
    option_pool_shares = int(self.get_total_shares() * (option_pool / 100) / existing_fraction)
    
    price_per_share = investment_amount / investor_shares
    
    # Gets information on investors from the console.
    if verbose:
      investor_list = []
      n_investors = int(input('Number of investors: '))
      for i in range(n_investors):
        name = input('Investor name: ').strip()
        n_invested = float(input('Amount invested by ' + name + ': '))
        
        investor_list.append(name, n_invested)
    
    # Enters passed information on the investors into the ledger.   
    for investor in investor_list:
      name = investor[0]
      n_invested = investor[1]
      
      share_info = {
        'shareholder': name,
        'change in shares': int(investor_shares * n_invested / investment_amount),
        'share class': preference,
        'share price': price_per_share,
        'participation': participation,
        'invested': n_invested,
        'issue date': date
        }
        
      self.ledger.append(share_info)
    
    # Enters option pool information into the ledger.
    share_info = {
      'shareholder': 'Option Pool',
      'change in shares': int(option_pool_shares),
      'share class': 'Option',
      }
      
    self.ledger.append(share_info)
    
    # Converts any outstanding ntoes into equity.
    for transaction in self.ledger:
      if transaction['share class'] == 'Note' and 'conversion date' not in transaction.keys():
        
        # Calculates whether the note will be converted based on discount or valuation cap.
        capped_share_price = (transaction['valuation cap'] / pre_money_valuation) * price_per_share
        discount_share_price = price_per_share * (1 - transaction['discount'])
        if discount_share_price < capped_share_price:
          share_price = discount_share_price
        else:
          share_price = capped_share_price
        
        # Calculates how much interest has accrued.
        n_years = relativedelta.relativedelta(date, transaction['issue date']).years + relativedelta.relativedelta(date, transaction['issue date']).months / 12
        n_invested = transaction['invested'] * numpy.exp(transaction['interest rate'] * n_years)
      
        share_info = {
          'shareholder': transaction['shareholder'],
          'change in shares': int(n_invested / share_price),
          'share class': preference,
          'share price': transaction['invested'] / int(n_invested / share_price),
          'participation': participation,
          'invested': transaction['invested'],
          'issue date': date
          }
          
        self.ledger.append(share_info)
        
        transaction['conversion date'] = date
    
    self.valuation = pre_money_valuation + investment_amount
    
  def acquisition(self, verbose = True, sale_price = 0):
    '''
    Prints out the amount that each shareholder would recieve from an acquisition.
    :param verbose: Boolean value denoting whether the certain variables are passed into the function or entered into the console.
    :param sale_price: Float value denoting the price paid to acquire all shares of the company.
    '''
    
    # Gets information from the console.
    if verbose:
      sale_price = float(input('Sale price ($): '))
    
    shareholder_dict = self.get_shareholder_dict()   
    if 'Option Pool' in shareholder_dict:
      share_info = {
        'shareholder': 'Option Pool',
        'change in shares': -shareholder_dict['Option Pool'],
        'share class': 'Option',
        }
      
      self.ledger.append(share_info)
    price_per_share = sale_price / self.get_total_shares()
    
    # Gets the amount paid in in each equity funding round, and makes the decision on whether preferred shares will be converted.
    rounds_dict = {}
    payout_dict = {}
    for transaction in self.ledger:
      
      if transaction['shareholder'] not in payout_dict:
        payout_dict[transaction['shareholder']] = 0
      
      if transaction['share class'] == 'Preferred':
        if transaction['participation'] == 'y' or price_per_share <= transaction['share price']:
          if transaction['participation'] == 'y':
            transaction['share class'] = 'Common'
          if transaction['issue date'] in rounds_dict:
            rounds_dict[transaction['issue date']].append((transaction['shareholder'], transaction['invested']))
          else:
            rounds_dict[transaction['issue date']] = [(transaction['shareholder'], transaction['invested'])]
        
        else:
          transaction['share class'] = 'Common'
    
    # Moves through the different preferred tiers to disburse that money first.
    amount_left = sale_price
    for r in sorted(rounds_dict, reverse = True):
      
      if amount_left > 0:
        round_sum = sum([i[1] for i in rounds_dict[r]])
        
        if round_sum > amount_left:
          for investor in rounds_dict[r]:
            payout_dict[investor[0]] += investor[1] / round_sum * amount_left
          amount_left = 0
        else:
          for investor in rounds_dict[r]:
            payout_dict[investor[0]] += investor[1]
          amount_left -= round_sum
    
    # Calculates price of each share. 
    total_shares = self.get_total_shares(['Common', 'Option'])
    share_price = amount_left / total_shares
    
    # Disburses the rest of the money to common shareholders.
    shareholder_dict = self.get_shareholder_dict(['Common', 'Option'])
    for shareholder in shareholder_dict:
      payout_dict[shareholder] += share_price * shareholder_dict[shareholder]
    
    shareprice_dict = self.get_share_price_dict()
    # Assembles and prints the table.
    headers = ['Shareholder', 'Cost of shares ($)', 'Payout ($)', 'Return (%)']
    table = []
    for shareholder in sorted(payout_dict.items(), key=lambda x: x[1], reverse = True):
      if shareholder[0] != 'Option Pool':
        table.append([shareholder[0], 
          '$' + str(round(shareprice_dict[shareholder[0]], 2)),
          '$' + str(round(payout_dict[shareholder[0]], 2)), 
          str(round((payout_dict[shareholder[0]] / shareprice_dict[shareholder[0]] - 1) * 100, 2)) + '%' ])
        
    return tabulate(table, headers, tablefmt="simple")
