#!/usr/bin/env python3
"""
Standalone script to check if track numbers in batch_content.txt are in ascending order.
This script can be run independently without importing the server module.

Usage:
    python3 check_track_order.py
    
Or make it executable and run:
    chmod +x check_track_order.py
    ./check_track_order.py
"""

import os
import re

def _get_batch_file_path():
    """Get the path to batch_content.txt file."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    batch_file_path = os.path.join(current_dir, 'output_files/batch_content.txt')
    return os.path.abspath(batch_file_path)

def _extract_track_numbers(content):
    """Extract track numbers from file content."""
    track_pattern = r'Track:\s*(\d+)'
    matches = re.findall(track_pattern, content)
    return [int(match) for match in matches] if matches else []

def _find_order_inconsistencies(track_numbers):
    """Find places where tracks are not in ascending order."""
    inconsistencies = []
    for i in range(1, len(track_numbers)):
        current_track = track_numbers[i]
        previous_track = track_numbers[i-1]
        
        if current_track <= previous_track:
            inconsistencies.append({
                'position': i + 1,
                'previous_track': previous_track,
                'current_track': current_track,
                'line_number': i + 2
            })
    return inconsistencies

def _print_inconsistencies(inconsistencies):
    """Print found inconsistencies."""
    print(f"\n❌ INCONSISTENCIES FOUND: {len(inconsistencies)} places where tracks are not in ascending order:")
    print("-" * 70)
    
    for issue in inconsistencies:
        print(f"Position {issue['position']}: Track {issue['current_track']} comes after Track {issue['previous_track']}")
        print(f"  Expected: Track {issue['previous_track']} < Track {issue['current_track']}")
        print(f"  Approximate line: {issue['line_number']}")
        print()

def _find_duplicate_tracks(track_numbers):
    """Find duplicate track numbers."""
    duplicate_tracks = []
    seen = set()
    for track in track_numbers:
        if track in seen and track not in duplicate_tracks:
            duplicate_tracks.append(track)
        seen.add(track)
    return duplicate_tracks

def _print_statistics(track_numbers):
    """Print additional statistics about tracks."""
    expected_sequence = set(range(1, len(track_numbers) + 1))
    track_set = set(track_numbers)
    missing_tracks = expected_sequence - track_set
    duplicate_tracks = _find_duplicate_tracks(track_numbers)
    
    if missing_tracks:
        print(f"⚠️  Missing tracks (if expecting 1 to {len(track_numbers)}): {sorted(missing_tracks)}")
    
    if duplicate_tracks:
        print(f"⚠️  Duplicate tracks found: {duplicate_tracks}")

def check_track_order():
    """
    Function to check if track numbers in batch_content.txt are in ascending order.
    Prints any inconsistencies found where tracks are not in ascending order.
    """
    batch_file_path = _get_batch_file_path()
    
    if not os.path.exists(batch_file_path):
        print(f"Error: File not found - {batch_file_path}")
        return
    
    try:
        with open(batch_file_path, 'r') as f:
            content = f.read()
        
        track_numbers = _extract_track_numbers(content)
        
        if not track_numbers:
            print("No track numbers found in the file.")
            return
        
        print(f"Found {len(track_numbers)} track entries.")
        print(f"Track numbers: {track_numbers}")
        
        inconsistencies = _find_order_inconsistencies(track_numbers)
        
        if inconsistencies:
            _print_inconsistencies(inconsistencies)
        else:
            print("\n✅ All tracks are in ascending order!")
            
        _print_statistics(track_numbers)
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    check_track_order()

# ------------------------------------------------------------ #
# To run this script, use the following command:
# python3 check_track_order.py
# ------------------------------------------------------------ #