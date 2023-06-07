from .. import modules, schemas, oauth2
from fastapi import Depends, FastAPI , Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
(oauth2.get_current_user)):

    post = db.query(modules.Post).filter(modules.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(modules.Vote).filter(modules.Vote.post_id == vote.post_id, modules.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} haz alredy voted on post {vote.post_id}")
        new_vote = modules.Vote(post_id =vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}


        