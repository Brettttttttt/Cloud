"""
Middleware for exception handling and request logging
"""
import logging
import time
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


async def log_requests_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to log all incoming requests and responses.
    
    Args:
        request: Incoming request
        call_next: Next middleware or route handler
    
    Returns:
        Response from the handler
    """
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"Incoming request: {request.method} {request.url.path} "
        f"- Client: {request.client.host if request.client else 'unknown'}"
    )
    
    # Process request
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Completed request: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        
        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} "
            f"- Error: {str(e)} - Time: {process_time:.3f}s",
            exc_info=True
        )
        raise


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions (404, 405, etc.)
    
    Args:
        request: Incoming request
        exc: HTTP exception
    
    Returns:
        JSON response with error details
    """
    logger.warning(
        f"HTTP {exc.status_code} error on {request.method} {request.url.path}: {exc.detail}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "status_code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url.path)
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation errors (422)
    
    Args:
        request: Incoming request
        exc: Validation exception
    
    Returns:
        JSON response with validation error details
    """
    errors = exc.errors()
    
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {errors}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
                "path": str(request.url.path),
                "details": errors
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all uncaught exceptions (500)
    
    Args:
        request: Incoming request
        exc: Any unhandled exception
    
    Returns:
        JSON response with error details
    """
    # Check if it's a database error
    if isinstance(exc, SQLAlchemyError):
        logger.error(
            f"Database error on {request.method} {request.url.path}: {str(exc)}",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": {
                    "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
                    "message": "Database service unavailable",
                    "path": str(request.url.path)
                }
            }
        )
    
    # Generic server error
    logger.error(
        f"Internal server error on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error",
                "path": str(request.url.path),
                "detail": str(exc) if logger.level == logging.DEBUG else "An unexpected error occurred"
            }
        }
    )
