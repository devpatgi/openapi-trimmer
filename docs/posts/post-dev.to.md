### Simplifying Your OpenAPI Files with OpenAPI Trimmer

Managing large OpenAPI files can be a hassle, especially when you only need a small portion of the
API for specific tasks. This is where **OpenAPI Trimmer** comes in handy. It's a lightweight tool
designed to trim down your OpenAPI files to include only the endpoints and data transfer objects (
DTOs) you care about.

#### How Does It Work?

Let's say you're working with a large OpenAPI file, but you only need the endpoints related to the
Quotes API. You can easily extract just those endpoints and remove irrelevant DTOs with a single
command:

```bash
openapi-trimmer -i openapi.yaml \
  -p /v1/quotes,/v1/users \
  -ec CompanyConfigDto,CompanyConfigPagedDto
```

This command will:

- **-i openapi.yaml**: Use your existing OpenAPI YAML file as input.
- **-p /v1/quotes,/v1/users**: Keep only the endpoints starting with `/v1/quotes` and `/v1/users`.
- **-ec CompanyConfigDto,CompanyConfigPagedDto**: Exclude specific components, in this case,
  the `CompanyConfigDto`, and `CompanyConfigPagedDto`.

The trimmed API definition will be saved as `openapi-trimmer.yaml`.

#### Validation

To ensure the integrity of your trimmed OpenAPI file, validate it with:

```bash
swagger-cli validate ./openapi-trimmer.yaml
```

This step helps catch any issues before you deploy or share the trimmed API file.

#### Installation

You can install OpenAPI Trimmer directly from PyPi:

```bash
pip install openapi-trimmer
```

For more details and the latest updates, visit
the [OpenAPI Trimmer PyPi page](https://pypi.org/project/openapi-trimmer/).

GitHub repository: [OpenAPI Trimmer on GitHub](https://github.com/idachev/openapi-trimmer).

#### Command-Line Options

The OpenAPI Trimmer offers several options to customize its operation:

- **-h, --help**: Show help information.
- **-v, --version**: Display the version number.
- **-i INPUT, --input INPUT**: Specify the input YAML file (required).
- **-o OUTPUT, --output OUTPUT**: Define the output file name (optional; defaults to appending '
  -trimmed' to the input file).
- **-p PREFIXES, --prefixes PREFIXES**: List the paths to retain in the output (comma-separated).
- **-ec EXCLUDE_COMPONENTS, --exclude-components EXCLUDE_COMPONENTS**: List the components to
  exclude (comma-separated).

#### Conclusion

OpenAPI Trimmer is an essential tool for developers looking to streamline their OpenAPI files,
making them more manageable and tailored to specific needs. Whether you're preparing API
documentation or simplifying an API for internal use, OpenAPI Trimmer saves you time and effort by
focusing only on what matters most to you.
