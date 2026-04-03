from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Сначала получаем стандартный ответ DRF
    response = exception_handler(exc, context)

    if response is not None:
        # Добавляем свой формат
        customized_response = {
            "success": False,
            "status_code": response.status_code,
            "error": response.data  # стандартное сообщение
        }
        return Response(customized_response, status=response.status_code)

    # Если DRF ничего не вернул (например, необработанное исключение)
    return Response({
        "success": False,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "error": "Internal server error"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)