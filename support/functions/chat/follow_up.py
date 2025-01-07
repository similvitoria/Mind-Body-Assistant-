def follow_up() -> str:
    return {
        "type": "function",
        "name": "follow_up",
        "function": {
            "description": "Acompanha o usuário com conselhos contínuos baseados no problema descrito.",
            "parameters": {
                "type": "object",
                "properties": {
                    "descricao_problema": {
                        "type": "string",
                        "description": "Resumo do problema descrito pelo usuário."
                    },
                    "frequencia": {
                        "type": "string",
                        "description": "Frequência do acompanhamento, como 'diariamente' ou 'semanalmente'."
                    }
                },
                "required": ["descricao_problema", "frequencia"],
                "additionalProperties": False
            }
        }
    }