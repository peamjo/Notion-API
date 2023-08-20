from wiki_scraping_final import wiki_scrape_bot
import string
from import_requests import get_pages
from final_transfer import update_page, create_page, create_content
import re
from wikipedia_summary import wiki_summary
from get_images import get_images, convert_to_jpg
from face_recognition import face_recognition, majority_race_gender
from pathlib import Path

#Enter_input = input("Search: ")
def input_names(Enter_input):
    if Enter_input[:2] != "DJ":
        u_i = string.capwords(Enter_input)
    else:
        u_i = "DJ " + string.capwords(Enter_input).split(" ",1)[1]
    lists = u_i.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    name = {
        "Name": {"title": [{"text": {"content": u_i}}]},
    }
    return u_i, url, name

def get_info(data):
    info = []
    info.append([u_i])
    us_states = {'Alabama': 'AL', 'Kentucky': 'KY', 'Ohio': 'OH', 'Alaska': 'AK', 'Louisiana': 'LA', 'Oklahoma': 'OK', 'Arizona': 'AZ', 'Maine': 'ME', 'Oregon': 'OR', 'Arkansas': 'AR', 'Maryland': 'MD', 'Pennsylvania': 'PA', 'Massachusetts': 'MA', 'California': 'CA', 'Michigan': 'MI', 'Rhode Island': 'RI', 'Colorado': 'CO', 'Minnesota': 'MN', 'South Carolina': 'SC', 'Connecticut': 'CT', 'Mississippi': 'MS', 'South Dakota': 'SD', 'Delaware': 'DE', 'Missouri': 'MO', 'Tennessee': 'TN', 'Montana': 'MT', 'Texas': 'TX', 'Florida': 'FL', 'Nebraska': 'NE', 'Georgia': 'GA', 'Nevada': 'NV', 'Utah': 'UT', 'New Hampshire': 'NH', 'Vermont': 'VT', 'Hawaii': 'HI', 'New Jersey': 'NJ', 'Virginia': 'VA', 'Idaho': 'ID', 'New Mexico': 'NM', 'Virgin Islands': 'VI', 'Illinois': 'IL', 'New York': 'NY', 'Washington': 'WA', 'Indiana': 'IN', 'North Carolina': 'NC', 'West Virginia': 'WV', 'Iowa': 'IA', 'North Dakota': 'ND', 'Wisconsin': 'WI', 'Kansas': 'KS', 'Wyoming': 'WY'}
    flags_final = {'🏴󠁧󠁢󠁥󠁮󠁧󠁿': 'England','🇦🇩': 'Andorra', '🇦🇪': 'United Arab Emirates', '🇦🇫': 'Afghanistan', '🇦🇬': 'Antigua and Barbuda', '🇦🇮': 'Anguilla', '🇦🇱': 'Albania', '🇦🇲': 'Armenia', '🇦🇴': 'Angola', '🇦🇶': 'Antarctica', '🇦🇷': 'Argentina', '🇦🇸': 'American Samoa', '🇦🇹': 'Austria', '🇦🇺': 'Australia', '🇦🇼': 'Aruba', '🇦🇽': 'Åland Islands', '🇦🇿': 'Azerbaijan', '🇧🇦': 'Bosnia and Herzegovina', '🇧🇧': 'Barbados', '🇧🇩': 'Bangladesh', '🇧🇪': 'Belgium', '🇧🇫': 'Burkina Faso', '🇧🇬': 'Bulgaria', '🇧🇭':'Bahrain', '🇧🇮': 'Burundi', '🇧🇯': 'Benin', '🇧🇱': 'Saint Barthélemy', '🇧🇲': 'Bermuda', '🇧🇳': 'Brunei Darussalam', '🇧🇴': 'Bolivia', '🇧🇷': 'Brazil', '🇧🇸': 'Bahamas', '🇧🇹': 'Bhutan', '🇧🇻': 'Bouvet Island', '🇧🇼': 'Botswana', '🇧🇾': 'Belarus', '🇧🇿': 'Belize', '🇨🇦': 'Canada', '🇨🇨': 'Cocos (Keeling) Islands', '🇨🇩': 'Congo', '🇨🇫': 'Central African Republic', '🇨🇬': 'Congo', '🇨🇭': 'Switzerland', '🇨🇮': 'Ivory Coast', '🇨🇰': 'Cook Islands', '🇨🇱': 'Chile', '🇨🇲': 'Cameroon', '🇨🇳': 'China', '🇨🇴': 'Colombia', '🇨🇷': 'Costa Rica', '🇨🇺': 'Cuba', '🇨🇻': 'Cape Verde', '🇨🇼': 'Curaçao', '🇨🇽': 'Christmas Island', '🇨🇾': 'Cyprus', '🇨🇿': 'Czech Republic', '🇩🇪': 'Germany', '🇩🇯': 'Djibouti', '🇩🇰': 'Denmark', '🇩🇲': 'Dominica', '🇩🇴': 'Dominican Republic', '🇩🇿': 'Algeria', '🇪🇨': 'Ecuador', '🇪🇪': 'Estonia', '🇪🇬': 'Egypt', '🇪🇭': 'Western Sahara', '🇪🇷': 'Eritrea', '🇪🇸': 'Spain', '🇪🇹': 'Ethiopia', '🇫🇮': 'Finland', '🇫🇯': 'Fiji', '🇫🇰': 'Falkland Islands (Malvinas)', '🇫🇲': 'Micronesia', '🇫🇴': 'Faroe Islands', '🇫🇷': 'France', '🇬🇦': 'Gabon', '🇬🇧': 'United Kingdom', '🇬🇩': 'Grenada', '🇬🇪': 'Georgia', '🇬🇫': 'French Guiana', '🇬🇬': 'Guernsey', '🇬🇭': 'Ghana', '🇬🇮': 'Gibraltar', '🇬🇱': 'Greenland', '🇬🇲': 'Gambia', '🇬🇳': 'Guinea', '🇬🇵': 'Guadeloupe', '🇬🇶': 'Equatorial Guinea', '🇬🇷': 'Greece', '🇬🇸': 'South Georgia', '🇬🇹': 'Guatemala', '🇬🇺': 'Guam', '🇬🇼': 'Guinea-Bissau', '🇬🇾': 'Guyana', '🇭🇰': 'Hong Kong', '🇭🇲': 'Heard Island and Mcdonald Islands', '🇭🇳': 'Honduras', '🇭🇷': 'Croatia', '🇭🇹': 'Haiti', '🇭🇺': 'Hungary', '🇮🇩': 'Indonesia', '🇮🇪': 'Ireland', '🇮🇱': 'Israel', '🇮🇲': 'Isle of Man', '🇮🇳': 'India', '🇮🇴': 'British Indian Ocean Territory', '🇮🇶': 'Iraq', '🇮🇷': 'Iran', '🇮🇸': 'Iceland', '🇮🇹': 'Italy', '🇯🇪': 'Jersey', '🇯🇲': 'Jamaica', '🇯🇴': 'Jordan', '🇯🇵': 'Japan', '🇰🇪': 'Kenya', '🇰🇬': 'Kyrgyzstan', '🇰🇭': 'Cambodia', '🇰🇮': 'Kiribati', '🇰🇲': 'Comoros', '🇰🇳': 'Saint Kitts and Nevis', '🇰🇵': 'North Korea', '🇰🇷': 'South Korea', '🇰🇼': 'Kuwait', '🇰🇾': 'Cayman Islands', '🇰🇿': 'Kazakhstan', '🇱🇦': 'Laos', '🇱🇧': 'Lebanon', '🇱🇨': 'Saint Lucia', '🇱🇮': 'Liechtenstein', '🇱🇰': 'Sri Lanka', '🇱🇷': 'Liberia', '🇱🇸': 'Lesotho', '🇱🇹': 'Lithuania', '🇱🇺': 'Luxembourg', '🇱🇻': 'Latvia', '🇱🇾': 'Libya', '🇲🇦': 'Morocco', '🇲🇨': 'Monaco', '🇲🇩': 'Moldova', '🇲🇪': 'Montenegro', '🇲🇫': 'Saint Martin (French Part)', '🇲🇬': 'Madagascar', '🇲🇭': 'Marshall Islands', '🇲🇰': 'Macedonia', '🇲🇱': 'Mali', '🇲🇲': 'Myanmar', '🇲🇳': 'Mongolia', '🇲🇴': 'Macao', '🇲🇵': 'Northern Mariana Islands', '🇲🇶': 'Martinique', '🇲🇷': 'Mauritania', '🇲🇸': 'Montserrat', '🇲🇹': 'Malta', '🇲🇺': 'Mauritius', '🇲🇻': 'Maldives', '🇲🇼': 'Malawi', '🇲🇽': 'Mexico', '🇲🇾': 'Malaysia', '🇲🇿': 'Mozambique', '🇳🇦': 'Namibia', '🇳🇨': 'New Caledonia', '🇳🇪': 'Niger', '🇳🇫': 'Norfolk Island', '🇳🇬': 'Nigeria', '🇳🇮': 'Nicaragua', '🇳🇱': 'Netherlands', '🇳🇴': 'Norway', '🇳🇵': 'Nepal', '🇳🇷': 'Nauru', '🇳🇺': 'Niue', '🇳🇿': 'New Zealand', '🇴🇲': 'Oman', '🇵🇦': 'Panama', '🇵🇪': 'Peru', '🇵🇫': 'French Polynesia', '🇵🇬': 'Papua New Guinea', '🇵🇭': 'Philippines', '🇵🇰': 'Pakistan', '🇵🇱': 'Poland', '🇵🇲': 'Saint Pierre and Miquelon', '🇵🇳': 'Pitcairn', '🇵🇷': 'Puerto Rico', '🇵🇸': 'Palestine', '🇵🇹': 'Portugal', '🇵🇼': 'Palau', '🇵🇾': 'Paraguay', '🇶🇦': 'Qatar', '🇷🇪': 'Réunion', '🇷🇴': 'Romania', '🇷🇸': 'Serbia', '🇷🇺': 'Russia', '🇷🇼': 'Rwanda', '🇸🇦': 'Saudi Arabia', '🇸🇧': 'Solomon Islands', '🇸🇨': 'Seychelles', '🇸🇩': 'Sudan', '🇸🇪': 'Sweden', '🇸🇬': 'Singapore', '🇸🇭': 'Saint Helena', '🇸🇮': 'Slovenia', '🇸🇯': 'Svalbard and Jan Mayen', '🇸🇰': 'Slovakia', '🇸🇱': 'Sierra Leone', '🇸🇲': 'San Marino', '🇸🇳': 'Senegal', '🇸🇴': 'Somalia', '🇸🇷': 'Suriname', '🇸🇸': 'South Sudan', '🇸🇹': 'Sao Tome and Principe', '🇸🇻': 'El Salvador', '🇸🇽': 'Sint Maarten (Dutch Part)', '🇸🇾': 'Syrian Arab Republic', '🇸🇿': 'Eswatini', '🇹🇨': 'Turks and Caicos Islands', '🇹🇩': 'Chad', '🇹🇫': 'French Southern Territories', '🇹🇬': 'Togo', '🇹🇭': 'Thailand', '🇹🇯': 'Tajikistan', '🇹🇰': 'Tokelau', '🇹🇱': 'East Timor', '🇹🇲': 'Turkmenistan', '🇹🇳': 'Tunisia', '🇹🇴': 'Tonga', '🇹🇷': 'Turkey', '🇹🇹': 'Trinidad and Tobago', '🇹🇻': 'Tuvalu', '🇹🇼': 'Taiwan', '🇹🇿': 'Tanzania', '🇺🇦': 'Ukraine', '🇺🇬': 'Uganda', '🇺🇸': 'USA', '🇺🇾': 'Uruguay', '🇺🇿': 'Uzbekistan', '🇻🇦': 'Vatican City', '🇻🇨': 'Saint Vincent and The Grenadines', '🇻🇪': 'Venezuela', '🇻🇳': 'Vietnam', '🇻🇺': 'Vanuatu', '🇼🇫': 'Wallis and Futuna', '🇼🇸': 'Samoa', '🇾🇪': 'Yemen', '🇾🇹': 'Mayotte', '🇿🇦': 'South Africa', '🇿🇲': 'Zambia', '🇿🇼': 'Zimbabwe'}

    for x, i in enumerate(data):
        if i[0] == "Died":
            segment_1 = i[1].split('(', 1)
            segment_2 = segment_1[1].split(')', 1)
            death_date = segment_2[0]
            info.append(['Died', death_date])
            info.append(['YoD', death_date.split("-",1)[0]])
        if i[0] == "Born":
            segment_1 = i[1].split('(', 1)
            segment_2 = segment_1[1].split(')', 1)
            birth_date = segment_2[0]
            if (data[x+1])[0] == "Died":
                match = re.findall(r'\d', i[1])
                last_num = match[-1]
                segment_1 = i[1].split(last_num)
            else:
                segment_1 = i[1].split(')')
            location = segment_1[-1]            
            final_location = location.split(',')
            info.append(['Birthday', birth_date])
            info.append(['YoB', birth_date.split("-",1)[0]])
            if len(final_location) > 3:
                final_location.pop(0)
            if len(final_location) == 3:
                city = final_location[0]
                state = final_location[1].replace(' ','',1)
                country = final_location[2].replace(' ','',1)
                info.append(['City', city])
                info.append(['State', state])
                info.append(['Country', country])
            elif len(final_location) > 1 and len(final_location) < 3:
                city = final_location[0]
                if city == "New York City":
                    city = "NYC"
                country = final_location[1].replace(' ','',1)
                if country == "Empire of Japan":
                    country = "Japan"
            #   if country == "French Algeria":
            #       country = "'France', 'Algeria'"
                info.append(['City', city])
                info.append(['Country', country])
            if len(info)>1:
                if (info[-1])[1] == 'U.S.' or (info[-1])[1] == 'US' or (info[-1])[1] == 'United States':
                    (info[-1])[1] = 'USA'
                    if len(final_location)>2:
                        for key in us_states:                    
                            if key == state:
                                (info[-2])[1] = us_states[key]
                for key in flags_final:
                    if flags_final[key] == (info[-1])[1]:
                        info.append(['Flag', key])
        if i[0] == "Occupations" or i[0] == 'Occupation' or i[0] == "Occupation(s)":
            info.append(['Occupations', i[1]])
        if i[0] == "Genres":
            info.append(['Genres', i[1]])
        if i[0] == "Instruments" or i[0] == "Instrument(s)":
            info.append(['Instruments', i[1]])
        if i[0] == "Movement":
            info.append(['Art Style/Movement', i[1]])
        if i[0] == "Years active" or i[0] == "Turned pro":
            i[1]=i[1].replace("–"," to ")
            i[1]=i[1].replace("-"," to ")
            info.append(['Years active', i[1]])
        if i[0] == "Retired":
            info.append(['Retired', i[1]])
    info.append(['Wiki', url])
    return(info)

