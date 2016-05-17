import soundcloud
import urllib.request
import json
import requests
import time

clientID = "346e7346df6130458107f64f76ccbe88"
client = soundcloud.Client(client_id=clientID)
api_base = "https://api.soundcloud.com"


def get_user_info(username):
    user = client.get('/resolve', url='http://soundcloud.com/{}/'.format(username))
    user_info = urllib.request.urlopen("{}/users/{}.json?consumer_key={}".format(api_base, user.id, clientID)).read()
    user_info_data = json.loads(user_info.decode())
    number_of_likes = user_info_data['public_favorites_count']
    username = user_info_data['username']
    return username, number_of_likes, user


user_information = get_user_info("hypertextmike")
user_name = user_information[0]
number_of_user_likes = user_information[1]
userID = user_information[2]

csv_file = open("{}-like-list.csv".format(user_name), "w", encoding='UTF-8')
csv_file.write("Track Title, Track URL\n")  # Writes headers to CSV file

number = 1
page_size = 50
tracks = client.get("/users/{}/favorites".format(userID.id), limit=page_size, linked_partitioning=1)
for track in tracks.collection:
    track_title = track.title.replace(",", "")  # Removes commas as causes issues with .csv files
    csv_file.write("{},{}\n".format(track_title, track.permalink_url))
    print("{} of {} ({}%)".format(number, number_of_user_likes,
        round(float(100 / number_of_user_likes * number), 2)))

    number += 1

while hasattr(tracks, 'next_href'):
    tracks = client.get(tracks.next_href)
    for track in tracks.collection:
        track_title = track.title.replace(",", "")  # Removes commas as causes issues with .csv files
        csv_file.write("{},{}\n".format(track_title, track.permalink_url))
        print("{} of {} ({}%)".format(number, number_of_user_likes,
            round(float(100 / number_of_user_likes * number), 2)))

        number += 1

#tracks = client.get('/tracks', order='created_at', limit=page_size, linked_partitioning=1)

#offset_number = 0
#while offset_number < number_of_user_likes:
#    try:
#        track_fetch = urllib.request.urlopen(
#            "{}/users/{}/favorites.json?client_id={}&offset={}&limit30".format(api_base, userID.id,
#                                                                              clientID, offset_number)).read()
#        track_data = json.loads(track_fetch.decode())
#        for track in track_data:
#
#        offset_number += 30
#        time.sleep(5)
#    except IndexError:
#        print("There is an issue with Soundcloud, please try again")
#    except requests.HTTPError:
#        print("There is an issue with Soundcloud, please try again")
#    except requests.ConnectionError:
##        print("Check your internet connection")
