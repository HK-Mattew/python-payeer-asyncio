import re


async def validate_account(wallet):
    if not re.match("^[Pp]{1}[0-9]{7,15}|.+@.+\..+$", wallet):
        raise ValueError('Wrong account format!')
    

