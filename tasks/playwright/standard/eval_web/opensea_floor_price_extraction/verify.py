#!/usr/bin/env python3
"""
Verification script for OpenSea floor price extraction task.
"""

import sys
import json
import os
import re
import csv
from io import StringIO

# Expected CSV header (must match exactly)
EXPECTED_HEADER_LINE = "Collection, Floor Price"
EXPECTED_HEADERS = ["Collection", "Floor Price"]


def get_model_response():
    """
    Get the model's response from the MCP_MESSAGES environment variable.
    """
    messages_path = os.getenv("MCP_MESSAGES")
    if not messages_path:
        print("| Warning: MCP_MESSAGES environment variable not set", file=sys.stderr)
        return None

    try:
        with open(messages_path, 'r') as f:
            messages = json.load(f)

        for message in reversed(messages):
            if (message.get('role') == 'assistant' and
                    message.get('status') == 'completed' and
                    message.get('type') == 'message'):
                content = message.get('content', [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get('type') in ['text', 'output_text']:
                            return item.get('text', '')
                elif isinstance(content, str):
                    return content
        return None
    except Exception as e:
        print(f"| Error reading messages file: {str(e)}", file=sys.stderr)
        return None


def extract_csv_from_response(response):
    """
    Extract CSV data from markdown code blocks.
    """
    csv_pattern = r'```(?:csv)?\s*\n(.*?)\n```'
    matches = re.findall(csv_pattern, response, re.DOTALL | re.IGNORECASE)

    if matches:
        return matches[-1].strip()

    # Fallback to lines matching headers
    lines = response.split('\n')
    for i, line in enumerate(lines):
        if "Collection" in line and "Floor Price" in line:
            csv_lines = []
            for l in lines[i:]:
                l = l.strip()
                if not l or ("," not in l and "|" not in l):
                    if csv_lines:
                        break
                    continue
                csv_lines.append(l)
            return '\n'.join(csv_lines)
    return None


def validate_csv_data(csv_text):
    """
    Validate CSV data according to task requirements.
    """
    if not csv_text:
        return False, "CSV data not found in response"

    try:
        lines = csv_text.strip().split('\n')
        if len(lines) < 2:
            return False, "CSV data too short (must contain header and at least one row)"

        # Check header
        header_line = lines[0].strip()
        if header_line != EXPECTED_HEADER_LINE:
            return False, f"Header mismatch, expected: '{EXPECTED_HEADER_LINE}', actual: '{header_line}'"

        # Parse CSV
        # Handle both comma and pipe separators if model uses them (though prompt says comma)
        f = StringIO(csv_text)
        reader = csv.DictReader(f, skipinitialspace=True)
        
        valid_rows = 0
        for i, row in enumerate(reader, 1):
            # Check for header keys
            if 'Collection' not in row or 'Floor Price' not in row:
                return False, f"Row {i} is missing expected columns"
            
            collection = row.get('Collection', '').strip()
            floor_price_str = row.get('Floor Price', '').strip()
            
            if not collection:
                return False, f"Row {i} has empty collection name"
            
            # Use regex to clean floor_price_str if necessary (in case model included ETH)
            # and then convert to float
            price_match = re.search(r'([0-9\.]+)', floor_price_str.replace(',', ''))
            if not price_match:
                return False, f"Row {i} floor price must be a number, actual: '{floor_price_str}'"
            
            try:
                floor_price = float(price_match.group(1))
            except ValueError:
                return False, f"Row {i} floor price must be valid float, actual: '{floor_price_str}'"
            
            # The criteria: must be strictly > 1.0
            if floor_price <= 1.0:
                return False, f"Found collection '{collection}' with floor price {floor_price} <= 1.0 ETH (should have been filtered out)"
            
            valid_rows += 1

        if valid_rows == 0:
            return False, "No valid collections found matching the criteria"

        return True, f"Verified {valid_rows} collections with floor price > 1.0 ETH."

    except Exception as e:
        return False, f"CSV parsing/validation error: {str(e)}"


def verify():
    model_response = get_model_response()
    if not model_response:
        return False

    csv_data = extract_csv_from_response(model_response)
    if not csv_data:
        print("| ✗ CSV not found in response", file=sys.stderr)
        return False

    success, message = validate_csv_data(csv_data)
    if success:
        print(f"| ✓ {message}", file=sys.stderr)
        return True
    else:
        print(f"| ✗ {message}", file=sys.stderr)
        return False


if __name__ == "__main__":
    is_successful = verify()
    sys.exit(0 if is_successful else 1)
