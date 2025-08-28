from typing import Dict
from pydantic import BaseModel, Field
from portia import (
    Tool,
    ToolRunContext,
    CustomClarification,
)
import json


class ClarificationToolSchema(BaseModel):
    """Schema defining the inputs for the ClarificationTool.

    This schema expects a string value to take the authorization code from the user."""

    user_input: str = Field(
        ...,
        description="The feedback from the user.",
    )
    auth_code: str = Field(
        ...,
        description="The authorization code from the user.",
    )


class ClarificationTool(Tool[Dict[str, str]]):
    """A tool for asking feedback from the user on the legal document.
    The tool expects a JSON string containing the consent url.
    in the following format:
    {
        "consent_url": "The url for oauth",
    }
    The tool will:
    1. Present the url to the user.
    2. Wait for user to authorize.
    3. Return the code.
    """

    id: str = "clarification"
    name: str = "Clarification Tool"
    description: str = "Used to get the authorization code from the user."
    args_schema: type[BaseModel] = ClarificationToolSchema
    output_schema: tuple[str, str] = (
        json.dumps(
            {
                "type": "object",
                "properties": {
                    "auth_code": {"type": "string"},
                },
            }
        ),
        "Returns collected field value and status",
    )

    def run(
        self, ctx: ToolRunContext, user_input: str, auth_code: str
    ) -> str | CustomClarification:
        print("🔍 Clarification Tool")
        print(f"Received user_input: '{user_input}'")
        print(f"Received auth_code: '{auth_code}'")

        # If we have the auth_code, return it directly
        if auth_code and auth_code.strip():
            result = auth_code.strip()
            print(f"Returning auth_code: '{result}'")
            return {"auth_code": result}

        print("Raising clarification for empty auth_code.")
        clarification = CustomClarification(
            name="user_feedback",
            user_guidance=f"{user_input} .Please provide the authorization code.",
            argument_name="auth_code",
            plan_run_id=str(ctx.plan_run.id),
        )
        return clarification
