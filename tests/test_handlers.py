import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from bot.telegram_bot import set_subject_command, _core_ai_handler

@pytest.mark.asyncio
async def test_set_subject_modifies_prompt():
    """
    Integration Test: Verifies that setting a subject via set_subject_command
    correctly modifies the prompt passed to the AI in _core_ai_handler.
    """
    with patch("bot.telegram_bot.ask_gemini_stream") as mock_ask_gemini:
        async def mock_generator(*args, **kwargs):
            if False:
                yield

        mock_ask_gemini.side_effect = mock_generator

        update = MagicMock()
        context = MagicMock()

        update.message.reply_text = AsyncMock()

        mock_placeholder = MagicMock()
        mock_placeholder.edit_text = AsyncMock()
        update.message.reply_text.return_value = mock_placeholder

        context.user_data = {}
        context.chat_data = {}

        context.args = ["Quantum", "Mechanics"]
        await set_subject_command(update, context)

        assert context.user_data['study_subject'] == "Quantum Mechanics"

        update.message.text = "Tell me about the uncertainty principle."
        update.effective_user.id = 12345
        await _core_ai_handler(
            update,
            context,
            prompt_text=update.message.text,
            conversation_history=[]
        )

        mock_ask_gemini.assert_called_once()

        call_args, _ = mock_ask_gemini.call_args
        prompt_sent_to_ai = call_args[0]

        expected_start = "In the context of my study subject, which is 'Quantum Mechanics'"
        expected_end = "Tell me about the uncertainty principle."

        assert prompt_sent_to_ai.startswith(expected_start)
        assert prompt_sent_to_ai.endswith(expected_end)