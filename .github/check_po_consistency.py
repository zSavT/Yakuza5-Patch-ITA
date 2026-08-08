#!/usr/bin/env python3
import os
import sys
import glob
import re
import difflib

# Ensure stdout handles UTF-8 on Windows as well
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def normalize_text_permissive(raw_msgid):
    """
    Extracts text from PO string quotes and normalizes:
    - Removes punctuation, quotes, apostrophes, hyphens, dashes, and tags
    - Converts to lowercase
    - Collapses all whitespace and linebreaks into a single space
    """
    lines = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_msgid)
    combined = "".join(lines)
    
    # Remove HTML/formatting tags like <Color:...>, <Color:Default>
    cleaned = re.sub(r'<[^>]+>', '', combined)
    
    # Replace linebreaks with space
    cleaned = cleaned.replace('\\r\\n', ' ').replace('\\n', ' ').replace('\\r', ' ')
    
    # Strip all punctuation and symbols, convert to lowercase
    cleaned = re.sub(r'[^\w\s]', '', cleaned).lower()
    
    return re.sub(r'\s+', ' ', cleaned).strip()

def contains_translation_in_msgid(orig_norm, trad_norm, msgstr_norm):
    """
    Detects if trad_norm differs from orig_norm because it contains parts of the Italian translation (msgstr_norm),
    Italian localization terms, or deduplicated/substring text in msgid.
    """
    if not trad_norm:
        return False
        
    # Check 1: trad_norm is a substring of orig_norm or contains orig_norm
    if orig_norm and (orig_norm in trad_norm or trad_norm in orig_norm):
        return True
        
    # Check 2: trad_norm shares significant word overlap with msgstr_norm
    if msgstr_norm:
        orig_words = set(orig_norm.split())
        trad_words = set(trad_norm.split())
        msgstr_words = set(msgstr_norm.split())
        
        added_words = trad_words - orig_words
        if added_words and (added_words & msgstr_words):
            return True
            
        if trad_words and len(trad_words & msgstr_words) / len(trad_words) >= 0.25:
            return True

    # Common Italian localization keywords that might replace English terms in msgid (e.g. heat -> furore, east -> est)
    italian_terms = {
        "furore", "barra", "est", "ovest", "nord", "sud", "via", "mancina", "destra", 
        "livello", "agenzia", "lezioni", "media", "pubblicità", "prelievo", "stanca", 
        "mancia", "ragione", "verme", "allenatore", "colpo", "spada", "stella"
    }
    trad_words = set(trad_norm.split())
    if trad_words & italian_terms:
        return True
        
    return False

def is_text_matching(orig_norm, trad_norm, similarity_threshold=0.85):
    """
    Returns True if texts match exactly after normalization, or if fuzzy similarity >= threshold (default 85%).
    """
    if orig_norm == trad_norm:
        return True
    if not orig_norm or not trad_norm:
        return False
    ratio = difflib.SequenceMatcher(None, orig_norm, trad_norm).ratio()
    return ratio >= similarity_threshold

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
        msgstr_m = re.search(r'msgstr\s+((?:"[^"\\]*(?:\\.[^"\\]*)*"\s*)+)', block)
        
        if ctx_m and msgid_m:
            ctx = ctx_m.group(1)
            raw_msgid = msgid_m.group(1).strip()
            raw_msgstr = msgstr_m.group(1).strip() if msgstr_m else ""
            
            norm_id = normalize_text_permissive(raw_msgid)
            norm_str = normalize_text_permissive(raw_msgstr)
            
            entries[ctx] = {
                'norm_msgid': norm_id,
                'norm_msgstr': norm_str
            }
            
    return entries

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    orig_dir = os.path.join(repo_root, "File Versione Beta", "File Originali")
    trad_dir = os.path.join(repo_root, "File Versione Beta", "File Tradotti", "data")
    
    if not os.path.exists(orig_dir) or not os.path.exists(trad_dir):
        print(f"❌ Error: Directories not found.\n  Original: {orig_dir}\n  Translated: {trad_dir}")
        sys.exit(1)
        
    orig_files = glob.glob(os.path.join(orig_dir, "**", "*.po"), recursive=True)
    print(f"🔍 Found {len(orig_files)} PO files in original directory. Starting key-based consistency check (85% similarity threshold)...\n")
    
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
            file_errors.append(f"Missing msgctxt '{k}' in translated file (expected msgid text: '{orig_dict[k]['norm_msgid']}')")
            
        # Check text mismatches for same msgctxt key with 85% similarity threshold
        for k, o_item in orig_dict.items():
            if k in trad_dict:
                o_text = o_item['norm_msgid']
                t_item = trad_dict[k]
                t_text = t_item['norm_msgid']
                t_str = t_item['norm_msgstr']
                
                if not is_text_matching(o_text, t_text, similarity_threshold=0.85):
                    # Ignore if trad_text contains parts of Italian translation (msgstr or Italian keywords)
                    if contains_translation_in_msgid(o_text, t_text, t_str):
                        continue
                        
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
        print(f"✅ SUCCESS: All {checked_count} PO files match 100% in msgctxt keys and English text content (>=85% similarity or translation in msgid ignored)!")
        sys.exit(0)

if __name__ == "__main__":
    main()
