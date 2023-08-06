# s3head

`s3head` is the `head` command for AWS S3.

## Install
```
pip install s3head
```
If you use pipx, it's nice to install by it.

```
pipx iinstall s3head
```
## Usage
Before using, create `.s3cfg` file by `s3cmd --configure`. See [s3cmd](https://github.com/s3tools/s3cmd)
```
Usage: s3head [OPTIONS] URI

Options:
  -n, --num-lines INTEGER   lines
  -c, --count-byte INTEGER  bytes
  --config TEXT             Path to the `.s3cfg`
  --help                    Show this message and exit.
```

For example,
```
s3head -n 100 s3://your_bucket/your_file.txt
```