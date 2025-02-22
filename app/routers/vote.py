from .. import models, schemas, utils, oauth2
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = db.get(models.Post, vote.post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist",
        )

    found_vote = db.get(
        models.Votes, {"post_id": vote.post_id, "user_id": current_user}
    )
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user} has already voted on post {vote.post_id}",
            )

        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        db.delete(found_vote)
        db.commit()
        return {"message": "Successfully deleted vote"}
