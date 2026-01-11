#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GenPlexMatch
A utility script to generate .plexmatch files for complex Anime directory structures.
"""

import os
import re
import sys

# ================= CONFIGURATION =================
OUTPUT_FILE = ".plexmatch"
VIDEO_EXTS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.iso']
# Regex to match episode numbers like [01], [12], [09v2]
EPISODE_PATTERN = re.compile(r'\[(\d{1,3})(?:v\d)?\]')
# Keywords to identify Special features
SPECIAL_KEYWORDS = ['OAD', 'Menu', 'NCOP', 'NCED', 'SP', 'OVA', 'Specials', 'PV', 'CM', 'Event', 'Trailer']
# ===============================================

def get_subfolders(root_dir):
    """Get all visible subdirectories."""
    return sorted([d for d in os.listdir(root_dir) 
                   if os.path.isdir(os.path.join(root_dir, d)) and not d.startswith('.')])

def get_video_files(folder_path, root_dir):
    """Get video files in a specific directory (recursive or flat)."""
    videos = []
    # If scanning root, do not go recursive to avoid duplicates with subfolders
    if folder_path == root_dir:
        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in VIDEO_EXTS:
                videos.append(f)
    else:
        # Recursive scan for subfolders
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                if os.path.splitext(f)[1].lower() in VIDEO_EXTS:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, root_dir)
                    # Force unix-style path separators for .plexmatch compatibility
                    rel_path = rel_path.replace(os.sep, '/')
                    videos.append(rel_path)
    return sorted(videos)

def is_special_file(filename):
    """Check if filename contains keywords indicating it's a special feature."""
    for kw in SPECIAL_KEYWORDS:
        if kw.lower() in filename.lower():
            return True
    return False

def process_files(videos, season_num, plexmatch_lines, folder_name="Root"):
    """Analyze files and append mapping rules to the list."""
    folder_eps = []
    folder_sps = []
    global global_sp_count

    for filepath in videos:
        filename = os.path.basename(filepath)
        
        # Strategy 1: User explicitly defined as Specials (S00)
        if season_num == 0:
            match = EPISODE_PATTERN.search(filename)
            if match:
                # If explicit number found in OVA folder (e.g. [01]), use it
                folder_sps.append((int(match.group(1)), filepath, True))
            else:
                # No number found, use auto-increment
                folder_sps.append((999, filepath, False))
        
        # Strategy 2: Regular Season (S01, S02...)
        else:
            if is_special_file(filename):
                folder_sps.append((999, filepath, False))
            else:
                match = EPISODE_PATTERN.search(filename)
                if match:
                    folder_eps.append((int(match.group(1)), filepath))
                else:
                    # No episode number matched, treat as special
                    folder_sps.append((999, filepath, False))

    # Write Regular Episodes
    if season_num > 0 and folder_eps:
        plexmatch_lines.append("")
        plexmatch_lines.append(f"season:{season_num}")
        folder_eps.sort(key=lambda x: x[0])
        for ep_num, filepath in folder_eps:
            plexmatch_lines.append(f"ep:S{season_num:02d}E{ep_num:02d}:{filepath}")

    # Write Specials
    if folder_sps:
        plexmatch_lines.append("")
        plexmatch_lines.append(f"# Specials from: {folder_name}")
        # Sort by filename to ensure consistent order
        folder_sps.sort(key=lambda x: x[1])
        
        for ep_num, filepath, has_explicit_num in folder_sps:
            if has_explicit_num and season_num == 0:
                target_ep = ep_num
            else:
                target_ep = global_sp_count
                global_sp_count += 1
            plexmatch_lines.append(f"ep:S00E{target_ep:02d}:{filepath}")

def main():
    current_dir = os.getcwd()
    print(f"📂 Current Working Directory: {current_dir}")
    root_dir = '.'
    
    # 1. Scan Root Files
    root_videos = get_video_files(root_dir, root_dir)
    # 2. Scan Subfolders
    subfolders = get_subfolders(root_dir)
    
    # --- Display Summary ---
    print("\n" + "=" * 50)
    print(f"👀 Scan Results:")
    if root_videos:
        print(f"  [Root] Found {len(root_videos)} video files in root (likely Season 1)")
    
    if subfolders:
        print(f"  [Dirs] Found {len(subfolders)} subfolders:")
        for idx, folder in enumerate(subfolders, 1):
            print(f"         {idx}. {folder}")
    else:
        print("  [Dirs] No subfolders found.")
    print("=" * 50)

    # Confirmation
    if not root_videos and not subfolders:
        print("❌ No videos found. Please run this script inside an Anime folder.")
        return

    if input("Start matching? (Y/n): ").strip().lower() not in ['', 'y', 'yes']:
        print("Aborted.")
        return

    # Get TMDB ID
    print("\n" + "-" * 50)
    print("ℹ️  Tip: You can search TMDB ID at https://www.themoviedb.org/")
    tmdb_id = input("👉 Enter TMDB ID (Optional, press Enter to skip): ").strip()
    
    # Initialize global counter for specials
    global global_sp_count
    global_sp_count = 1
    
    plexmatch_lines = ["# Auto-generated by GenPlexMatch"]
    if tmdb_id:
        plexmatch_lines.append(f"tmdbid:{tmdb_id}")

    # --- Process Root Files ---
    if root_videos:
        print("\n" + "-" * 50)
        print(f"📂 Processing {len(root_videos)} files in ROOT directory...")
        print(f"   Sample: {root_videos[0]}")
        
        prompt = "👉 Which Season are these? (Default is 1. Input 's' to Skip): "
        s_input = input(prompt).strip()
        
        if s_input in ['', '1']:
            process_files(root_videos, 1, plexmatch_lines, "Root Files")
            print("   ✅ Marked as Season 1")
        elif s_input.isdigit():
            season = int(s_input)
            process_files(root_videos, season, plexmatch_lines, "Root Files")
            print(f"   ✅ Marked as Season {season}")
        else:
            print("   ⏭️  Skipped root files.")

    # --- Process Subfolders ---
    if subfolders:
        print("\n" + "-" * 50)
        print("📂 Processing Subfolders...")
        print("   Instructions: Input '1' for S01, '2' for S02, '0' for Specials/OVA.")
        print("                 Input 's' or Enter to Skip (e.g., for CDs/Scans).")
        
        for folder in subfolders:
            videos = get_video_files(folder, root_dir)
            if not videos:
                continue
                
            print(f"\n📁 Folder: \033[1;33m{folder}\033[0m ({len(videos)} videos)")
            s_input = input(f"   👉 Season? (s/0/1...): ").strip()
            
            if s_input.isdigit():
                season = int(s_input)
                process_files(videos, season, plexmatch_lines, folder)
                season_label = "Specials (S00)" if season == 0 else f"Season {season}"
                print(f"      ✅ Marked as {season_label}")
            else:
                print(f"      ⏭️  Skipped.")

    # --- Write File ---
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(plexmatch_lines))
        
        print("\n" + "=" * 50)
        print(f"🎉 Success! Generated: {os.path.abspath(OUTPUT_FILE)}")
        print(f"📝 {len(plexmatch_lines)} lines written.")
        print("⚠️  Remember to 'Refresh Metadata' in Plex for changes to take effect.")
        print("=" * 50)
    except IOError as e:
        print(f"\n❌ Error writing file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user.")
        sys.exit(0)
