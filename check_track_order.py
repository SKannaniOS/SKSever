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

def check_track_order():
    """
    Function to check if track numbers in batch_content.txt are in ascending order.
    Prints any inconsistencies found where tracks are not in ascending order.
    """
    # Get the path to batch_content.txt
    current_dir = os.path.dirname(os.path.realpath(__file__))
    batch_file_path = os.path.join(current_dir, 'output_files/batch_content.txt')
    batch_file_path = os.path.abspath(batch_file_path)
    
    if not os.path.exists(batch_file_path):
        print(f"Error: File not found - {batch_file_path}")
        return
    
    try:
        with open(batch_file_path, 'r') as f:
            content = f.read()
        
        # Extract track numbers using regex
        track_pattern = r'Track:\s*(\d+)'
        matches = re.findall(track_pattern, content)
        
        if not matches:
            print("No track numbers found in the file.")
            return
        
        # Convert to integers
        track_numbers = [int(match) for match in matches]
        
        print(f"Found {len(track_numbers)} track entries.")
        print(f"Track numbers: {track_numbers}")
        
        # Check for ascending order
        inconsistencies = []
        
        for i in range(1, len(track_numbers)):
            current_track = track_numbers[i]
            previous_track = track_numbers[i-1]
            
            if current_track <= previous_track:
                inconsistencies.append({
                    'position': i + 1,  # 1-based position
                    'previous_track': previous_track,
                    'current_track': current_track,
                    'line_number': i + 2  # Approximate line number (considering header)
                })
        
        if inconsistencies:
            print(f"\n❌ INCONSISTENCIES FOUND: {len(inconsistencies)} places where tracks are not in ascending order:")
            print("-" * 70)
            
            for issue in inconsistencies:
                print(f"Position {issue['position']}: Track {issue['current_track']} comes after Track {issue['previous_track']}")
                print(f"  Expected: Track {issue['previous_track']} < Track {issue['current_track']}")
                print(f"  Approximate line: {issue['line_number']}")
                print()
        else:
            print("\n✅ All tracks are in ascending order!")
            
        # Additional statistics
        expected_sequence = list(range(1, len(track_numbers) + 1))
        missing_tracks = set(expected_sequence) - set(track_numbers)
        duplicate_tracks = []
        
        # Check for duplicates
        seen = set()
        for track in track_numbers:
            if track in seen and track not in duplicate_tracks:
                duplicate_tracks.append(track)
            seen.add(track)
        
        if missing_tracks:
            print(f"⚠️  Missing tracks (if expecting 1 to {len(track_numbers)}): {sorted(missing_tracks)}")
        
        if duplicate_tracks:
            print(f"⚠️  Duplicate tracks found: {duplicate_tracks}")
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    check_track_order()
