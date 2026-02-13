import uvicorn
from fastapi import FastAPI
from app.routers import main_router
#from app.routers import main_router2
#from app.routers import main_router3
app = FastAPI()
app.include_router(main_router)

#app2 = FastAPI()
#app2.include_router(main_router2)

#app3 = FastAPI()
#app3.include_router(main_router3)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
