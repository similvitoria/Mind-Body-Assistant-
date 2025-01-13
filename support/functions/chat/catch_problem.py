def catch_problem() -> str:
    return {
        "type": "function",
        "name": "handle_user_problem",
        "function": {
            "description": "Analisa o problema do usuário com cuidado indepente do tamanho da mensagem sendo gentil e oferecendo conselhos pequenos porem efetivos e ao oferecer apoio pergunte se há algo mais que possa fazer",
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
                        "description": "Classificação do problema, pode ser 'saúde física' ou 'saúde mental'.",
                        "default": "Indeterminado"
                    },
                    "advice": {
                        "type": "string",
                        "description": "Conselhos ou sugestões baseados no problema analisado.",
                        "default": "Não conseguimos identificar o problema, mas estamos aqui para ajudar!"
                    },
                    "activities_suggested": {
                        "type": "string",
                        "description": "Atividades ou práticas sugeridas para aliviar o problema relatado, caso o usuário tenha pedido por elas.",
                        "default": "Nenhuma atividade sugerida no momento. Por favor, forneça mais detalhes."
                    }
                },
                "required": ["problem_type", "advice"],
                "additionalProperties": True
            },
            "examples": {
                "user_input": "Consegue me indicar atividades para diminuir o estresse?", 
                "returns": {
                    "problem_type": "saúde mental",
                    "advice": "Tente relaxar, respire fundo e pratique atividades que acalmem sua mente.",
                    "activities_suggested": "Realizar exercícios de respiração profunda, caminhada ao ar livre, ouvir música relaxante"  
                }
            }
        }
    }
