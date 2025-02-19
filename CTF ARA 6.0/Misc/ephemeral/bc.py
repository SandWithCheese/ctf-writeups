from solcx import compile_source

exploit_source = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Exploit {
    fallback() external payable {
        assembly {
            mstore(0, caller())
            return(0, 32)
        }
    }
}
'''

compiled_sol = compile_source(exploit_source)
bytecode = compiled_sol['<stdin>:Exploit']['bin']
print("Bytecode:", bytecode)
