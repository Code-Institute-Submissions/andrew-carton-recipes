from recipemain import *

if "PORT" not in os.environ:
    os.environ["PORT"] = "8000"
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT')))
