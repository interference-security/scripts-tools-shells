#!/usr/bin/env python3
"""
Swagger YAML to CSV Converter
Converts Swagger/OpenAPI YAML file to CSV with HTTP methods, API URLs, Deprecated status, Tags, and Description

Run this to use this:
pip install pyyaml

Example:
python3 swagger_to_csv.py swagger.yaml output.csv
"""

import yaml
import csv
import sys
import argparse
from pathlib import Path

def load_swagger_yaml(file_path):
    """Load and parse Swagger YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def extract_api_endpoints(swagger_data):
    """Extract HTTP methods, API URLs, Deprecated status, Tags, and Description from Swagger data"""
    endpoints = []
    
    if not swagger_data or 'paths' not in swagger_data:
        print("Error: No 'paths' section found in Swagger file.")
        return endpoints
    
    base_path = swagger_data.get('basePath', '')
    
    for path, methods in swagger_data['paths'].items():
        full_path = base_path + path
        
        for method, details in methods.items():
            # Only include standard HTTP methods
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                # Handle deprecated field
                deprecated = details.get('deprecated', False)
                if deprecated is True:
                    deprecated_status = 'true'
                elif deprecated is False:
                    deprecated_status = 'false'
                else:
                    deprecated_status = ''
                
                # Handle tags field (can be array or single value)
                tags = details.get('tags', [])
                if isinstance(tags, list):
                    tags_str = ', '.join(tags) if tags else ''
                else:
                    tags_str = str(tags)
                
                # Handle description field
                description = details.get('description', '')
                if description is None:
                    description = ''
                
                endpoints.append({
                    'http_method': method.upper(),
                    'api_url': full_path,
                    'deprecated': deprecated_status,
                    'tags': tags_str,
                    'description': description
                })
    
    return endpoints

def write_to_csv(endpoints, output_file):
    """Write endpoints to CSV file"""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['http_method', 'api_url', 'deprecated', 'tags', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for endpoint in endpoints:
                writer.writerow(endpoint)
        
        print(f"Successfully wrote {len(endpoints)} endpoints to {output_file}")
        
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Convert Swagger YAML to CSV with HTTP methods, API URLs, Deprecated status, Tags, and Description'
    )
    parser.add_argument(
        'input_file',
        help='Path to the Swagger YAML file'
    )
    parser.add_argument(
        'output_file',
        help='Path to the output CSV file'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    # Load and parse Swagger YAML
    print(f"Loading Swagger file: {args.input_file}")
    swagger_data = load_swagger_yaml(args.input_file)
    
    # Extract endpoints
    print("Extracting API endpoints...")
    endpoints = extract_api_endpoints(swagger_data)
    
    if not endpoints:
        print("No API endpoints found in the Swagger file.")
        sys.exit(1)
    
    # Write to CSV
    print(f"Writing to CSV: {args.output_file}")
    write_to_csv(endpoints, args.output_file)

if __name__ == "__main__":
    main()