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
    Extracts text from PO string quotes and normalizes all whitespace/linebreaks
    so that visual line breaks (\r\n or multi-line wrapping) do not trigger false errors.
    """
    lines = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_msgid)
    combined = "".join(lines)
    # Replace literal \r\n escape strings or actual newlines with single space
    cleaned = combined.replace('\\r\\n', ' ').replace('\\n', ' ').replace('\\r', ' ')
    # Normalize multiple spaces/newlines to single space
    return re.sub(r'\s+', ' ', cleaned).strip()

def parse_po_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    content_lf = content.replace('\r\n', '\n')
    blocks = content_lf.split('\n\n')
    entries = []
    
    for block in blocks:
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
        
        norm_id = normalize_text(raw_msgid)
        
        entries.append({
            'ctx': ctx,
            'raw_msgid': raw_msgid,
            'norm_msgid': norm_id,
            'msgstr': raw_msgstr,
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
    print(f"🔍 Found {len(orig_files)} PO files in original directory. Starting flexible consistency check...\n")
    
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
                
            # Check normalized msgid text content match (ignoring line break formatting)
            if o_e['norm_msgid'] != t_e['norm_msgid']:
                file_errors.append(f"Entry #{i+1} text content mismatch (msgctxt='{o_e['ctx']}'):\n      Original text:   {o_e['norm_msgid']!r}\n      Translated text: {t_e['norm_msgid']!r}")
                
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
        print(f"✅ SUCCESS: All {checked_count} PO files match 100% in msgctxt sequence and English text content!")
        sys.exit(0)

if __name__ == "__main__":
    main()
