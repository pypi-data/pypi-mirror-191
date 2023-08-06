import base64
import random

import siphash24

#
# Hashing
#


def get_siphash13_u64(b: bytes) -> int:
    byt = siphash24.siphash13(b, key=b"").digest()
    return int.from_bytes(byt, byteorder="little", signed=False)


def get_siphash13_hex(b: bytes) -> str:
    return siphash24.siphash13(b, key=b"").digest()[::-1].hex()


def get_base32(hex: str) -> str:
    return base64.b32encode(hex.encode("utf-8")).decode("utf-8")


def get_external_id_bytes(b: bytes, prefix: str) -> str:
    hex = get_siphash13_hex(b)
    b32 = get_base32(hex)
    result = b32.lower().replace("=", "")
    return f"{prefix}-{result}"


#
# Consistent EIDs
#


def get_external_id_str(name: str, prefix: str) -> str:
    return get_external_id_bytes(name.encode("utf-8"), prefix)


def get_db_eid(database_name: str) -> str:
    return get_external_id_str(database_name, "db")


def get_table_eid(table_name: str) -> str:
    return get_external_id_str(table_name, "table")


def get_job_eid(job_name: str) -> str:
    return get_external_id_str(job_name, "job")


def get_org_eid(organization_name: str) -> str:
    return get_external_id_str(organization_name, "org")


def get_user_eid(user_name: str) -> str:
    return get_external_id_str(user_name, "user")


#
# Random IDs
#


def get_eval_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_str(byt, "eval")


def get_req_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes(byt, "req")


def get_mat_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes(byt, "mat")


def get_mat_group_eid() -> str:
    byt = random.randbytes(16)
    return get_external_id_bytes(byt, "mg")
