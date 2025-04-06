import re
from typing import Dict, Optional

class PHPFuck():
    def __init__(self):
        # simple constant
        arr_str = "[].[]"  # "ArrayArray"
        zero = "([]^[])"
        one = "([]^[[]])"

        # generate digits
        nums = [zero, one]
        for i in range(2, 10):
            nums.append('+'.join([nums[1]]*i))

        self.nums = nums
        # using `Aray0123456789` & xor to generate printable ascii char
        self.char_mapping = {
            '\t': f'{nums[1]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '\n': f'{nums[2]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '\x0b': f'({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            '\x0c': f'{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '\r': f'{nums[5]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            ' ': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]',
            '!': f'{nums[2]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            '"': f'{nums[1]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            '#': f'{nums[0]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            '$': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]',
            '%': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]',
            '&': f'{nums[5]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            "'": f'{nums[4]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            '(': f'{nums[0]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            ')': f'{nums[1]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '*': f'{nums[2]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '+': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            ',': f'{nums[4]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '-': f'{nums[5]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '.': f'{nums[6]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '/': f'{nums[7]}.[][[]]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '0': f'{nums[0]}.[][[]]',
            '1': f'{nums[1]}.[][[]]',
            '2': f'{nums[2]}.[][[]]',
            '3': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]',
            '4': f'{nums[4]}.[][[]]',
            '5': f'{nums[5]}.[][[]]',
            '6': f'{nums[6]}.[][[]]',
            '7': f'{nums[7]}.[][[]]',
            '8': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '9': f'{nums[2]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            ':': f'{nums[1]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            ';': f'{nums[0]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            '<': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '=': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[4]}]',
            '>': f'{nums[5]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            '?': f'{nums[4]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            '@': f'{nums[2]}.[][[]]^({arr_str})[{nums[1]}]',
            'A': f'({arr_str})[{nums[0]}]',
            'B': f'{nums[0]}.[][[]]^({arr_str})[{nums[1]}]',
            'C': f'{nums[1]}.[][[]]^({arr_str})[{nums[1]}]',
            'D': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]',
            'E': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]',
            'F': f'{nums[4]}.[][[]]^({arr_str})[{nums[1]}]',
            'G': f'{nums[5]}.[][[]]^({arr_str})[{nums[1]}]',
            'H': f'{nums[1]}.[][[]]^({arr_str})[{nums[4]}]',
            'I': f'{nums[0]}.[][[]]^({arr_str})[{nums[4]}]',
            'J': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]',
            'K': f'{nums[2]}.[][[]]^({arr_str})[{nums[4]}]',
            'L': f'{nums[5]}.[][[]]^({arr_str})[{nums[4]}]',
            'M': f'{nums[4]}.[][[]]^({arr_str})[{nums[4]}]',
            'N': f'{nums[7]}.[][[]]^({arr_str})[{nums[4]}]',
            'O': f'{nums[6]}.[][[]]^({arr_str})[{nums[4]}]',
            'P': f'{nums[1]}.[][[]]^({arr_str})[{nums[3]}]',
            'Q': f'{nums[0]}.[][[]]^({arr_str})[{nums[3]}]',
            'R': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            'S': f'{nums[2]}.[][[]]^({arr_str})[{nums[3]}]',
            'T': f'{nums[5]}.[][[]]^({arr_str})[{nums[3]}]',
            'U': f'{nums[4]}.[][[]]^({arr_str})[{nums[3]}]',
            'V': f'{nums[7]}.[][[]]^({arr_str})[{nums[3]}]',
            'W': f'{nums[6]}.[][[]]^({arr_str})[{nums[3]}]',
            'X': f'{nums[2]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'Y': f'({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'Z': f'{nums[0]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '[': f'{nums[1]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '\\': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            ']': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '^': f'{nums[4]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '_': f'{nums[5]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            '`': f'{nums[0]}.[][[]]^{nums[1]}.[][[]]^({arr_str})[{nums[3]}]',
            'a': f'({arr_str})[{nums[3]}]',
            'b': f'{nums[1]}.[][[]]^{nums[2]}.[][[]]^({arr_str})[{nums[3]}]',
            'c': f'{nums[0]}.[][[]]^{nums[2]}.[][[]]^({arr_str})[{nums[3]}]',
            'd': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[3]}]',
            'e': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[3]}]',
            'f': f'{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]',
            'g': f'{nums[2]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[3]}]',
            'h': f'{nums[1]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'i': f'{nums[0]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'j': f'({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'k': f'{nums[2]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'l': f'{nums[5]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'm': f'{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'n': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[1]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'o': f'{nums[6]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[3]}]^({arr_str})[{nums[4]}]',
            'p': f'{nums[1]}.[][[]]^({arr_str})[{nums[0]}]',
            'q': f'{nums[0]}.[][[]]^({arr_str})[{nums[0]}]',
            'r': f'({arr_str})[{nums[1]}]',
            's': f'{nums[2]}.[][[]]^({arr_str})[{nums[0]}]',
            't': f'{nums[5]}.[][[]]^({arr_str})[{nums[0]}]',
            'u': f'{nums[4]}.[][[]]^({arr_str})[{nums[0]}]',
            'v': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[1]}]',
            'w': f'{nums[6]}.[][[]]^({arr_str})[{nums[0]}]',
            'x': f'{nums[0]}.[][[]]^{nums[1]}.[][[]]^({arr_str})[{nums[4]}]',
            'y': f'({arr_str})[{nums[4]}]',
            'z': f'{nums[1]}.[][[]]^{nums[2]}.[][[]]^({arr_str})[{nums[4]}]',
            '{': f'{nums[0]}.[][[]]^{nums[2]}.[][[]]^({arr_str})[{nums[4]}]',
            '|': f'{nums[1]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[4]}]',
            '}': f'{nums[0]}.[][[]]^{nums[4]}.[][[]]^({arr_str})[{nums[4]}]',
            '~': f'{nums[4]}.[][[]]^({arr_str})[{nums[0]}]^({arr_str})[{nums[1]}]^({arr_str})[{nums[4]}]'}

    def encode(self, code, eval_mode=None):
        def clean_code(code):
            return code.replace('\n', '').replace(' ', '')

        def basic_encode(code):
            return '.'.join([f"({self.char_mapping[c] if c in self.char_mapping else fix_missing_char(c)})" for c in code])

        def encode_number(num):
            return f"{self.nums[0]}+({'.'.join([self.nums[int(n)] for n in str(num)])})"

        def fix_missing_char(char, compatiable=True):
            # to compatiable with PHP < 7.2.0: `mb_chr` only support PHP >= 7.2.0
            if compatiable:
                str_getcsv = basic_encode("str_getcsv")
                mb_chr = basic_encode('IntlChar,chr')
                char_code = encode_number(ord(char))
                return f"({str_getcsv})({mb_chr})({char_code})"
            else:
                return f"({basic_encode('mb_chr')})({basic_encode(str(ord(char)))})"

        if eval_mode == 'create_function':
            code = code.replace('"', '""')

        code = basic_encode(code)

        if not eval_mode:
            return code

        elif eval_mode == 'create_function':
            create_function = basic_encode("create_function")
            str_getcsv = basic_encode("str_getcsv")
            comma = basic_encode(",")
            quote = basic_encode('"')

            """
            1. create_function(...str_getcsv(',"YOUR_CODE"') )
            2. create_function(...['', 'YOURCODE'])
            3. create_function('', 'YOURCODE')
            """

            eval_code = f"""({create_function})(
                ...({str_getcsv})({comma}.{quote}.{code}.{quote})
            )()
            """

        elif eval_mode == 'assert':  # only support PHP < 7.1
            assert_func = basic_encode('assert')
            prefix = basic_encode('(function(){')
            postfix = basic_encode(';return 1;})()')
            eval_code = f"""
            ({assert_func})(
                ({prefix}).({code}).({postfix})
            )
            """

        return clean_code(eval_code)

class PHPFuckDecoder:
    def __init__(self):
        # Initialize the basic building blocks
        self.arr_str = "[].[]"  # "ArrayArray"
        self.zero = "([]^[])"
        self.one = "([]^[[]])"
        
        # Generate number mappings
        self.number_patterns = self._generate_number_patterns()
        
        # Create reverse mapping from encoded patterns to characters
        self.reverse_mapping = self._generate_reverse_mapping()
    
    def _generate_number_patterns(self) -> Dict[str, int]:
        """Generate mappings for numbers 0-9 in PHPFuck format"""
        patterns = {
            self.zero: 0,
            self.one: 1
        }
        
        # Generate patterns for numbers 2-9
        one_pattern = self.one
        for i in range(2, 10):
            pattern = '+'.join([one_pattern] * i)
            patterns[pattern] = i
            
        return patterns
    
    def _generate_reverse_mapping(self) -> Dict[str, str]:
        """Generate reverse mapping from encoded patterns to characters"""
        phpfuck = PHPFuck()  # Create instance of original encoder
        reverse_map = {}
        
        # Generate reverse mapping for each character
        for char, pattern in phpfuck.char_mapping.items():
            reverse_map[pattern] = char

        return reverse_map
    
    def _simplify_expression(self, expr: str) -> str:
        """Simplify PHPFuck expressions by evaluating XOR operations"""
        # Remove whitespace
        expr = expr.replace(' ', '')
        
        # Handle array access patterns
        arr_access = f"({self.arr_str})"
        if arr_access in expr:
            # Extract the index number
            parts = expr.split(arr_access)
            indices = []
            for part in parts[1:]:
                if part.startswith('[') and ']' in part:
                    index_expr = part[1:part.index(']')]
                    for pattern, num in self.number_patterns.items():
                        if pattern == index_expr:
                            indices.append(num)
                            break
            
            # Convert array access to character based on index
            if len(indices) == 1:
                return f"Array[{indices[0]}]"
        
        return expr
    
    def decode(self, encoded: str) -> str:
        """Decode a PHPFuck encoded string back to its original form"""
        # Remove PHP tags and whitespace
        encoded = encoded.replace('<?php', '').replace('?>', '').strip()
        
        # Split into individual character expressions
        expressions = re.findall(r'\((.*?)\)', encoded)
        
        decoded = ""
        for expr in expressions:
            # Skip empty expressions
            if not expr:
                continue
                
            # Simplify the expression
            simplified = self._simplify_expression(expr)
            
            # Look up in reverse mapping
            if simplified in self.reverse_mapping:
                decoded += self.reverse_mapping[simplified]
            else:
                # Handle complex expressions
                components = expr.split('^')
                result_char = self._decode_complex_expression(components)
                if result_char:
                    decoded += result_char
                else:
                    decoded += f"[Unknown:{expr}]"
        
        return decoded
    
    def _decode_complex_expression(self, components: list) -> Optional[str]:
        """Decode complex expressions involving multiple XOR operations"""
        simplified_components = [self._simplify_expression(c) for c in components]
        print(simplified_components)
        
        # Try to match against reverse mapping
        pattern = '^'.join(simplified_components)
        if pattern in self.reverse_mapping:
            return self.reverse_mapping[pattern]
        
        return None

# Example usage
def main():
    decoder = PHPFuckDecoder()
    
    # Example encoded string (add your encoded string here)
    encoded = """<?php ([].[])[([].[]^[]).([].[]^[[]])]^([].[])[([].[]^[]).([].[]^[[]])] ?>"""
    
    try:
        decoded = decoder.decode(encoded)
        print(f"Decoded string: {decoded}")
    except Exception as e:
        print(f"Error decoding: {str(e)}")

if __name__ == "__main__":
    main()