#!/usr/bin/env python3
import os
import sys
import glob
import re

# Ensure stdout handles UTF-8 on Windows as well
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_text(raw_msgid):
    """
    Extracts text from PO string quotes and normalizes whitespace, linebreaks,
    and full-width dashes (－ vs -) so visual differences do not trigger false errors.
    """
    lines = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_msgid)
    combined = "".join(lines)
    cleaned = combined.replace('\\r\\n', ' ').replace('\\n', ' ').replace('\\r', ' ').replace('－', '-')
    return re.sub(r'\s+', ' ', cleaned).strip()

def parse_po_dict(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    content_lf = content.replace('\r\n', '\n')
    blocks = content_lf.split('\n\n')
    
    # Store entries mapped by msgctxt
    entries = {}
    
    for block in blocks:
        block = block.strip()
        if not block or "Project-Id-Version:" in block or block.startswith("msgid \"\""):
            continue
        
        ctx_m = re.search(r'msgctxt\s+"([^"]+)"', block)
        msgid_m = re.search(r'msgid\s+((?:"[^"\\]*(?:\\.[^"\\]*)*"\s*)+)', block)
        
        if ctx_m and msgid_m:
            ctx = ctx_m.group(1)
            raw_msgid = msgid_m.group(1).strip()
            norm_id = normalize_text(raw_msgid)
            entries[ctx] = norm_id
            
    return entries

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    orig_dir = os.path.join(repo_root, "File Versione Beta", "File Originali")
    trad_dir = os.path.join(repo_root, "File Versione Beta", "File Tradotti", "data")
    
    if not os.path.exists(orig_dir) or not os.path.exists(trad_dir):
        print(f"❌ Error: Directories not found.\n  Original: {orig_dir}\n  Translated: {trad_dir}")
        sys.exit(1)
        
    orig_files = glob.glob(os.path.join(orig_dir, "**", "*.po"), recursive=True)
    print(f"🔍 Found {len(orig_files)} PO files in original directory. Starting key-based consistency check...\n")
    
    total_errors = 0
    checked_count = 0
    
    for orig_path in sorted(orig_files):
        rel_path = os.path.relpath(orig_path, orig_dir)
        trad_path = os.path.join(trad_dir, rel_path)
        
        if not os.path.exists(trad_path):
            print(f"❌ MISSING FILE: {rel_path} does not exist in translated directory!")
            total_errors += 1
            continue
            
        checked_count += 1
        orig_dict = parse_po_dict(orig_path)
        trad_dict = parse_po_dict(trad_path)
        
        file_errors = []
        
        # Check missing msgctxt keys from Original
        missing_keys = [k for k in orig_dict if k not in trad_dict]
        for k in missing_keys:
            file_errors.append(f"Missing msgctxt '{k}' in translated file (expected msgid: '{orig_dict[k]}')")
            
        # Check text mismatches for same msgctxt key
        for k, o_text in orig_dict.items():
            if k in trad_dict:
                t_text = trad_dict[k]
                if o_text != t_text:
                    file_errors.append(f"Text content mismatch for msgctxt '{k}':\n      Original text:   {o_text!r}\n      Translated text: {t_text!r}")
                    
        if file_errors:
            total_errors += len(file_errors)
            print(f"❌ DISCREPANCIES IN FILE: {rel_path}")
            for err in file_errors[:10]:  # Limit output per file to top 10
                print(f"   • {err}")
            if len(file_errors) > 10:
                print(f"   ... and {len(file_errors) - 10} more errors in this file.")
            print()
            
    if total_errors > 0:
        print(f"❌ FAIL: Found {total_errors} discrepancy error(s) across {checked_count} PO files.")
        sys.exit(1)
    else:
        print(f"✅ SUCCESS: All {checked_count} PO files match 100% in msgctxt keys and English text content!")
        sys.exit(0)

if __name__ == "__main__":
    main()
