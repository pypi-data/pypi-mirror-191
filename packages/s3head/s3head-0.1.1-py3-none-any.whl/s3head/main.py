import configparser
import os
from typing import Union

import boto3
import click
from smart_open import open


class LoadS3Config:
    def __init__(
        self, s3cfg_path: Union[str, bytes, os.PathLike] = os.path.expanduser("~/.s3cfg")
    ):
        try:
            with open(s3cfg_path) as fp:
                s3cfg_file = configparser.ConfigParser()
                s3cfg_file.read_file(fp)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Please create `.s3cfg` to the `s3dfg_path`. Try `s3cmd --configure`"
            )

        s3cfg = s3cfg_file["default"]
        self.s3cfg = s3cfg_file["default"]
        self.AWS_ACCESS_KEY_ID = s3cfg["access_key"]
        self.AWS_SECRET_ACCESS_KEY = s3cfg["secret_key"]
        self.AWS_S3_ENDPOINT_URL = f"https://{s3cfg['host_base']}"
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            endpoint_url=self.AWS_S3_ENDPOINT_URL,
        )
        self.transport_params = dict(client=self.client)


@click.command
@click.argument("uri")
@click.option("-n", "--num-lines", type=int, default=10, help="lines")
@click.option("-c", "--count-byte", type=int, help="bytes")
@click.option("--config", help="Path to the `.s3cfg`")
def main(uri: str, num_lines: int, count_byte: int, config: str) -> None:
    if config:
        transport_params = LoadS3Config(s3cfg_path=config).transport_params
    else:
        transport_params = LoadS3Config().transport_params

    if count_byte:
        raise NotImplementedError("Byte count is not Implemented yet.")

    with open(uri, transport_params=transport_params) as fp:
        is_break = False
        for i, line in enumerate(fp):
            if i > num_lines - 1:
                is_break = True
                break
            print(line, end="")
        if not is_break:
            print("")


if __name__ == "__main__":
    main()
