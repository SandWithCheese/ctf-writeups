#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

bool check2(unsigned long param_1, unsigned long param_2)

{
    bool bVar1;
    unsigned long local_28;
    unsigned long local_20;
    int local_18;
    int local_14;
    unsigned long local_10;

    if (param_2 == 0) {
        bVar1 = false;
    }
    else {
        local_18 = 0;
        for (local_10 = param_2; local_10 != 0; local_10 = local_10 >> 2) {
            local_18 = local_18 + ((unsigned int)local_10 & 1);
        }
        if (local_18 < 7) {
            bVar1 = false;
        }
        else {
            local_14 = 0;
            for (local_20 = param_1; local_28 = param_2, local_20 != 0; local_20 = local_20 / 10) {
                local_14 = local_14 +
                    (int)local_20 + ((int)(local_20 / 10 << 2) + (int)(local_20 / 10)) * -2;
            }

            printf("local_14: %d\n", local_14);

            for (; local_28 != 0; local_28 = local_28 / 10) {
                local_14 = local_14 -
                    ((int)local_28 + ((int)(local_28 / 10 << 2) + (int)(local_28 / 10)) * -2);
            }

            printf("local_14: %d\n", local_14);

            bVar1 = local_14 == 105;
        }
    }
    return bVar1;
}


bool check3(uint64_t param_1) {
    uint8_t bVar1;            // To count set bits in local_28
    uint32_t uVar2;           // To extract lower 32 bits of local_40
    bool bVar3;               // Result flag
    uint64_t local_40;        // Temporary storage for shifting param_1
    uint64_t local_28;        // Reconstructed value
    uint64_t local_20;        // Loop variable for counting set bits

    // Check if param_1, when cast to signed, is negative
    if ((int64_t)param_1 < 0) {
        local_28 = 0;
        local_40 = param_1;

        // Loop to shift local_40 and construct local_28
        while (local_40 != 0) {
            uVar2 = (uint32_t)local_40;   // Get lower 32 bits
            local_40 = local_40 >> 1;     // Right shift local_40 by 1

            // Count the number of set bits in local_28
            bVar1 = 0;
            for (local_20 = local_28; local_20 != 0; local_20 = local_20 >> 1) {
                bVar1++;
            }

            // Set the corresponding bit in local_28
            local_28 |= (uint64_t)(uVar2 & 1) << (bVar1 & 63);
        }

        printf("param_1: %lu\n", param_1);
        printf("local_28: %lu\n", local_28);

        // Compare reconstructed local_28 with param_1
        bVar3 = (param_1 == local_28);
    }
    else {
        bVar3 = false;
    }

    return bVar3;
}


bool check4(uint64_t param_1, uint64_t param_2)

{
    bool bVar1;
    uint64_t local_10;

    printf("param_2: %lu\n", param_2);

    if (((param_2 & 1) == 0) || (param_2 == 1)) {
        bVar1 = false;
    }
    else {
        local_10 = param_1;
        if (param_2 <= param_1) {
            local_10 = param_2;
        }

        printf("local_10: %lu\n", local_10);

        for (; (local_10 != 0 && ((param_1 % local_10 != 0 || (param_2 % local_10 != 0))));
            local_10 = local_10 - 1) {
        }

        printf("local_10: %lu\n", local_10);

        bVar1 = local_10 == 1;
    }
    return bVar1;
}






int main() {
    // unsigned long param_1 = 9223372036854775808 * 2 - 1;
    // unsigned long param_1 = 18446744073709551615;
    unsigned long param_1 = -1;
    unsigned long param_2 = 7;

    if (check4(param_1, param_2)) {
        printf("Correct\n");
    }
    else {
        printf("Incorrect\n");
    }

    return 0;
}