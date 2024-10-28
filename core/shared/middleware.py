from datetime import datetime
from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from core.auth.models import User
from core.shared.auth import verify_token

EXEMPTED_PATHS = [
    "/api/docs",
    "/api/openapi.json",
    "/api/auth/signup/",
    "/api/auth/login/"
]

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        Initializes the JWTBearer class.

        Args:
            auto_error (bool): Whether to automatically raise an HTTPException for unauthorized requests.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Handles the HTTP request by verifying the JWT token.

        Args:
            request (Request): The incoming request object.

        Returns:
            str: The JWT token if valid.

        Raises:
            HTTPException: If the token is invalid or expired, or if the authorization code is missing.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            user = await self.authenticate(payload)
            request.state.user = user
            return credentials.credentials
        
        raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> Optional[dict]:
        """
        Verifies the JWT token and decodes the payload.

        Args:
            jwtoken (str): The JWT token to verify.

        Returns:
            Optional[dict]: The decoded token payload if valid, otherwise None.
        """
        try:
            return verify_token(jwtoken)
        except JWTError:
            return None

    async def authenticate(self, payload: dict) -> Optional[User]:
        """
        Authenticates the user based on the decoded token payload.

        Args:
            payload (dict): The decoded token payload.

        Returns:
            Optional[User]: The authenticated User object if valid, otherwise raises HTTPException.

        Raises:
            HTTPException: If the token is expired, or if the user is not found or invalid.
        """
        exp = payload.get("exp")
        if exp and exp <= datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=403, detail="Token is expired."
            )
        
        username = payload.get("sub")
        if username:
            user = await User.get_or_none(username=username)
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid token."
                )
        
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
