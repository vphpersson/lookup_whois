from asyncio import open_connection
from typing import Sequence, Final
from dataclasses import dataclass

_WHOIS_HOST: Final[str] = 'bgp.tools'
_WHOIS_PORT: Final[int] = 43


@dataclass
class WhoisData:
    as_number: str
    as_name: str
    allocated_date: str
    registry: str
    country: str
    ip_address: str
    ip_network: str


async def lookup(ip_addresses: Sequence[str]) -> list[WhoisData]:

    reader, writer = await open_connection(host=_WHOIS_HOST, port=_WHOIS_PORT)
    writer.write(b'begin\n' + b'\n'.join(map(str.encode, ip_addresses)) + b'\nend')
    await writer.drain()

    whois_data_lines: list[str] = (await reader.read()).decode().splitlines()

    return [
        WhoisData(
            as_number=whois_data_arr[0].strip(),
            as_name=whois_data_arr[6].strip(),
            allocated_date=whois_data_arr[5].strip(),
            registry=whois_data_arr[4].strip(),
            country=whois_data_arr[3].strip(),
            ip_address=whois_data_arr[1].strip(),
            ip_network=whois_data_arr[2].strip()
        )
        for whois_data_line in whois_data_lines
        if (whois_data_arr := whois_data_line.split('|'))
    ]
