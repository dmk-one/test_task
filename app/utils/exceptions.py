from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    def __init__(self, detail="Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestError(HTTPException):
    def __init__(self, detail="Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
