from flask import request, jsonify, Blueprint
import anthropic
import os

claude_blueprint = Blueprint("claude", __name__)

claude_api_key = os.getenv("claude_api_key")

claude_client = anthropic.Anthropic(
    api_key=claude_api_key
)

@claude_blueprint.route("/talkclaude", methods=["POST"])
def talkclaude():
    try:
        data = request.get_json()

        print("CLAUDE REQUEST:", data)

        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' field"}), 400

        prompt = data["prompt"]

        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        reply = response.content[0].text

        return jsonify({"response": reply})

    except Exception as e:
        print("Claude error:", e)
        return jsonify({"error": str(e)}), 500