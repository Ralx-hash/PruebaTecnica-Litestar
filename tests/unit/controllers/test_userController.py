import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.schemas import UsuarioLogin
from src.controllers.userController import userController
from src.database.models import Users
from litestar.exceptions import HTTPException


@pytest.mark.asyncio
async def test_login_email_no_existe():
    
    # PREPARAR 
    login_data = UsuarioLogin(
        email="noexiste@example.com",
        password="cualquierPassword"
    )
    
    mock_user_repo = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None  # Usuario no encontrado
    
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_user_repo.session = mock_session

    #Cuando await session.execute(...) se ejecuta, retorna mock_result
    #Y mock_result.scalars() retorna mock_scalars
    #Y mock_scalars.first() retorna None

    # EJECUTAR 
    controller = userController.__new__(userController)
    login_handler = userController.login
    login_function = login_handler.fn
    
    # VERIFICAR
    with pytest.raises(HTTPException) as exc_info:
        await login_function(controller, login_data, mock_user_repo)
    
    assert exc_info.value.status_code == 401
    assert "Email no encontrado" in str(exc_info.value.detail)
    # Verificar que se llamó a execute
    mock_session.execute.assert_called_once()

