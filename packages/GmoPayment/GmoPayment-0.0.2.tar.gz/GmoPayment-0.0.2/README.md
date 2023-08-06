[![PyPI version](https://img.shields.io/pypi/v/GmoPayment.svg)](https://pypi.python.org/pypi/GmoPayment)

# GmoPayment Python PyPackage

Python API Client for GMO Payment Gateway

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install GmoPayment
```
# Usage

Sample calling ExecTran.idPass

```python
from GmoPayment import Gateway

gmopg = Gateway(timeout=10, production=True)
try:
    response = gmopg.tran.execute(
        {'ShopID': 'your-shop-id', 'ShopPass': 'your-shop-pass', 'OrderID': 'your-order-id': '1234', 'JobCD': '1234'})
    except ResponseError as e:
    print(e)
else:
    print(response.data)
```

Parameter names conform to payment gateway specifications.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
