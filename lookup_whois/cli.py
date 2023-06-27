from argparse import ArgumentParser, FileType


class LookupWhoisArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(description='Lookup Whois information about IP addresses from bgp.tools.') | kwargs
            )
        )

        self.add_argument(
            'ip_addresses',
            help='IP addresses about which to retrieve Whois information',
            nargs='*'
        )

        self.add_argument(
            '--file',
            help='The path of a file from which to read IP addresses',
            type=FileType('r')
        )
