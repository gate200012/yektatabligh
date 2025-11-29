from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.models.models import Category
from app.schemas.common import CategoryCreate, CategoryRead
from app.utils.deps import get_db, require_role

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(db=Depends(get_db)):
    return db.exec(select(Category)).all()


@router.post("", response_model=CategoryRead, dependencies=[Depends(require_role("admin", "analyst"))])
def create_category(category_in: CategoryCreate, db=Depends(get_db), user=Depends(require_role("admin", "analyst"))):
    category = Category(**category_in.dict(), created_by=user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryRead, dependencies=[Depends(require_role("admin", "analyst"))])
def update_category(category_id: int, category_in: CategoryCreate, db=Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for k, v in category_in.dict().items():
        setattr(category, k, v)
    db.commit()
    db.refresh(category)
    return category
