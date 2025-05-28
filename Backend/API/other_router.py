from fastapi import APIRouter
import Tools.DBConnection as db

router = APIRouter()

@router.get("/departments", summary="Get all departments")
def get_departments():
    """
    Retrieve a list of all departments.
    """
    return db.get_all_departments()