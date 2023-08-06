# Wasabit

This package offers a solution for uploading files, creating folders, and authenticating with Wasabi. It contains scripts to simplify file uploads, folder creation, and authentication to the Wasabi environment. Streamline your Wasabi workflows with this package as a starting point for further customization and development.

## Installation

Use the package manager [pip](https://github.com/bippisb/wasabit.git) to install wasabit.

```bash
pip install git+https://github.com/bippisb/wasabit.git
```

## Usage

```python
from wasabit.wasabi_auth import wasabi_auth
from wasabit.wasabi_upload import upload_to_wasabi

# returns 's3 client'
s3 = wasabi_auth()

# 'upload data to wasabi'
upload_to_wasabi(folder_path, bucket_name,wasabi_path)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
