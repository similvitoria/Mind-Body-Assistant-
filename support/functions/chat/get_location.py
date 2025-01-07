def get_location() -> str:
    return {
        "type": "function",
        "name": "get_location",
        "function": {
            "description": "Sugere locais próximos para tratamento com base no problema identificado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo_tratamento": {
                        "type": "string",
                        "description": "Indica se o tratamento é para saúde física ou mental."
                    }
                },
                "required": ["tipo_tratamento"],
                "additionalProperties": False
            }
        }
    }