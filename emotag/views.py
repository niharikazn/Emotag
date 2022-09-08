from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Emotag
from .models import testimonial
import random
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def quote(word):
    d = {"neutral":["The hottest place in Hell is reserved for those who remain neutral in times of great moral conflict.",
          "People who demand neutrality in any situation are usually not neutral but in favor of the status quo",
          "Be it high or low, it doesn't matter. I need to stay calm and neutral all the time.",
          "Washing one's hands of the conflict between the powerful and the powerless means to side with the powerful, not to be neutral. ",
          "Armed neutrality makes it much easier to detect hypocrisy.",
          "I don't represent anyone's opinion. Not even my own. I'm neutral.",
          "Impartiality is a pompous name for indifference, which is an elegant name for ignorance.",
          "Nor must we always be neutral where our neighbors are concerned: for tho' meddling is a fault, helping is a duty",
          "If you are neutral in situations of injustice, you have chosen the side of the oppressor. If an elephant has its foot on the tail of a mouse and you say that you are neutral, the mouse will not appreciate your neutrality.",
          "Take sides. Neutrality helps the oppressor, never the victim.",
          "With a great moral issue involved, neutrality does not serve righteousness; for to be neutral between right and wrong is to serve wrong."],
         "sad":["I’m sad but I Smile.That’s my life." , "Silence is the most powerful scream." , "Being ignored worst feeling ever." , "i get lost inside my mind" , "You broke me again." , "I act like i don’t care but deep inside it hurts." , "I am only good at hiding my feeling." , "When you sit alone.. you sit with your past.."]
,
         "happy":["Smiling is definitely one of the best beauty remedies." , "Smile, smile, smile at your mind as often as possible." , "Your smiling will considerably reduce your mind’s tearing tension." ," Let us always meet each other with smile, for the smile is the beginning of love." , "Let us always meet each other with smile, for the smile is the beginning of love." , "Just for today, smile a little more." , "If you see someone without a smile give them one of yours." , "Smile is the beauty of the soul." , "A smiling face is a beautiful face. A smiling heart is a happy heart." , "A smile is an inexpensive way to change your looks." , "Keep calm and carry on smiling." ,"Smile, it is the key that fits the lock of everybody’s heart."],
         "fear":["Fear doesn't shut you down; it wakes you up" , "Fear cuts deeper than swords." , "Fear of a name increases fear of the thing itself." , "Have no fear of perfection - you'll never reach it." , "Scared is what you're feeling. Brave is what you're doing." , "Do not be afraid; our fate Cannot be taken from us; it is a gift." , "Don't give in to your fears. If you do, you won't be able to talk to your heart." , "Fear is a phoenix. You can watch it burn a thousand times and still it will return." , "The only thing we have to fear is fear itself." , "Without fear there cannot be courage." , "Keep your fears to yourself, but share your courage with others." , "Find out what you're afraid of and go live there." , "In time we hate that which we often fear."],
         "surprise":["Surprise is the greatest gift which life can grant us." , "Don't tell people how to do things, tell them what to do and let them surprise you with their results." , "The moments of happiness we enjoy take us by surprise." , "Life is so full of unpredictable beauty and strange surprises." , "There is power in surprising people with results" , "Surprise keeps the reader awake." , "Art must take reality by surprise." , "Mystery is at the heart of creativity. That, and surprise."],
         "angry":["When angry count to ten before you speak. If very angry, count to one hundred." ,"When angry count to ten before you speak. If very angry, count to one hundred." , "Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy." ,"Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy.","Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy.", "For every minute you remain angry, you give up sixty seconds of peace of mind." , "Speak when you are angry - and you'll make the best speech you'll ever regret." , "Whatever is begun in anger ends in shame." , "The greatest remedy for anger is delay." , "Do not let your anger lead to hatred, as you will hurt yourself more than you would the other."],
         "disgust":["Love is disgusting when you no longer possess yourself." , "Selfies are disgusting.",
"Love is disgusting when you no longer possess yourself." , "Selfies are disgusting.",
"Love is disgusting when you no longer possess yourself." , "Selfies are disgusting.",
"Love is disgusting when you no longer possess yourself." , "Selfies are disgusting.",
"Love is disgusting when you no longer possess yourself." , "Selfies are disgusting."]
         }
    x=random.randrange(0,10)
    return d[word][x]
def start(request):
    result=outdata()
    text=""
    k=list(result["chart"].values())
    if result["result"].upper()=="NO FACE IDENTIFIED":
        text="NO FACE IDENTIFIED"
    else:
        text=quote(result["result"])
    res={"result":result["result"].upper(),
         "data":k,
         "voice":text}
    print(result)
    return render(request, "start.html",res)
def check(request):
  mymembers = Emotag.objects.all().values()
  output = ""
  for x in mymembers:
    output += x["firstname"]
  return HttpResponse(output)

def outdata():
    import cv2
    from deepface import DeepFace
    import numpy as np
    face_cascade_name = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
    face_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
        print("Error loading xml file")

    video = cv2.VideoCapture(0)
    niha = 0
    l = []
    while video.isOpened():
        _, frame = video.read()
        niha += 1
        respo={}
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in face:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            try:
                analyze = DeepFace.analyze(frame, actions=['emotion'])
                l.append(analyze['dominant_emotion'])
            except:
                print()
            cv2.imshow('video', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        if niha == 50:
            s =['sad','fear','happy','neutral','angry','surprise','disgust']
            ele = ""
            d={}
            for i in s:
                d[i]=l.count(i)
            ele = max(zip(d.values(), d.keys()))[1]
            if ele == "" or d[ele]==0:
                respo["result"]="No face Identified"
            else:
                respo["result"]=ele
            respo["chart"] =d
            return respo
    video.release()