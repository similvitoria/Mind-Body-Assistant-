def get_location() -> dict:
    return {
        "type": "function",
        "name": "handle_user_location_request",
        "function": {
            "description": "Analisa a solicitação do usuário para encontrar serviços específicos em uma determinada localização.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_input": {
                        "type": "string",
                        "description": "Descrição da busca fornecida pelo usuário, incluindo o tipo de serviço e a localização desejada."
                    }
                },
                "required": ["query_input"],
                "additionalProperties": True
            },
            "responses": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Tipo de serviço solicitado pelo usuário."
                    },
                    "location": {
                        "type": "string",
                        "description": "Localização onde o serviço é procurado."
                    }
                },
                "required": ["service", "location"],
                "additionalProperties": True
            },
            "examples": {
                "query_input": "me indique psicologos no salgado filho, belo horizonte",
                "returns": {
                    "service": "psicólogos",
                    "location": "Salgado Filho, Belo Horizonte"
                }
            }
        }
    }