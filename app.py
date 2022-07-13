from website import createApp
from website.training import trainingImages
app=createApp()

if __name__=='__main__':
    # training start
    trainingImages()
    # project start
    app.run(debug=True)