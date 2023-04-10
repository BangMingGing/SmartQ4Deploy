from fastapi import APIRouter, Response, Request
from fastapi.templating import Jinja2Templates
from smartQ import token, database
from smartQ.hashing import Hash
from fastapi.responses import RedirectResponse

router = APIRouter(tags=['Authentication'])

templates = Jinja2Templates(directory="frontend")

# Get Home Pages
@router.get("/")
async def tologin(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/login.html", context)

@router.get("/menu")
async def menu(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/menu.html", context)

@router.post('/')
async def login(request: Request, response: Response):
    form = await request.form()
    user_email = form.get("user_id")
    print(user_email)
    password = form.get("password")
    
    errors = []
    if not user_email:
        errors.append("Please Enter Email")
    if not password:
        errors.append("Please Enter Password ")
    
    try:
        user = database.get_user(user_email)
        if not user:
            errors.append("Email does not exists")
            return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
        else:
            if not Hash.verify(user["password"], password):
                errors.append("Invalid Password")
                return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
            else:
                msg = "Login Successful"
                print(msg)
                access_token = token.create_access_token(data={"sub": user["email"]})
                response = templates.TemplateResponse("/login.html", {"request": request, "msg": msg})
                response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
                return response
    except:
        errors.append("Something Wrong")
        return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
