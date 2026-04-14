import os
import json
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

# Configuration
EXT_DIR = "/home/yasir/Masaüstü/Coding/ShineS/shines/shinescript-extension"
OUTPUT_VSIX = "/home/yasir/Masaüstü/Coding/ShineS/shines/shinescript-1.0.0.vsix"

def create_vsix_manifest(pkg_data):
    # Standard XML namespaces for VSIX manifest
    root = ET.Element("PackageManifest", {
        "Version": "2.0.0",
        "xmlns": "http://schemas.microsoft.com/developer/vsx-schema/2011",
        "xmlns:d": "http://schemas.microsoft.com/developer/vsx-schema-design/2011"
    })
    
    metadata = ET.SubElement(root, "Metadata")
    ET.SubElement(metadata, "Identity", {
        "Id": pkg_data["name"],
        "Version": pkg_data["version"],
        "Publisher": pkg_data["publisher"],
        "Language": "en-US"
    })
    ET.SubElement(metadata, "DisplayName").text = pkg_data["displayName"]
    ET.SubElement(metadata, "Description", {"xml:space": "preserve"}).text = pkg_data.get("description", "")
    
    # Keywords/Tags
    if "keywords" in pkg_data:
        ET.SubElement(metadata, "Tags").text = ",".join(pkg_data["keywords"])
        
    # Categories
    if "categories" in pkg_data:
        ET.SubElement(metadata, "Categories").text = ",".join(pkg_data["categories"])
        
    ET.SubElement(metadata, "GalleryFlags").text = "Public"
    
    # Properties for VS Code
    properties = ET.SubElement(metadata, "Properties")
    ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Code.Engine", "Value": pkg_data.get("engines", {}).get("vscode", "^1.60.0")})
    ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Code.ExtensionKind", "Value": "workspace"})
    ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.GitHubFlavoredMarkdown", "Value": "true"})
    ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Content.Pricing", "Value": "Free"})
    
    if "repository" in pkg_data and "url" in pkg_data["repository"]:
        repo_url = pkg_data["repository"]["url"].replace(".git", "")
        ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Links.Source", "Value": repo_url})
        ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Links.Getstarted", "Value": repo_url})
        ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Links.GitHub", "Value": repo_url})
        ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Links.Support", "Value": f"{repo_url}/issues"})
        ET.SubElement(properties, "Property", {"Id": "Microsoft.VisualStudio.Services.Links.Learn", "Value": f"{repo_url}#readme"})

    # Installation Target (REQUIRED)
    installation = ET.SubElement(root, "Installation")
    ET.SubElement(installation, "InstallationTarget", {"Id": "Microsoft.VisualStudio.Code"})
    
    ET.SubElement(root, "Dependencies")
    
    assets = ET.SubElement(root, "Assets")
    # package.json is the core manifest
    ET.SubElement(assets, "Asset", {
        "Type": "Microsoft.VisualStudio.Code.Manifest",
        "Path": "extension/package.json",
        "Addressable": "true"
    })
    
    # Optional but recommended assets
    asset_map = [
        ("README.md", "Microsoft.VisualStudio.Services.Content.Details"),
        ("CHANGELOG.md", "Microsoft.VisualStudio.Services.Content.Changelog"),
        ("LICENSE", "Microsoft.VisualStudio.Services.Content.License"),
        ("icon.png", "Microsoft.VisualStudio.Services.Icons.Default")
    ]
    
    for filename, asset_type in asset_map:
        if os.path.exists(os.path.join(EXT_DIR, filename)):
            ET.SubElement(assets, "Asset", {
                "Type": asset_type,
                "Path": f"extension/{filename}",
                "Addressable": "true"
            })
    
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def create_content_types():
    root = ET.Element("Types", {"xmlns": "http://schemas.openxmlformats.org/package/2006/content-types"})
    
    # Default types
    defaults = [
        ("xml", "text/xml"),
        ("json", "application/json"),
        ("png", "image/png"),
        ("md", "text/markdown"),
        ("js", "application/javascript"),
        ("txt", "text/plain")
    ]
    
    for ext, ct in defaults:
        ET.SubElement(root, "Default", {"Extension": ext, "ContentType": ct})
        
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def package():
    with open(os.path.join(EXT_DIR, "package.json"), "r") as f:
        pkg_data = json.load(f)
        
    print(f"Packaging {pkg_data['name']} v{pkg_data['version']}...")
    
    # Load .vscodeignore
    ignore_list = [".git", ".vscode", "extension-packer.py"]
    ignore_file = os.path.join(EXT_DIR, ".vscodeignore")
    if os.path.exists(ignore_file):
        with open(ignore_file, "r") as f:
            ignore_list.extend([line.strip() for line in f if line.strip() and not line.startswith("#")])

    with zipfile.ZipFile(OUTPUT_VSIX, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add [Content_Types].xml
        zipf.writestr("[Content_Types].xml", create_content_types())
        
        # 2. Add extension.vsixmanifest
        zipf.writestr("extension.vsixmanifest", create_vsix_manifest(pkg_data))
        
        # 3. Add extension folder contents
        for root_dir, dirs, files in os.walk(EXT_DIR):
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, EXT_DIR)
                
                # Check ignore list
                should_ignore = False
                for ignore_pattern in ignore_list:
                    if ignore_pattern in rel_path:
                        should_ignore = True
                        break
                
                if not should_ignore:
                    zipf.write(full_path, os.path.join("extension", rel_path))
                    print(f"  Added: {rel_path}")

    print(f"\nSuccessfully created: {OUTPUT_VSIX}")

if __name__ == "__main__":
    package()
