#!/usr/bin/env python3

# File: imgbb/cli.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2026-10-21
# Description: CLI interface module for ImgBB with Rich formatting, wildcard support, and flexible JSON field outputs.
# License: MIT

"""CLI interface module for ImgBB with Rich formatting, wildcard support, and flexible JSON field outputs."""

import argparse
import glob
import json
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .core import ImgBBClient, ImgBBError

console = Console()

def main():
    try:
        from rchf import CustomRichHelpFormatter
    except ImportError:
        CustomRichHelpFormatter = argparse.RawTextHelpFormatter
    
    parser = argparse.ArgumentParser(
        description="A production-ready CLI tool to upload images to ImgBB with wildcard support and flexible outputs.",
        prog='imgbb',
        formatter_class=CustomRichHelpFormatter
    )
    parser.add_argument(
        "IMAGES",
        help="Path or wildcard pattern to the image file(s) to upload (e.g., *.jpg, image?.png, *).",
        nargs='*'
    )
    parser.add_argument(
        "-k", "--key",
        dest="api_key",
        help="ImgBB API key. Can also be set via IMGBB_API_KEY environment variable.",
        default=None
    )
    parser.add_argument(
        "-e", "--expiration",
        type=int,
        help="Enable auto-deletion after given seconds (60-15552000).",
        default=None
    )
    parser.add_argument(
        "-n", "--name",
        help="Custom name for the uploaded image file (applicable if uploading a single file).",
        default=None
    )
    parser.add_argument(
        "-f", "--format",
        dest="output_format",
        choices=["pretty", "json", "url", "display_url", "delete_url", "thumb_url", "medium_url"],
        default="pretty",
        help=(
            "Output format style or specific JSON field to extract:\n"
            "  - pretty      : Rich formatted panel view (default)\n"
            "  - json        : Full raw JSON response\n"
            "  - url         : Direct image URL only\n"
            "  - display_url : Viewer / display page URL only\n"
            "  - delete_url  : Deletion URL only\n"
            "  - thumb_url   : Thumbnail URL only\n"
            "  - medium_url  : Medium image URL only"
        )
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Initialize client once and validate API key
    try:
        client = ImgBBClient(api_key=args.api_key)
    except ImgBBError as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        sys.exit(1)

    # Expand wildcards (e.g., *.jpg, *, image??.png)
    resolved_images = []
    for pattern in args.IMAGES:
        matched_files = glob.glob(pattern)
        if matched_files:
            resolved_images.extend(matched_files)
        else:
            # If no wildcard match found, keep the raw string so core.py handles file-not-found nicely
            resolved_images.append(pattern)

    # Remove duplicates while preserving order
    resolved_images = list(dict.fromkeys(resolved_images))

    for image in resolved_images:
        try:
            # Show progress bar only if format is pretty, keep silent for pure data outputs
            if args.output_format == "pretty":
                with console.status(f"[bold cyan]🚀 Uploading[/] [bold #FFFF00]{image}[/] [bold cyan]to ImgBB [/bold cyan]", spinner="point", spinner_position='right', persist="all"):
                    data = client.upload(image, expiration=args.expiration, name=args.name)
            else:
                data = client.upload(image, expiration=args.expiration, name=args.name)

            # Flexible Output Handler based on parsed JSON fields
            fmt = args.output_format
            
            if fmt == "json":
                print(json.dumps(data, indent=2))
            elif fmt == "url":
                print(data.get("url", ""))
            elif fmt == "display_url":
                print(data.get("display_url", ""))
            elif fmt == "delete_url":
                print(data.get("delete_url", ""))
            elif fmt == "thumb_url":
                thumb = data.get("thumb", {})
                print(thumb.get("url", "") if isinstance(thumb, dict) else "")
            elif fmt == "medium_url":
                medium = data.get("medium", {})
                print(medium.get("url", "") if isinstance(medium, dict) else "")
            else:
                # Pretty sectionized output using Rich Table & Panel
                table = Table(show_header=False, box=None, padding=(0, 2))
                table.add_column("Key", style="bold yellow")
                table.add_column("Value", style="cyan")

                table.add_row("🔗 Direct URL", data.get('url'))
                table.add_row("🌐 Viewer URL", data.get('display_url'))
                table.add_row("🗑️ Delete URL", data.get('delete_url'))
                
                thumb = data.get('thumb', {})
                if isinstance(thumb, dict) and thumb.get('url'):
                    table.add_row("🖼️ Thumbnail URL", thumb.get('url'))
                    
                medium = data.get('medium', {})
                if isinstance(medium, dict) and medium.get('url'):
                    table.add_row("📐 Medium URL", medium.get('url'))

                table.add_row("📁 File Name", data.get('title') or data.get('name'))
                table.add_row("📦 Size", f"{data.get('size')} bytes")
                table.add_row("⏱️ Expiration", f"{data.get('expiration')} seconds" if data.get('expiration') != '0' else "Never")

                panel = Panel(
                    table,
                    title=f"[bold green]✨ Upload Successful ({image})! ✨[/bold green]",
                    border_style="green",
                    expand=False
                )
                console.print(panel)

        except ImgBBError as e:
            console.print(f"[bold red]❌ Error ({image}):[/bold red] {e}")
            continue
        except Exception as e:
            console.print(f"[bold red]💥 Unexpected Error ({image}):[/bold red] {e}")
            continue

if __name__ == "__main__":
    main()
