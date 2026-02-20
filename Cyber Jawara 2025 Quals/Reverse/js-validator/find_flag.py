#!/usr/bin/env python3
with open('chall.bin', 'rb') as f:
    data = f.read()

offset = data.find(b'CJ{')
if offset != -1:
    print(f'✓ Found "CJ{{" at offset: 0x{offset:x} ({offset})')
    end = data.find(b'}', offset)
    if end != -1:
        flag = data[offset:end+1]
        print(f'Potential flag bytes: {flag}')
        print(f'Length: {end - offset + 1} bytes')
        
        try:
            flag_str = flag.decode('ascii')
            print(f'\n🎯 Potential flag (ASCII): {flag_str}')
            
            # Test if this is the correct flag
            import hashlib
            hash_result = hashlib.sha256(flag_str.encode()).hexdigest()
            target = "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"
            
            print(f'\nSHA-256 of "{flag_str}":')
            print(f'  Computed: {hash_result}')
            print(f'  Target:   {target}')
            
            if hash_result == target:
                print(f'\n🎉🎉🎉 FLAG FOUND: {flag_str} 🎉🎉🎉')
            else:
                print(f'\n✗ Hash does not match')
        except:
            print(f'Cannot decode as ASCII: {flag}')
    else:
        print('✗ No closing brace "}" found after "CJ{"')
        print(f'Next 100 bytes: {data[offset:offset+100]}')
else:
    print('✗ "CJ{" pattern not found in binary')
