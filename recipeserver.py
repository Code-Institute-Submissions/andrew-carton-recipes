from recipemain import *

os.environ["PORT"] = "8080"
app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT')))
