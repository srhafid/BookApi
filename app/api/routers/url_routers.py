from fastapi import APIRouter, HTTPException
from app.api.controllers.controller_url import UrlsController

router = APIRouter()
controller = UrlsController()  # Initialize the controller with appropriate dependencies


@router.post("/urls/")
def create_url(url_data: dict):
    try:
        url = controller.create_url(url_data)
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/urls/{url_id}")
def read_url(url_id: int):
    try:
        url = controller.read_url(url_id)
        return url
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/urls/{url_id}")
def update_url(url_id: int, url_data: dict):
    try:
        updated = controller.update_url(url_id, url_data)
        if updated:
            return {"message": "URL updated successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/urls/{url_id}")
def delete_url(url_id: int):
    try:
        deleted = controller.delete_url(url_id)
        if deleted:
            return {"message": "URL deleted successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
