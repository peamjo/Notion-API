from deepface import DeepFace
from collections import Counter

def face_recognition(image_path):
    objs = DeepFace.analyze(img_path = image_path, actions = ['gender', 'race'], enforce_detection = False
    )

    if objs[0]["dominant_gender"] == "Woman":
        gender = "Female"
    else:
        gender = "Male"

    if (objs[0]["dominant_race"]).capitalize() == "Indian":
        ethnicity = "South Asian"
    elif (objs[0]["dominant_race"]).capitalize() == "Latino hispanic":
        ethnicity = "Latinx"
    elif (objs[0]["dominant_race"]).capitalize() == "Middle eastern":
        ethnicity = "Arab"
    else:
        ethnicity = (objs[0]["dominant_race"]).capitalize() 

    return(gender, ethnicity)

def majority_race_gender(gender_list = [], ethnicity_list = []):
    gender_list = Counter(gender_list)
    ethnicity_list = Counter(ethnicity_list)
    gender = gender_list.most_common()[0][0]
    ethnicity = ethnicity_list.most_common()[0][0]
    print(gender, ethnicity)
    return (gender, ethnicity)
