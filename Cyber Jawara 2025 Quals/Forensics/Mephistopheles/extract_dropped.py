
import re

filename = 'sysmon.txt'
target_image = 'AnsiArtInstaller.exe'
dropped_files = set()

with open(filename, 'r') as f:
    text = f.read()

# Split into events (assuming "Event" or "UtcTime" or consistent separators, but sysmon.txt from strings is messy)
# The strings output grouped fields somewhat.
# Let's search for the block pattern.

# Pattern: Image [newline] ... AnsiArtInstaller.exe ... TargetFilename [newline] ... <filename>
# Or: TargetFilename [newline] <filename> ... Image [newline] ... AnsiArtInstaller.exe

# Since strings output is line-based, let's iterate lines and keep state.
lines = text.splitlines()
current_image = None
for i, line in enumerate(lines):
    line = line.strip()
    if line.endswith('AnsiArtInstaller.exe'):
        # This could be Image or TargetFilename (self-reference) or ParentImage
        # We need to rely on context.
        # But looking at previous output, "Image" line is followed by the path.
        pass

# Let's try a regex on the whole text for blocks
# We saw:
# Image
# C:\...\AnsiArtInstaller.exe
# TargetFilename
# C:\...\file.ext

# Or
# TargetFilename
# C:\...\file.ext
# ...
# Image
# C:\...\AnsiArtInstaller.exe

# The order varies.
# Let's finding all occurrences of TargetFilename and check the nearby Image.

candidates = []

# Scan for blocks roughly (assuming small distance)
for i in range(len(lines)):
    if 'TargetFilename' in lines[i]:
        # Look ahead for value
        target_file = None
        if i+1 < len(lines):
            target_file = lines[i+1].strip()
        
        # Look around for Image
        # Search backwards and forwards a bit (e.g., 20 lines)
        found_installer = False
        
        # Check if the target file itself is the installer (Zone.Identifier etc)
        if 'AnsiArtInstaller.exe' in target_file:
            continue
            
        start = max(0, i - 15)
        end = min(len(lines), i + 15)
        context = lines[start:end]
        
        for cline in context:
            # We want Image to be AnsiArtInstaller.exe
            # But we must distinguish from ParentImage
            if 'AnsiArtInstaller.exe' in cline and 'Image' in lines[max(0, lines.index(cline)-1)]: 
                # Very heuristic as lines.index finds first match.
                pass
        
        # Simpler approach:
        # The grep output showed:
        # C:\Users\Administrator\Downloads\AnsiArtInstaller.exe
        # C:\Users\ADMINI~1\AppData\Local\Temp\program.banner
        
        # It seems the Image comes first, then TargetFilename?
        if i > 0 and 'AnsiArtInstaller.exe' in lines[i-1]:
             # Matches the pattern seen in grep output
             candidates.append(target_file)

print('\n'.join(sorted(list(set(candidates)))))
