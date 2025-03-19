from fastapi import APIRouter, Depends

from domain.auth.dto.request import AuthSignUpRequest
from domain.auth.service.auth import AuthService
from domain.common.dto.response.api_response import APIResponse

