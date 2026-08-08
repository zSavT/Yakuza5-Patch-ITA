#!/usr/bin/env python3
import os
import sys
import glob
import re

# Ensure stdout handles UTF-8 on Windows as well
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def parse_po_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Normalize line endings for comparison
    content_lf = content.replace('\r\n', '\n')
    
    blocks = content_lf.split('\n\n')
    entries = []
    
    for block_idx, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        if "Project-Id-Version:" in block or block.startswith("msgid \"\""):
            continue
        
        ctx_m = re.search(r'msgctxt\s+"([^"]+)"', block)
        msgid_m = re.search(r'msgid\s+((?:"[^"\\]*(?:\\.[^"\\]*)*"\s*)+)', block)
        msgstr_m = re.search(r'msgstr\s+((?:"[^"\\]*(?:\\.[^"\\]*)*"\s*)+)', block)
        
        ctx = ctx_m.group(1) if ctx_m else ""
        raw_msgid = msgid_m.group(1).strip() if msgid_m else ""
        raw_msgstr = msgstr_m.group(1).strip() if msgstr_m else ""
        
        # Check if there is an illegal blank line between msgid and msgstr in the block
        has_blank_between_id_str = bool(re.search(r'msgid\s+.*?\n\nmsgstr', block, re.DOTALL))
        
        entries.append({
            'ctx': ctx,
            'msgid': raw_msgid,
            'msgstr': raw_msgstr,
            'blank_err': has_blank_between_id_str,
            'block': block
        })
        
    return entries

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    orig_dir = os.path.join(repo_root, "File Versione Beta", "File Originali")
    trad_dir = os.path.join(repo_root, "File Versione Beta", "File Tradotti", "data")
    
    if not os.path.exists(orig_dir) or not os.path.exists(trad_dir):
        print(f"❌ Error: Directories not found.\n  Original: {orig_dir}\n  Translated: {trad_dir}")
        sys.exit(1)
        
    orig_files = glob.glob(os.path.join(orig_dir, "**", "*.po"), recursive=True)
    print(f"🔍 Found {len(orig_files)} PO files in original directory. Starting consistency check...\n")
    
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
        orig_entries = parse_po_file(orig_path)
        trad_entries = parse_po_file(trad_path)
        
        file_errors = []
        
        if len(orig_entries) != len(trad_entries):
            file_errors.append(f"Entry count mismatch: Original has {len(orig_entries)} entries, Translated has {len(trad_entries)} entries.")
            
        max_len = max(len(orig_entries), len(trad_entries))
        for i in range(max_len):
            if i >= len(orig_entries):
                file_errors.append(f"Entry #{i+1}: Extra entry in translated file (msgctxt: '{trad_entries[i]['ctx']}')")
                continue
            if i >= len(trad_entries):
                file_errors.append(f"Entry #{i+1}: Missing entry in translated file (expected msgctxt: '{orig_entries[i]['ctx']}')")
                continue
                
            o_e = orig_entries[i]
            t_e = trad_entries[i]
            
            # Check msgctxt match
            if o_e['ctx'] != t_e['ctx']:
                file_errors.append(f"Entry #{i+1} msgctxt mismatch: Original='{o_e['ctx']}' vs Translated='{t_e['ctx']}'")
                
            # Check msgid match (including line breaks / multiline quotes)
            if o_e['msgid'] != t_e['msgid']:
                file_errors.append(f"Entry #{i+1} msgid mismatch (msgctxt='{o_e['ctx']}'):\n      Original msgid:   {o_e['msgid']!r}\n      Translated msgid: {t_e['msgid']!r}")
                
            # Check for blank lines between msgid and msgstr
            if t_e['blank_err']:
                file_errors.append(f"Entry #{i+1} formatting error (msgctxt='{o_e['ctx']}'): Blank line found between msgid and msgstr!")
                
        if file_errors:
            total_errors += len(file_errors)
            print(f"❌ DISCREPANCIES IN FILE: {rel_path}")
            for err in file_errors:
                print(f"   • {err}")
            print()
            
    if total_errors > 0:
        print(f"❌ FAIL: Found {total_errors} discrepancy error(s) across {checked_count} PO files.")
        sys.exit(1)
    else:
        print(f"✅ SUCCESS: All {checked_count} PO files match 100% in msgctxt, msgid, order, and formatting!")
        sys.exit(0)

if __name__ == "__main__":
    main()
