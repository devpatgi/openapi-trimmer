#!/usr/bin/env python3

import argparse
import os
import sys
from collections import OrderedDict
from importlib.metadata import version, PackageNotFoundError

import yaml


class OrderedDumper(yaml.SafeDumper):
    pass


def dict_representer(dumper, dict_data):
    return dumper.represent_dict(dict_data.items())


OrderedDumper.add_representer(OrderedDict, dict_representer)


def get_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


def parse_args():
    parser = argparse.ArgumentParser(description="OpenAPI Trimmer")

    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {get_version("openapi-trimmer")}')

    parser.add_argument('-i', '--input', type=str, required=True,
                        help="Input YAML File (Required).")

    parser.add_argument('-o', '--output', type=str, required=False,
                        help="Output YAML File (Optional) If missing will "
                             "append '-trimmed' to input file path.")

    parser.add_argument('-p', '--prefixes', type=str, required=True,
                        help="A comma-separated, zero-spaces list of paths "
                             "to keep. (Ex. /v1/users,/v1/organizations)")

    parser.add_argument('-ec', '--exclude-components', type=str,
                        required=False,
                        help="A comma-separated, zero-spaces list of "
                             "components names to exclude."
                             " (Ex. CompanyConfigDto,CompanyItemDto)")

    parser.add_argument('-sc', '--strip-components', action='store_true',
                        help="Remove components not referenced by the"
                             " selected paths.")

    return parser.parse_args()


def read_yaml(input_path):
    print(f"\nReading input file: {input_path}")

    has_yaml_doc_separator = False

    with open(input_path, 'r') as file:
        line = file.readline().strip()

        if line == "---":
            has_yaml_doc_separator = True

        file.seek(0)

        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing input file: {e}")
            sys.exit(1)

    return data, has_yaml_doc_separator


def trim_yaml(prefixes, exclude_components, strip_components, data):
    prefixes = prefixes.split(",")

    prefixes = [prefix.strip() for prefix in prefixes if prefix.strip()]

    print(f"\nTrimming to just paths: {', '.join(prefixes)}")

    paths = {path: value for path, value in data.get('paths', {}).items() if
             any(path.startswith(retain) for retain in prefixes)}

    paths_tags = set()
    for path, value in paths.items():
        for method, method_value in value.items():
            paths_tags.update(method_value.get('tags', []))

    data['paths'] = paths

    if 'tags' in data:
        data['tags'] = [tag for tag in data['tags'] if
                        tag['name'] in paths_tags]

    if exclude_components:
        exclude_components = exclude_components.split(",")

        exclude_components = [exclude_component.strip() for exclude_component
                              in exclude_components if
                              exclude_component.strip()]

        print(f"\nExclude components: {', '.join(exclude_components)}")

        if 'components' in data:
            for component in exclude_components:
                if component in data['components']['schemas']:
                    del data['components']['schemas'][component]

    if strip_components and 'components' in data:
        data = strip_unreferenced_components(data)

    return data


def find_component_refs(node, refs):
    if isinstance(node, dict):
        ref = node.get('$ref')
        if isinstance(ref, str) and ref.startswith('#/components/'):
            parts = ref.split('/')
            if len(parts) >= 4:
                refs.setdefault(parts[2], set()).add(parts[3])
        for value in node.values():
            find_component_refs(value, refs)
    elif isinstance(node, list):
        for item in node:
            find_component_refs(item, refs)


def strip_unreferenced_components(data):
    refs = {}
    find_component_refs(data.get('paths', {}), refs)
    to_process = {k: set(v) for k, v in refs.items()}
    components = data.get('components', {})

    while to_process:
        comp_type, names = to_process.popitem()
        for name in names:
            component = components.get(comp_type, {}).get(name)
            if component:
                new_refs = {}
                find_component_refs(component, new_refs)
                for n_type, n_names in new_refs.items():
                    existing = refs.setdefault(n_type, set())
                    diff = n_names - existing
                    if diff:
                        existing.update(diff)
                        to_process.setdefault(n_type, set()).update(diff)

    for comp_type, comp_items in list(components.items()):
        used = refs.get(comp_type, set())
        for name in list(comp_items.keys()):
            if name not in used:
                del comp_items[name]
        if not comp_items:
            del components[comp_type]

    if not components:
        data.pop('components', None)

    return data


def build_output_path(input_path, output_path):
    if output_path:
        return output_path

    input_yaml_ext = os.path.splitext(input_path)[1]

    output_path = os.path.splitext(input_path)[0] + "-trimmed" + input_yaml_ext

    return output_path


def write_trimmed_yaml(output_path, data, has_yaml_doc_separator):
    data = OrderedDict(
            sorted(data.items(),
                   key=lambda x: ['openapi', 'info', 'tags', 'paths',
                                  'components'].index(x[0])))

    print(f"\nOutput to: {output_path}")

    with open(output_path, 'w') as file:
        if has_yaml_doc_separator:
            file.write('---\n')

        yaml.dump(data, file, Dumper=OrderedDumper, default_flow_style=False)


def offer_validation_execute(output_path):
    print("\nTo validate execute:")
    print(f"\nswagger-cli validate {output_path}\n")


def trim_openapi(input_path, prefixes, output_path=None, *,
                 exclude_components=None, strip_components=False):
    data, has_yaml_doc_separator = read_yaml(input_path)
    data = trim_yaml(prefixes, exclude_components, strip_components, data)
    output_path = build_output_path(input_path, output_path)
    write_trimmed_yaml(output_path, data, has_yaml_doc_separator)
    return output_path


def main():
    args = parse_args()

    output_path = trim_openapi(
        args.input,
        args.prefixes,
        output_path=args.output,
        exclude_components=args.exclude_components,
        strip_components=args.strip_components,
    )
    offer_validation_execute(output_path)


if __name__ == '__main__':
    main()
