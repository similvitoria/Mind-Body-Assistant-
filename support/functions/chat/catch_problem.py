def catch_problem() -> str:
    return {
        "type": "function",
        "name": "handle_user_problem",
        "function": {
            "description": "Analisa o problema do usuário, oferece conselhos e sugere atividades baseadas no tipo do problema.",
            "parameters": {
            "type": "object",
            "properties": {
                "user_input": {
                "type": "string",
                "description": "Descrição do problema fornecida pelo usuário."
                }
            },
            "required": ["user_input"],
            "additionalProperties": True
            },
            "responses": {
            "type": "object",
            "properties": {
                "problem_type": {
                "type": "string",
                "description": "Classificação do problema, pode ser 'saúde física' ou 'saúde mental'."
                },
                "advice": {
                "type": "string",
                "description": "Conselhos ou sugestões baseados no problema analisado."
                },
                "activities_suggested": {
                "type": "string",
                "description": "Atividades ou práticas sugeridas para aliviar o problema relatado."
                }
            },
            "required": ["problem_type", "advice", "activities_suggested"],
            "additionalProperties": True
            }
        }
    }


