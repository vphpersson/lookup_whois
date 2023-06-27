#!/usr/bin/env python

from asyncio import run as asyncio_run
from dataclasses import asdict
from json import dumps as json_dumps
from typing import Sequence
from sys import stderr

from lookup_whois import lookup
from lookup_whois.cli import LookupWhoisArgumentParser


async def main():
    args = LookupWhoisArgumentParser().parse_args()

    ip_addresses_input: Sequence[str] | None = args.ip_addresses + list(args.file) if args.file else []

    if not ip_addresses_input:
        print('No IP addresses have been provided.', file=stderr)
        exit(1)

    print(
        json_dumps([
            asdict(whois_data)
            for whois_data in await lookup(ip_addresses=ip_addresses_input)
        ])
    )


if __name__ == '__main__':
    asyncio_run(main())

