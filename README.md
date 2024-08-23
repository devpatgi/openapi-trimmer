# OpenAPI Trimmer

Usage to make Open API file only for Quotes API, 
removing all others and also removing some DTOs:

```bash
./openapi-trimmer.py -i openapi.yaml \
  -p /v1/quotes \
  -ec CompanyConfigDto,CompanyConfigPagedDto,UpdateCompanyConfigDto
```

The output will be stored in `openapi-trimmer.yaml`

At the end validate with:

```bash
swagger-cli validate ./openapi-trimmer.yaml
```
