#include <node_api.h>

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <algorithm>

#define CHECK(env, status)              \
  if ((status) != napi_ok) {            \
    napi_throw_error((env), NULL, "napi failure"); \
    return NULL;                        \
  }

#pragma pack(push, 1)
typedef struct {
  uint64_t user_id;
  uint64_t issued_at;
  uint16_t name_len;
  char name[48];
  uint8_t role;
  uint64_t checksum;
} Session;
#pragma pack(pop)

static uint64_t compute_checksum(const uint8_t *secret, size_t secret_len,
                                 const uint8_t *data, size_t data_len) {
  uint64_t h = 0xcbf29ce484222325ULL;
  for (size_t i = 0; i < data_len; ++i) {
    uint8_t mix = data[i] ^ secret[i % secret_len];
    h ^= mix;
    h *= 0x100000001b3ULL;
    h ^= (uint64_t)(i & 0xff) << 40;
  }
  return h;
}

static napi_value issue(napi_env env, napi_callback_info info) {
  size_t argc = 2;
  napi_value argv[2];
  napi_status status = napi_get_cb_info(env, info, &argc, argv, NULL, NULL);
  CHECK(env, status);

  if (argc < 2) {
    napi_throw_error(env, NULL, "expected 2 arguments");
    return NULL;
  }

  bool is_buffer = false;
  status = napi_is_buffer(env, argv[0], &is_buffer);
  CHECK(env, status);
  if (!is_buffer) {
    napi_throw_type_error(env, NULL, "secret must be a buffer");
    return NULL;
  }

  uint8_t *secret_data = NULL;
  size_t secret_len = 0;
  status = napi_get_buffer_info(env, argv[0], (void **)&secret_data, &secret_len);
  CHECK(env, status);
  if (secret_len == 0) {
    napi_throw_error(env, NULL, "secret must not be empty");
    return NULL;
  }

  napi_value session_obj = argv[1];

  napi_value val;
  status = napi_get_named_property(env, session_obj, "userId", &val);
  CHECK(env, status);
  double user_id_double = 0;
  status = napi_get_value_double(env, val, &user_id_double);
  CHECK(env, status);

  status = napi_get_named_property(env, session_obj, "role", &val);
  CHECK(env, status);
  uint32_t role = 0;
  status = napi_get_value_uint32(env, val, &role);
  CHECK(env, status);

  status = napi_get_named_property(env, session_obj, "name", &val);
  CHECK(env, status);
  size_t name_len = 0;
  status = napi_get_value_string_utf8(env, val, NULL, 0, &name_len);
  CHECK(env, status);
  char *name_buf = (char *)malloc(name_len + 1);
  if (!name_buf) {
    napi_throw_error(env, NULL, "allocation failed");
    return NULL;
  }
  status = napi_get_value_string_utf8(env, val, name_buf, name_len + 1, &name_len);
  CHECK(env, status);

  Session payload;
  memset(&payload, 0, sizeof(Session));
  payload.user_id = (uint64_t)user_id_double;
  payload.issued_at = (uint64_t)time(NULL);
  payload.role = (uint8_t)role;
  memcpy(payload.name, name_buf, name_len);
  payload.name_len = name_len;

  free(name_buf);

  payload.checksum = 0;
  uint64_t checksum = compute_checksum(secret_data, secret_len,
                                       reinterpret_cast<const uint8_t *>(&payload),
                                       sizeof(Session));
  payload.checksum = checksum;

  napi_value result;
  status = napi_create_buffer_copy(env, sizeof(Session), &payload, NULL, &result);
  CHECK(env, status);
  return result;
}

static napi_value verify(napi_env env, napi_callback_info info) {
  size_t argc = 2;
  napi_value argv[2];
  napi_status status = napi_get_cb_info(env, info, &argc, argv, NULL, NULL);
  CHECK(env, status);

  if (argc < 2) {
    napi_throw_error(env, NULL, "expected 2 arguments");
    return NULL;
  }

  bool is_buffer = false;
  status = napi_is_buffer(env, argv[0], &is_buffer);
  CHECK(env, status);
  if (!is_buffer) {
    napi_throw_type_error(env, NULL, "secret must be a buffer");
    return NULL;
  }

  uint8_t *secret_data = NULL;
  size_t secret_len = 0;
  status = napi_get_buffer_info(env, argv[0], (void **)&secret_data, &secret_len);
  CHECK(env, status);

  status = napi_is_buffer(env, argv[1], &is_buffer);
  CHECK(env, status);
  if (!is_buffer) {
    napi_throw_type_error(env, NULL, "token must be a buffer");
    return NULL;
  }

  uint8_t *token_data = NULL;
  size_t token_len = 0;
  status = napi_get_buffer_info(env, argv[1], (void **)&token_data, &token_len);
  CHECK(env, status);

  if (token_len < sizeof(Session)) {
    napi_throw_error(env, NULL, "token too short");
    return NULL;
  }

  Session payload;
  memcpy(&payload, token_data, sizeof(Session));

  uint64_t checksum = payload.checksum;
  payload.checksum = 0;
  uint64_t expected = compute_checksum(secret_data, secret_len,
                                       reinterpret_cast<const uint8_t *>(&payload),
                                       sizeof(Session));
  if (checksum != expected) {
    napi_throw_error(env, NULL, "invalid signature");
    return NULL;
  }

  size_t name_len = payload.name_len;
  if (name_len > sizeof(payload.name)) {
    name_len = sizeof(payload.name);
  }

  napi_value result;
  status = napi_create_object(env, &result);
  CHECK(env, status);

  napi_value num;
  status = napi_create_double(env, (double)payload.user_id, &num);
  CHECK(env, status);
  status = napi_set_named_property(env, result, "userId", num);
  CHECK(env, status);

  status = napi_create_uint32(env, payload.role, &num);
  CHECK(env, status);
  status = napi_set_named_property(env, result, "role", num);
  CHECK(env, status);

  napi_value name_value;
  status = napi_create_string_utf8(env, payload.name, name_len, &name_value);
  CHECK(env, status);
  status = napi_set_named_property(env, result, "name", name_value);
  CHECK(env, status);

  return result;
}

static napi_value init(napi_env env, napi_value exports) {
  napi_status status;
  napi_value issue_fn;
  status = napi_create_function(env, "issue", NAPI_AUTO_LENGTH, issue, NULL, &issue_fn);
  CHECK(env, status);
  status = napi_set_named_property(env, exports, "issue", issue_fn);
  CHECK(env, status);

  napi_value verify_fn;
  status = napi_create_function(env, "verify", NAPI_AUTO_LENGTH, verify, NULL, &verify_fn);
  CHECK(env, status);
  status = napi_set_named_property(env, exports, "verify", verify_fn);
  CHECK(env, status);
  return exports;
}

NAPI_MODULE(NODE_GYP_MODULE_NAME, init)
