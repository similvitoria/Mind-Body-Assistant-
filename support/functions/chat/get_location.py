def get_location():
    return {
        "type": "function",
        "name": "get_location",
        "function": {
            "description": """Gera uma consulta de tratamentos médicos próximos, baseando-se no problema de saúde informado e na localização fornecida. 
            Os parâmetros DEVEM ser fornecidos EXATAMENTE nesta ordem:
            1. 'problem' - Tipo de tratamento ou especialidade médica
            2. 'location' - Nome da cidade
            3. 'neighborhood' - Nome do bairro
            A sequência é obrigatória: problem -> location -> neighborhood. O resultado será uma query de busca para tratamentos próximos, que pode ser utilizada em uma API de busca de estabelecimentos de saúde.""",
            "parameters": {
                "type": "object",
                "required": ["problem", "location", "neighborhood"],
                "additionalProperties": False,
                "propertyOrder": ["problem", "location", "neighborhood"],
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "PRIMEIRO PARÂMETRO - Tipo do tratamento ou especialidade médica",
                        "enum": [
                            "psicólogo",
                            "psiquiatra",
                            "terapia",
                            "fisioterapia",
                            "ortopedia",
                            "clínica médica",
                            "hospital",
                            "pronto socorro",
                            "nutricionista",
                            "academia",
                            "centro de reabilitação"
                        ]
                    },
                    "location": {
                        "type": "string",
                        "description": "SEGUNDO PARÂMETRO - Nome da cidade (ex: 'São Paulo', 'Rio de Janeiro')"
                    },
                    "neighborhood": {
                        "type": "string",
                        "description": "TERCEIRO PARÂMETRO - Nome do bairro (ex: 'Moema', 'Pinheiros')"
                    }
                }
            },
            "returns": {
                "type": "string",
                "description": "Uma consulta que pode ser utilizada para buscar tratamentos médicos e especialidades próximas ao usuário, com base na cidade e bairro fornecidos."
            }
        }
    }
