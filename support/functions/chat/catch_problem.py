def catch_problem() -> str:
    return {
        "type": "function",
        "name": "handle_user_problem",
        "function": {
            "description": "Analisa o problema do usuário, oferece conselhos pequenos e sugere atividades baseadas no tipo do problema(apenas se o usuário peça por elas).",
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
                        "description": "Atividades ou práticas sugeridas para aliviar o problema relatado, caso o usuário tenha pedido por elas."
                    }
                },
                "required": ["problem_type", "advice"],
                "additionalProperties": True
            },
            "examples": {
                "user_input": "Consegue me indicar atividades para diminuir o estresse?",  # Exemplo de pedido de atividades
                "returns": {
                    "problem_type": "saúde mental",
                    "advice": "Tente relaxar, respire fundo e pratique atividades que acalmem sua mente.",
                    "activities_suggested": "Realizar exercícios de respiração profunda, caminhada ao ar livre, ouvir música relaxante"  # Apenas se solicitado
                }
            }
        }
    }
