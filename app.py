from website import createApp
from website.training import trainingImages
app=createApp()

if __name__=='__main__':
    trainingImages()
    app.run(debug=True)