from app.crud.crud_bekpack.crud_bekpackuser import bekpackuser
from app.models.bekpack import BekpackUser
from app.models.user import User
from fastapi import Depends, HTTPException, status

from app.api import deps
import sqlalchemy
from sqlalchemy.orm import Session


def get_bekpack_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> BekpackUser:
    try:
        return bekpackuser.get_by_owner(db=db, owner_id=current_user.id)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=403, detail="User not registered for BekPack")
