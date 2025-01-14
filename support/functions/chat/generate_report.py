def generate_report() -> str: 
    return {
        "type": "function",
        "name": "generate_report",
        "function": {
            "description": "Gera um relatório detalhado com base na interação.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_hora": {"type": "string", "description": "Data e hora da interação."},
                    "problema": {"type": "string", "description": "Resumo do problema relatado pelo usuário."},
                    "conselhos": {"type": "string", "description": "Conselhos fornecidos pelo chatbot."},
                    "locais": {"type": "string", "description": "Locais recomendados, se aplicável."},
                    "atividades": {"type": "string", "description": "Atividades sugeridas, se aplicável."}
                },
                "required": ["data_hora", "problema", "conselhos", "locais", "atividades"],
                "additionalProperties": False
            },
            "strict": True
        }
    }