def add_or_check_jobs(info, job):
    counter = 0
    for i in info:
        if i[0] == "Occupations":
            for x in job:
                if x not in i[1]: 
                    i[1].append(x)
            break
        else: counter+=1
    if counter == len(info):
        info.append(['Occupations', job])
        

def edit_data(ip):
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        #date = props["Date"]["date"]["start"]
        if name == ip:
            for x,i in enumerate(info):
                if i[0] == 'Birthday':
                    update_data = {"Date": {"date": {"start": i[1]}}}
                    update_page(page_id, update_data)
                    birth = i[1]
                if i[0] == 'Died':
                    update_data = {"Date": {"date": {"start": birth, "end": i[1]}}}
                    update_page(page_id, update_data)
                if i[0] == 'YoB':
                    update_data = {"YoB": {"number": int(i[1])}}
                    update_page(page_id, update_data)
                if i[0] == 'YoD':
                    update_data = {"YoD": {"number": int(i[1])}}
                    update_page(page_id, update_data)
                if i[0] == 'Years active':
                    update_data = {"Years active": {"rich_text": [{"text": {"content": i[1]}}]}}
                    update_page(page_id, update_data)
                if i[0] == 'Country':
                    update_data = {"Country": {"multi_select": [{"name": i[1]}]}}
                    update_page(page_id, update_data)
                if i[0] == 'City':
                    update_data = {"City/Region": {"multi_select": [{"name": i[1]}]}}
                    update_page(page_id, update_data)
                    city = i[1]
                if i[0] == 'State':
                    update_data = {"City/Region": {"multi_select": [{"name": city}, {"name": i[1]}]}}
                    update_page(page_id, update_data)
                if i[0] == 'Gender':
                    update_data = {"Gender": {"select": {"name": i[1]}}}
                    update_page(page_id, update_data)
                if i[0] == 'Ethnicity':
                    update_data = {"Ethnicity": {"multi_select": [{"name": i[1]}]}}
                    update_page(page_id, update_data)
                if i[0] == 'Flag':
                    update_data = {"emoji": i[1]}
                    update_page(page_id, update_data)
                if i[0] == 'Occupations':
                    jobs = []
                    for j in i[1]:
                        j = {"name": j}
                        jobs.append(j)
                    update_data = {"Job(s)": {"multi_select": jobs}}
                    update_page(page_id, update_data)
                if i[0] == 'Wiki':
                    update_data = {"Wiki": {"url": i[1]}}
                    update_page(page_id, update_data)
                if i[0] == 'Genres':
                    genres = []
                    for j in i[1]:
                        j = {"name": j}
                        genres.append(j)
                    update_data = {"Genres (Music)": {"multi_select": genres}}
                    update_page(page_id, update_data)
                if i[0] == 'Instruments':
                    instruments = []
                    for j in i[1]:
                        j = {"name": j}
                        instruments.append(j)
                    update_data = {"Instrument(s)": {"multi_select": instruments}}
                    update_page(page_id, update_data)
                if i[0] == 'Art Style/Movement':
                    movement = []
                    for j in i[1]:
                        j = {"name": j}
                        movement.append(j)
                    update_data = {"Art Style/Movement": {"multi_select": movement}}
                    update_page(page_id, update_data)
            update_data = wiki_summary(name)
            create_content(page_id, update_data)

people_list = []
job = []
error_list = []

for people in people_list:
    try:
        u_i, url, name = input_names(people)
        data = wiki_scrape_bot(url)
        print(data)
        info = get_info(data)
        if job != []:
            add_or_check_jobs(info, job)
        get_images(people)
        convert_to_jpg(people)
        gender_list = []
        ethnicity_list = []
        for x in range(1,6):
            link = str(Path.cwd().joinpath('download',rf'{people} face',rf'Image_{x}.jpg'))
            gender_count, ethnicity_count = face_recognition(link)
            gender_list.append(gender_count)
            ethnicity_list.append(ethnicity_count)
        print(gender_list, ethnicity_list)
        gender, ethnicity = majority_race_gender(gender_list, ethnicity_list)
        info.append(["Gender", gender])
        info.append(["Ethnicity", ethnicity])
        print(info)
        pages = get_pages()
        exist = False
        for page in pages:
            og_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            if og_name == u_i:
                exist = True
        if exist == False:
            create_page(name)
            pages = get_pages()
        edit_data((info[0])[0])
    except KeyboardInterrupt:
        break
    except:
        error_list.append(people)
        continue
print("Error List:", error_list)
