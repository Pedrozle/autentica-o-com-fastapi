import pytest

from src.services.emailservice import EmailService

subj = "Email Teste Service"
corpo_email = """
    <h1>Este é um email de teste</h1>
    <p>Tudo deve funcionar corretamenteo</p>
    <p>Ignore este email</p>
"""
email_seg = "pedrozle@outlook.com"


@pytest.fixture
def emailservice():
    return EmailService()


@pytest.mark.asyncio
async def test_enviar_email(emailservice):
    assert (
        await emailservice.enviar_email(
            subj=subj, corpo_email=corpo_email, email_seg=email_seg
        )
        == "email enviado"
    ), "retorno deve ser email enviado"
