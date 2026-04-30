from armoriq import ArmorIQ

client = ArmorIQ(
    api_key="YOUR_ARMORIQ_API_KEY"
)

def verify_ai_action(user_id, metrics):
    """
    Verify if AI explanation generation is allowed
    """

    policy_input = {
        "user_id": user_id,
        "action": "generate_fairness_explanation",
        "resource": "fairness_audit",
        "metrics": metrics
    }

    response = client.evaluate(policy_input)

    return response