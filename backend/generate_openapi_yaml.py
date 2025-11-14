#!/usr/bin/env python3
"""
Generate OpenAPI YAML file from FastAPI app
Usage: python generate_openapi_yaml.py
"""

import sys
import yaml
from pathlib import Path

def generate_openapi_yaml(output_file: str = "openapi.yaml"):
    """
    Generate OpenAPI YAML file from FastAPI app.
    
    Args:
        output_file: Output YAML file path
    """
    try:
        # Import the FastAPI app
        from main import app
        
        print("Loading FastAPI app...")
        
        # Get OpenAPI schema
        openapi_schema = app.openapi()
        
        # Write to YAML
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(
                openapi_schema, 
                f, 
                sort_keys=False, 
                default_flow_style=False, 
                allow_unicode=True,
                width=120
            )
        
        print(f"\n[SUCCESS] OpenAPI YAML generated successfully!")
        print(f"  File: {output_path.absolute()}")
        print(f"  Title: {openapi_schema.get('info', {}).get('title')}")
        print(f"  Version: {openapi_schema.get('info', {}).get('version')}")
        print(f"  Total Endpoints: {len(openapi_schema.get('paths', {}))}")
        
        # Count endpoints by tag
        paths = openapi_schema.get('paths', {})
        tags_count = {}
        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    tags = details.get('tags', ['Untagged'])
                    for tag in tags:
                        tags_count[tag] = tags_count.get(tag, 0) + 1
        
        print(f"\n  Endpoints by category:")
        for tag, count in sorted(tags_count.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {tag}: {count} endpoints")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Could not import FastAPI app")
        print(f"   {str(e)}")
        print(f"\n   Make sure you're running this from the backend directory")
        print(f"   and all dependencies are installed.")
        return False
    except Exception as e:
        print(f"[ERROR] Error generating OpenAPI YAML: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else "openapi.yaml"
    
    print("=" * 60)
    print("OpenAPI YAML Generator for PulseTrack HRMS")
    print("=" * 60)
    
    success = generate_openapi_yaml(output_file)
    
    if success:
        print("\n[DONE] You can now use this YAML file for Milestone 4 submission.")
        print(f"  View it at: http://localhost:8000/api/docs")
        print(f"  Or open: {output_file}")
    else:
        print("\n[FAILED] Failed to generate YAML file.")
        sys.exit(1)

