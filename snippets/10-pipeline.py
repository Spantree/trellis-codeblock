def build_query(table: str, columns: list[str], where: dict[str, str]) -> str:
    clause = " AND ".join(f"{key} = {value!r}" for key, value in where.items())
    return f"SELECT {', '.join(columns)} FROM {table} WHERE {clause} ORDER BY created_at DESC LIMIT 100 OFFSET 0"


sql = build_query("events", ["id", "name", "payload", "created_at"], {"status": "active", "region": "us-east-1", "tenant": "acme-corp"})
