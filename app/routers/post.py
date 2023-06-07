from .. import modules, schemas, oauth2
from fastapi import Depends, FastAPI , Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    print(limit)

    # posts = db.query(modules.Post).filter(modules.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(modules.Post, func.count(modules.Vote.post_id).label("votes")).join(modules.Vote, modules.Vote.post_id== modules.Post.id, isouter=True).group_by(modules.Post.id).filter(modules.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
        


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ ,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = modules.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # post =db.query(modules.Post).filter(modules.Post.id == id).first()

    post = db.query(modules.Post, func.count(modules.Vote.post_id).label("votes")).join(modules.Vote, modules.Vote.post_id == modules.Post.id, isouter=True).group_by(modules.Post.id).filter(modules.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to preform requested action")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(modules.Post).filter(modules.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to preform requested action")


    
    post_query.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(modules.Post).filter(modules.Post.id == id)

    post = post_query.first()
    
       
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to preform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    
    return post_query.first()