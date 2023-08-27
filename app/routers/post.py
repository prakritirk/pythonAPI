from fastapi import FastAPI , Response, status , HTTPException , Depends, APIRouter
from .. import models,schemas, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session 
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", 
    tags= ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/")
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    print(limit)
    # cursor.execute("""Select * FROM posts""")
    # posts = cursor.fetchall()
    #  print(current_user.id)
    #  posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(""" Insert into posts (title, content, published) values (%s, %s, %s) RETURNING * """, 
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return  new_post

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, response: Response , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post=db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute("""Select * from posts where id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found" )
    
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""Delete from posts where id = %s Returning * """, (str(id),))
    # conn.commit()
    # deleted_post= cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int, updated_post:schemas.PostCreate ,db: Session = Depends(get_db), response_model =schemas.Post, current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # cursor.execute(""" Update posts set title = %s, content = %s, published = %s where id = %s Returning *""", 
    #                 (post.title, post.content, post.published, str(id)) )
    # conn.commit()
    # updated_post = cursor.fetchone()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id {id} does not exist')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested")
    post_query.update({'title': 'this is updated tile', 'content':'updated content'}, synchronize_session = False)
    db.commit()
    
    return {'data': post_query.first()}