def get_location() -> dict:
    return {
        "type": "function",
        "name": "handle_user_location_request",
        "function": {
            "description": "Encontra locais OU PROFISSIONAIS para tratamentos específicos em uma determinada localização.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Tipo de tratamento OU PROFISSIONAIS"
                    },
                    "location": {
                        "type": "string",
                        "description": "Localização desejada."
                    }
                },
                "required": ["service", "location"],
                "additionalProperties": False
            },
            "responses": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Tipo de tratamento OU PROFISSIONAIS."
                    },
                    "location": {
                        "type": "string",
                        "description": "Localização onde o serviço é procurado."
                    }
                },
                "required": ["service", "location"],
                "additionalProperties": False
            },
        },
        "examples": [
            {
                "query_input": "me indique psicólogos no Salgado Filho, Belo Horizonte",
                "returns": {
                    "service": "psicólogos",
                    "location": "Salgado Filho, Belo Horizonte"
                }
            },
            {
                "query_input": "quais são os melhores nutricionistas no centro de São Paulo?",
                "returns": {
                    "service": "nutricionistas",
                    "location": "Centro, São Paulo"
                }
            }
        ]
    }