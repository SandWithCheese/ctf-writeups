#include "aes.h"

void add_round_key(state_t *state, const u8 *round_key, u8 round){
    for(u8 i = 0; i < 4; i++){
        for(u8 j = 0; j < 4; j++){
            (*state)[i][j] ^= round_key[(round * AES_BLOCK_SIZE) + (i * 4) + j];
        }
    }
}

u8 xtime(u8 x){
    return ((x << 1) ^ (((x >> 7) & 1) * 0x1b));
}

void sub_bytes(state_t *state){
    for (u8 i = 0; i < 4; i++){
        for (u8 j = 0; j < 4; j++){
            (*state)[i][j] = getSBOX((*state)[i][j]);
        }
    }
}

void inv_sub_bytes(state_t *state){
    for(u8 i = 0; i < 4; i ++){
        for (u8 j = 0; j < 4; j++) {
            (*state)[i][j] = invSBOX((*state)[i][j]);
        }
    }
}

void shift_rows(state_t *state){
    u8 tmp;

    tmp            = (*state)[0][1];
    (*state)[0][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[3][1];
    (*state)[3][1] = tmp;

    tmp            = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = tmp;

    tmp            = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = tmp;

    tmp            = (*state)[0][3];
    (*state)[0][3] = (*state)[3][3];
    (*state)[3][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[1][3];
    (*state)[1][3] = tmp;
}

void inv_shift_rows(state_t *state){
    u8 tmp;

    tmp            = (*state)[3][1];
    (*state)[3][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[0][1];
    (*state)[0][1] = tmp;

    tmp            = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = tmp;

    tmp            = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = tmp;

    tmp            = (*state)[0][3];
    (*state)[0][3] = (*state)[1][3];
    (*state)[1][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[3][3];
    (*state)[3][3] = tmp;
}

void mix_columns(state_t *state){
    u8 t, u, tmp;

    for(u8 i = 0; i < 4; i++){
        
        tmp = (*state)[i][0];
        t = (*state)[i][0] ^ (*state)[i][1] ^ (*state)[i][2] ^ (*state)[i][3];
        u = (*state)[i][0] ^ (*state)[i][1]; u = xtime(u); (*state)[i][0] ^= u ^ t;
        u = (*state)[i][1] ^ (*state)[i][2]; u = xtime(u); (*state)[i][1] ^= u ^ t;
        u = (*state)[i][2] ^ (*state)[i][3]; u = xtime(u); (*state)[i][2] ^= u ^ t;
        u = (*state)[i][3] ^ tmp           ; u = xtime(u); (*state)[i][3] ^= u ^ t;
    }
}

u8 multiply(u8 x, u8 y) {
  return (((y & 1) * x) ^
       ((y>>1 & 1) * xtime(x)) ^
       ((y>>2 & 1) * xtime(xtime(x))) ^
       ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^
       ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))));
}

void inv_mix_columns(state_t *state){
    int i;
    u8 a, b, c, d;
    for (i = 0; i < 4; ++i){ 

        a = (*state)[i][0];
        b = (*state)[i][1];
        c = (*state)[i][2];
        d = (*state)[i][3];

        (*state)[i][0] = multiply(a, 0x0e) ^ multiply(b, 0x0b) ^ multiply(c, 0x0d) ^ multiply(d, 0x09);
        (*state)[i][1] = multiply(a, 0x09) ^ multiply(b, 0x0e) ^ multiply(c, 0x0b) ^ multiply(d, 0x0d);
        (*state)[i][2] = multiply(a, 0x0d) ^ multiply(b, 0x09) ^ multiply(c, 0x0e) ^ multiply(d, 0x0b);
        (*state)[i][3] = multiply(a, 0x0b) ^ multiply(b, 0x0d) ^ multiply(c, 0x09) ^ multiply(d, 0x0e);
    }
}

void key_expansion(u8 *round_key, u8 *key){
    u8 i,j,k;
    u8 tmp[4];

    for(i = 0; i < 4; i++){
        round_key[(i * 4) + 0] = key[(i * 4) + 0];
        round_key[(i * 4) + 1] = key[(i * 4) + 1];
        round_key[(i * 4) + 2] = key[(i * 4) + 2];
        round_key[(i * 4) + 3] = key[(i * 4) + 3];
    }
    for(i = 4; i < 4 * (NR_ROUND + 1); i++){
        k = (i - 1) * 4;
        tmp[0] = round_key[k + 0];
        tmp[1] = round_key[k + 1];
        tmp[2] = round_key[k + 2];
        tmp[3] = round_key[k + 3];

        if(i % 4 == 0){
            const u8 tmp0 = tmp[0];
            tmp[0] = tmp[1];
            tmp[1] = tmp[2];
            tmp[2] = tmp[3];
            tmp[3] = tmp0;
            
            tmp[0] = getSBOX(tmp[0]);
            tmp[1] = getSBOX(tmp[1]);
            tmp[2] = getSBOX(tmp[2]);
            tmp[3] = getSBOX(tmp[3]);

            tmp[0] ^= Rcon[i/4];
        }
        j = i * 4;
        k = (i - 4) * 4;
        round_key[j + 0] = round_key[k + 0] ^ tmp[0];
        round_key[j + 1] = round_key[k + 1] ^ tmp[1];
        round_key[j + 2] = round_key[k + 2] ^ tmp[2];
        round_key[j + 3] = round_key[k + 3] ^ tmp[3];
    }
}

void AES_encrypt(state_t *state, u8 *round_key){

    u8 round = 0;
    add_round_key(state, round_key, round);

    for(round = 1;; ++round ){
        sub_bytes(state);
        shift_rows(state);

        if(round == NR_ROUND) break;

        mix_columns(state);
        add_round_key(state, round_key, round);
    }

    add_round_key(state, round_key, round); 
}

void AES_decrypt(state_t *state, u8 *round_key){
    
    u8 round = 0;
    add_round_key(state, round_key, NR_ROUND);

    for (round = (NR_ROUND - 1);; --round) {
        inv_shift_rows(state);
        inv_sub_bytes(state);   
        add_round_key(state, round_key, round);
        
        if(round == 0) break;

        inv_mix_columns(state);
    }
}

void xor_bytes(u8 *dst, u8 *src){
    for(int i=0; i<AES_BLOCK_SIZE; i++){
        dst[i] ^= src[i];
    }
}

int pad(u8 *plain_state, int datalen){
    u8 pad_len = AES_BLOCK_SIZE - (datalen % AES_BLOCK_SIZE);
    for(int idx = 0; idx < pad_len; idx++){
        plain_state[datalen + idx] = pad_len;
    }
    return datalen + pad_len;
}

int unpad(u8 *pad_state, int padlen){
    u8 last_byte = *(pad_state + padlen - 1);
    if(last_byte < 1 || last_byte > AES_BLOCK_SIZE){
        return -1;
    } else {
        for (int i = 0; i < last_byte; i++) {
            if (last_byte != *(pad_state + padlen - 1 - i)) {
                return -1;
            }
            *(pad_state + padlen - 1 - i) = '\0';
        }
    }
    u8 data_len = padlen - last_byte;
    for (int idx = padlen; idx >= data_len; idx--) {
        pad_state[idx] = '\0';
    }
    return padlen - last_byte;
}

void mode_CBC_encrypt(aes_ctx_t *ctx, u8 *plaintext, size_t length, loff_t offset){
    key_expansion(ctx->round_key, ctx->key);

    u8 iv[AES_BLOCK_SIZE];
    memcpy(iv, ctx->iv, AES_BLOCK_SIZE);

    for(size_t idx = 0; idx < length; idx += AES_BLOCK_SIZE){
        xor_bytes(plaintext + idx, iv);
        AES_encrypt((state_t*)(plaintext + idx), ctx->round_key);
        memcpy(iv, plaintext + idx, AES_BLOCK_SIZE);
    }
    memcpy(ctx->data + offset, plaintext, length);
}

void mode_CBC_decrypt(aes_ctx_t *ctx, u8 *ciphertext, size_t length, loff_t offset){
    key_expansion(ctx->round_key, ctx->key);

    u8 iv[AES_BLOCK_SIZE], prev[AES_BLOCK_SIZE];
    memcpy(iv, ctx->iv, AES_BLOCK_SIZE);

    for (size_t idx = 0; idx < length; idx += AES_BLOCK_SIZE) {
        memcpy(prev, ciphertext + idx, AES_BLOCK_SIZE);
        AES_decrypt((state_t*)(ciphertext + idx), ctx->round_key);
        xor_bytes(ciphertext + idx, iv);
        memcpy(iv, prev, AES_BLOCK_SIZE);
    }
    if(unpad(ciphertext, length) == -1) return;
    memcpy(ctx->data + offset, ciphertext, length);
}