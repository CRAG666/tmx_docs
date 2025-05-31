from fastapi import HTTPException, status
from typing import Dict, Any, Optional


class CustomException(HTTPException):
    """
    Excepción personalizada para manejar errores de la API

    Atributos:
        status_code: Código HTTP de estado
        message: Mensaje descriptivo del error
        details: Detalles adicionales del error (opcional)
    """

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Se produjo un error inesperado",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(status_code=status_code, detail=message)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la excepción a un diccionario para la respuesta JSON"""
        error_dict = {"status_code": self.status_code, "message": self.message}

        if self.details:
            error_dict["details"] = self.details

        return error_dict


# Excepciones comunes predefinidas
def not_found_exception(resource: str, id: Any) -> CustomException:
    """Crea una excepción para recursos no encontrados"""
    return CustomException(
        status_code=status.HTTP_404_NOT_FOUND,
        message=f"{resource} con id {id} no encontrado",
    )


def bad_request_exception(
    message: str = "Solicitud incorrecta", details: Optional[Dict[str, Any]] = None
) -> CustomException:
    """Crea una excepción para solicitudes incorrectas"""
    return CustomException(
        status_code=status.HTTP_400_BAD_REQUEST, message=message, details=details
    )


def validation_exception(errors: Dict[str, Any]) -> CustomException:
    """Crea una excepción para errores de validación"""
    return CustomException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Error de validación en los datos de entrada",
        details={"validation_errors": errors},
    )


def unauthorized_exception(message: str = "No autorizado") -> CustomException:
    """Crea una excepción para accesos no autorizados"""
    return CustomException(status_code=status.HTTP_401_UNAUTHORIZED, message=message)


def forbidden_exception(message: str = "Acceso prohibido") -> CustomException:
    """Crea una excepción para accesos prohibidos"""
    return CustomException(status_code=status.HTTP_403_FORBIDDEN, message=message)
