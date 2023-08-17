from deepface import DeepFace

def face_recognition(image_path):
    objs = DeepFace.analyze(img_path = image_path, actions = ['gender', 'race']
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

    final_list = [["Gender:", gender],["Ethnicity:", ethnicity]]

    print(objs)
    print(final_list)

    return(final_list)
