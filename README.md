# OpenAPI Trimmer

Usage to make Open API file only for Quotes API,
removing all others and also removing some DTOs:

```bash
openapi-trimmer -i openapi.yaml \
  -p /v1/quotes \
  -ec CompanyConfigDto,CompanyConfigPagedDto,UpdateCompanyConfigDto
```

The output will be stored in `openapi-trimmer.yaml`

At the end validate with:

```bash
swagger-cli validate ./openapi-trimmer.yaml
```

## PyPi

To install check the package on PyPi:

https://pypi.org/project/openapi-trimmer/

```bash
pip install openapi-trimmer
```
