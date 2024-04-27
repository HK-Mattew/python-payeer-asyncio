# AsyncIO Payeer Client

Implementation of AsyncIO Client for Payeer API.

Before use, it is advisable to familiarize yourself with the official Payeer documentation (https://payeercom.docs.apiary.io/). The application implements the interaction protocol described in this document.

## Installation

```
pip install git+https://github.com/HK-Mattew/python-payeer-asyncio
```

## Example of use

```python
from payeer_asyncio import PayeerAsyncIO
import asyncio



async def main():


    payeer = PayeerAsyncIO(
        account='<your-account>',
        apiId='<your-api-id>',
        apiPass='<your-api-pass>'
    )


    balance = await payeer.get_balance()

    print(balance)




if __name__ == "__main__":
    asyncio.run(main())
```