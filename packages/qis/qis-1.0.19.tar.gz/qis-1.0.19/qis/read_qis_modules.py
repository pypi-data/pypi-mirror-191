import qis.portfolio.multi_portfolio_data
this = dir(qis.portfolio.multi_portfolio_data)
print(this)
for x in this:
    if not any(y in x for y in ['__', 'Dict']):
        print(f"{x},")


print('##############################')
import inspect

all_functions = inspect.getmembers(qis.portfolio.multi_portfolio_data, inspect.isfunction)
for x in all_functions:
    if not any(y in x for y in ['run_unit_test', 'njit', 'NamedTuple', 'dataclass', 'skew', 'kurtosis', 'abstractmethod']):
        print(f"{x[0]},")