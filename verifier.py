def verify_answer(question, answer):
    answer_lower = answer.lower()

    #  unsure detection
    if "not confident" in answer_lower:
        return {
            "verified": False,
            "confidence": 20,
            "reason": "Model unsure"
        }

    #  very short answer
    if len(answer.strip()) < 10:
        return {
            "verified": False,
            "confidence": 30,
            "reason": "Too short"
        }

    #  special fact correction example
    if "pm of usa" in question.lower():
        if "does not have" in answer_lower or "no prime minister" in answer_lower:
            return {
                "verified": True,
                "confidence": 90,
                "reason": "Correct factual logic"
            }
        else:
            return {
                "verified": False,
                "confidence": 20,
                "reason": "Incorrect fact"
            }

    # default
    return {
        "verified": True,
        "confidence": 80,
        "reason": "Looks reasonable"
    }