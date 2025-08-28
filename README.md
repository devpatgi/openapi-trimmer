# OpenAPI Trimmer

⚡ Python / Bash CLI Tool to Trim OpenAPI Paths / Endpoints ⚡

OpenAPI Trimmer is a lightweight tool designed to trim down your OpenAPI files to include only the
endpoints and data transfer objects (DTOs) you care about. This helps in managing large OpenAPI
files by focusing only on the necessary parts for specific tasks.

## Usage

Example usage to make Open API file only for `/v1/quotes` and `/v1/users` APIs,
removing all others and also removing some DTOs:

```bash
openapi-trimmer -i openapi.yaml \
  -p /v1/quotes,/v1/users \
  -ec CompanyConfigDto,UpdateCompanyConfigDto \
  -sc
```

The output will be stored in `openapi-trimmer.yaml`

Pass `-sc` to strip any components not referenced by the selected paths.

At the end validate with:

```bash
swagger-cli validate ./openapi-trimmer.yaml
```

## Install from PyPi

To install check the package on PyPi:

https://pypi.org/project/openapi-trimmer/

```bash
pip install openapi-trimmer
```

## Credits

This tool was inspired from the OpenAPI Endpoint Trimmer JavaScript
tool [openapi-endpoint-trimmer](https://github.com/andenacitelli/openapi-endpoint-trimmer) by
[andenacitelli](https://github.com/andenacitelli).

## Support

If you'd like to support me, you can support me with the "Sponsor" options on the right. Thank you
for your support!

## Contributing

I highly encourage contributions! Create issues and/or PRs for any bugs or features you'd like to
see.

## License

This project is licensed under the MIT license. This basically means you can use it for any purpose,
commercially or not, but I have zero liability.
