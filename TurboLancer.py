# romE2I69nPailBx4S8agYb09En3XPhhVJXnE74qChVS sandbox api
# set CLOUDINARY_URL=cloudinary://489474321839884:82k4ZB3pAQWVtZSzfdHHLMpo0QM@dfew09nzc
# romE2I69nPailBx4S8agYb09En3XPhhVJXnE74qChVS sandbox api
import os
import re
import io
import uuid
import json
import random
import datetime as dt
import threading
import time
from datetime import datetime, timedelta
from urllib.parse import unquote
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    jsonify,
    send_file,
    render_template_string,
    abort,
)
from flask_wtf import FlaskForm
from wtforms import FileField
from pymongo import MongoClient
from bson.objectid import ObjectId
import turbolancer_data_Security
import TurboLancer_RePhrase_text
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from werkzeug.datastructures import ImmutableMultiDict
import uploade_video as uv
from jinja2 import Environment, FileSystemLoader
import pytz
from base64 import b64decode
TurboLancer = Flask(__name__, template_folder="template", static_folder="static")
TurboLancer.config["SECRET_KEY"] = os.urandom(24)
socketio = SocketIO(TurboLancer)
env = Environment(loader=FileSystemLoader("template"))

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://junaidiqbal:allahsadaro@junaid.lkpmjko.mongodb.net/?retryWrites=true&w=majority"
)
db = client["Tasker"]
key = b'||/:?"(:@junaid)'
chat = client["chat"]
# Set collection names
chatroom_collection = chat["chatroom"]
chatImages_collection = chat["images"]
seller_collection = db["Sellers"]
user_collection = db["users"]
serving_sectors_collection = db["serving_sectors"]
sectors_technologies_collection = db["technologies"]
chat_rooms = db["chatrooms"]
question_collection = db["questions"]
image_collection = db["images"]
catalogue_collection = db["catalogue"]
draft_catalogue_collection = db["draft_catalogue"]
slideshow_collection = db["slideshow"]
chatFiles_collection = chat['chatFiles']

def generate_id():
    return str(uuid.uuid4())

def new_or_not(date_str):
   date = datetime.strptime(date_str, "%d/%m/%y")
   days_diff = (datetime.now() - date).days
   if days_diff <= 5:
       return True
   else:
       return False

def getkey(data):
    keys_to_find = ["ideo", "emalo", "deno"]
    found_items = {key: data.get(key) for key in keys_to_find if key in data}
    return found_items



def check(data, file):
    try:
        compound = {key: data.get(key) for key in ["ideo", "emalo", "deno"] if key in data}
        if not compound:
            return None

        if "ideo" not in compound:
            return None

        user_id = turbolancer_data_Security.decrypt(key, compound.get("ideo"))
        if not user_id:
            return None

        user = seller_collection.find_one({"_id": user_id}) or user_collection.find_one({"_id": user_id})
        if not user:
            return None

        user_email = user.get("email")
        if not user_email or user_email != compound.get("emalo"):
            return None

        if user.get("d") == "d" and not compound.get("deno"):
            return None
        elif user.get("d") == "d" and compound.get("deno"):
            return file
        elif user.get("d") == "c":
            return file

        return None
    except Exception as e:
        print(f"An error occurred in check function: {e}")
        return None

def remove_word_without_space(text, word):
    pattern = rf"\b{word}(?!\s)"
    return re.sub(pattern, "", text)


def remove_first_uppercase(s):
    if len(s) >= 2 and s[:2].isupper():
        return s[1:]
    return s

def update_database(collection, ideo, encoded_email, data):
    for field in ["bir", "gan", "name", "about_self", "sk"]:
        if field == "sk" and data.get(field):
            arr = data["sk"].split(",")
            print(arr)
            arr = split_into_child_arrays(
                arr
            ) 
            print(arr)

            ud = seller_collection.find_one({"_id": ideo, "email": encoded_email})
            print(ud)
            if ud and "sk" in ud:
                main_arr = ud["sk"]
                print(main_arr)
                for x in range(len(arr)):
                    found = False
                    for y in range(len(main_arr)):
                        if main_arr[y][0] == arr[x][0]:
                            main_arr[y] = arr[x]
                            found = True
                            break
                    if not found:
                        main_arr.append(arr[x])
                print(main_arr)

                seller_collection.update_one(
                    {"_id": ideo, "email": encoded_email}, {"$set": {"sk": main_arr}}
                )
        elif data.get(field):
            collection.update_one(
                {"_id": ideo, "email": encoded_email}, {"$set": {field: data[field]}}
            )


def delete_image(image_id):
    image_id = image_id.split("/")[-1]
    print('this is from: '+image_id)
    filter = {"_id": ObjectId(image_id)}

    delete_result = slideshow_collection.delete_one(filter) or ''
    print(delete_result)
    if delete_result:
            print(f"Image with ID {image_id} deleted successfully.")
    else:
            print(f"No image found with ID {image_id}.")
    

def get_user_dataA(user_id):
    user_data = user_collection.find_one({"_id": user_id})
    if user_data:
        email = turbolancer_data_Security.decrypt(key, user_data["email"])
        image = user_data["image"]
        name = user_data["name"]
        country = turbolancer_data_Security.decrypt(key, user_data["country"])
        ph = turbolancer_data_Security.decrypt(key, user_data["phone_number"])
        year = user_data["account_created_in"]
        method = user_data["payment_method"]
        bir = turbolancer_data_Security.decrypt(key, user_data["bir"])
        gan = turbolancer_data_Security.decrypt(key, user_data.get("gan", None)) or None
        tag = user_data["tag"] or None

        return {
            'dd':user_id,
            "name": name,
            "image": image,
            "email": email,
            "country": country,
            "ph": ph,
            "year": year,
            "bir": bir,
            "tag": tag,
            "gan": gan,
        }

    return None


def get_seller_data(developer_id):
    developer_data = seller_collection.find_one({"_id": developer_id})
    if developer_data:
        email = turbolancer_data_Security.decrypt(key, developer_data["email"])
        image = developer_data["image"]
        name = developer_data["name"]
        country = turbolancer_data_Security.decrypt(key, developer_data["country"])
        ph = turbolancer_data_Security.decrypt(key, developer_data["phone_number"])
        year = developer_data["account_created_in"]
        method = developer_data["payment_method"]
        grade = developer_data["grade"]
        rating = developer_data["rating"]
        about_self = developer_data["about_self"]
        tag = developer_data["tag"] or None
        sk = developer_data["sk"] or None
        earnings = developer_data["earnings"] or None
        bir = turbolancer_data_Security.decrypt(key, developer_data["bir"]) or None
        gan = (
            turbolancer_data_Security.decrypt(key, developer_data.get("gan", None))
            or None
        )
        length = len(sk) if sk else 0
        return {
            'dd':developer_id,
            "name": name,
            "image": image,
            "email": email,
            "country": country,
            "ph": ph,
            "year": year,
            "about_self": about_self,
            "rating": rating,
            "grade": grade,
            "tag": tag,
            "bir": bir,
            "gan": gan,
            "sk": sk,
            "earnings": earnings,
            "len": length,
        }
    return None
def upload_image_local(image_data, encoded_email, ideo):
    collection = seller_collection.find_one(
        {"_id": ideo, "email": encoded_email}
    ) or user_collection.find_one({"_id": ideo, "email": encoded_email})
    if "image" in collection:
        previous_image_link = collection["image"]
        if previous_image_link != "":
            previous_image_id = previous_image_link.split("/")[-1]
            image_collection.delete_one({"_id": ObjectId(previous_image_id)})
    image_id = image_collection.insert_one(
        {"data": image_data, "reference": ideo}
    ).inserted_id

    # Update the 'image' field in the TurboLancerropriate collection
    if seller_collection.find_one({"_id": ideo, "email": encoded_email}):
        seller_collection.update_one(
            {"_id": ideo, "email": encoded_email},
            {"$set": {"image": "/get_image/" + str(image_id)}},
        )
    else:
        user_collection.update_one(
            {"_id": ideo, "email": encoded_email},
            {"$set": {"image": "/get_image/" + str(image_id)}},
        )

    return jsonify({"image_id": str(image_id)})

def handle_data_encryption(data):
    if data.get("bir"):
        data["bir"] = turbolancer_data_Security.encrypt(key, data["bir"])
    if data.get("gan"):
        data["gan"] = turbolancer_data_Security.encrypt(key, data["gan"])
    return data


def get_collection(ideo, encoded_email):
    if seller_collection.find_one({"_id": ideo, "email": encoded_email}):
        return seller_collection
    else:
        return user_collection


def split_into_child_arrays(original_array):
    child_arrays = []
    for i in range(0, len(original_array), 3):
        child_array = original_array[i : i + 3]
        child_arrays.append(child_array)
    return child_arrays

def collect_messages(data):
    combined_messages = {}
    
    for message_obj in data:
        room = message_obj['room']
        username = message_obj['username']
        keyy = (room, username)
        print(turbolancer_data_Security.decrypt(key, username))

        if keyy not in combined_messages:
            item = user_collection.find_one({'_id':turbolancer_data_Security.decrypt(key, username)}) or seller_collection.find_one({'_id':turbolancer_data_Security.decrypt(key, username)})
            combined_messages[keyy] = {
                'room': room,
                'username': item['name'] if item else 'Unknown User',
                'img': item['image'] if item else '/static/default_avatar.png',
                'message_count': 0
            }
        
        combined_messages[keyy]['message_count'] += len(message_obj['messages'])
    
    result = []
    for value in combined_messages.values():
        result.append({
            'room': value['room'],
            'username': value['username'],
            'img': value['img'],
            'message_count': value['message_count']
        })
    
    return result



# Form for uploading images
class ImageUploadForm(FlaskForm):
    image = FileField("Image")


@TurboLancer.route("/")
def main():
    try:
        cookies = getkey(request.cookies)
        if cookies.get("ideo"):
            id_ = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
            ud = seller_collection.find_one({"_id": id_}) or user_collection.find_one(
                {"_id": id_}
            )
            if (
                cookies.get("emalo") == ud.get("email")
                and ud.get("d") == "d"
                and not cookies.get("deno")
            ):
                return redirect(f'/addinfo/{id_}/{ud["name"]}/{ud["email"]}')
            elif (
                cookies.get("emalo") == ud["email"]
                and ud["d"] == "d"
                and cookies.get("deno")
            ):
                return redirect(f'/home-c/{id_}/{ud["d"]}')
            elif cookies.get("emalo") == ud["email"] and ud["d"] == "c":
                return redirect(f'/home-c/{id_}/{ud["d"]}')
    except Exception as e:
        print(f"An error occurred in main route: {e}")

    return render_template("index.html")


@TurboLancer.route("/start_selling_now", methods=["GET", "POST"])
def signup():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            name = request.form["name"]
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )
            encoded_phone = turbolancer_data_Security.encrypt(key, request.form["ph"])
            encoded_bir = turbolancer_data_Security.encrypt(
                key, request.form.get("bir")
            )
            encoded_gan = turbolancer_data_Security.encrypt(
                key, request.form.get("gan")
            )
            encoded_country = turbolancer_data_Security.encrypt(
                key, request.form["con"]
            )
            d = "d"

            user = (
                seller_collection.find_one({"email": encoded_email})
                or user_collection.find_one({"email": encoded_email})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_ph = (
                seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_id = generate_id()

            if user or user_ph:
                return render_template(
                    "signup-c.html",
                    x="Account already exists with this email/phone.",
                    y="onload= this.click",
                )
            else:
                t = name.replace(" ", "")
                tag = "@" + t
                user_id = generate_id()
                count = seller_collection.count_documents({"name": name})
                count_s = user_collection.count_documents({"name": name})
                count = str((int(count + count_s) + 1) * 1000)[::-1]
                year = dt.date.today().year
                month = dt.date.today().strftime("%b")
                count = str(count)
                if count:
                    count += str(random.randint(0, 9))
                user = {
                    "_id": user_id,
                    "image": "",
                    "name": name,
                    "tag": (tag + count).lower(),
                    "email": encoded_email,
                    "password": encoded_password,
                    "country": encoded_country,
                    "phone_number": encoded_phone,
                    "about_self": "",
                    "d": d,
                    "sk": [],
                    "grade": "C",
                    "earnings": [0],
                    "rating": 0,
                    "english": "",
                    "payment_method": "Visa",
                    "project_history": [],
                    "chat_rooms": [],
                    "account_created_in": str(month) + " " + str(year),
                    "bir": encoded_bir,
                    "gan": encoded_gan,
                }

                seller_collection.insert_one(user)
                ide = user_id
                user_id = turbolancer_data_Security.encrypt(key, user_id)
            return render_template(
                "save_cook.html",
                keys=[["ideo", "emalo", "tp"], [user_id, encoded_email, "d"]],
                redi=f"addinfo/{ide}/{name}/{encoded_email}",
            )
    except Exception as e:
        print(f"An error occurred in signup route: {e}")

    return render_template("signup-c.html")


@TurboLancer.route("/addinfo/<x>/<y>/<z>")
def addinfo(x, y, z):
    try:
        cookies = getkey(request.cookies)
        if cookies:
            if cookies.get("emalo") in z:
                return render_template(
                    "dataform.html",
                    id=x,
                    name=y,
                    email=z,
                    emaloz=turbolancer_data_Security.decrypt(key, cookies.get("emalo")),
                )
            else:
                return redirect(url_for("main"))
        else:
            return redirect(url_for("main"))
    except Exception as e:
        print(f"An error occurred in addinfo route: {e}")
        return redirect(url_for("main"))


@TurboLancer.route("/begin_client_journey", methods=["GET", "POST"])
def signup_and_upload_image():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            name = request.form.get("name")
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )
            encoded_phone = turbolancer_data_Security.encrypt(key, request.form["ph"])
            encoded_country = turbolancer_data_Security.encrypt(
                key, request.form["con"]
            )
            d = "c"
            encoded_bir = turbolancer_data_Security.encrypt(
                key, request.form.get("bir")
            )
            encoded_gan = turbolancer_data_Security.encrypt(
                key, request.form.get("gan")
            )

            user = (
                seller_collection.find_one({"email": encoded_email})
                or user_collection.find_one({"email": encoded_email})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_ph = (
                seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_id = generate_id()

            if "image" not in request.files:
                return jsonify(success=False, error="No image uploaded")

            image = request.files["image"]
            image_data = image.read()
            image_id = image_collection.insert_one({"data": image_data}).inserted_id

            if user or user_ph:
                return jsonify(success=False, error="Account already exists with this email/phone.")

            if user is None and user_ph is None:
                t = name.split(' ')[0]
                tag = "@" + t
                user_id = generate_id()
                count = seller_collection.count_documents({"name": name})
                count_s = user_collection.count_documents({"name": name})
                count = str((int(count + count_s) + 1) * 1000)[::-1]
                year = dt.date.today().year
                month = dt.date.today().strftime("%b")

                count = str(count)
                if count:
                    count += str(random.randint(0, 9))
                user = {
                    "_id": user_id,
                    "image": "/get_image/" + str(image_id),
                    "name": name,
                    "tag":(tag + count).lower(),
                    "email": encoded_email,
                    "password": encoded_password,
                    "country": encoded_country,
                    "phone_number": encoded_phone,
                    "d": d,
                    "spending": 0,
                    "account_created_in": str(month) + " " + str(year),
                    "payment_method": "Visa",
                    "orders_history": [],
                    "bir": encoded_bir,
                    "gan": encoded_gan,
                }

                user_collection.insert_one(user)
                ide = user_id
                user_id = turbolancer_data_Security.encrypt(key, user_id)
                redirect_url = f'/redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/none'
                return jsonify(success=True, redirect_url=redirect_url)

        return render_template("sin-c.html")
    except Exception as e:
        print(f"An error occurred in signup_and_upload_image route: {e}")
        return jsonify(success=False, error=str(e))



@TurboLancer.route("/signin", methods=["GET", "POST"])
def signin():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )

            user = seller_collection.find_one(
                {"email": encoded_email}
            ) or user_collection.find_one({"email": encoded_email})

            if user:
                stored_password = user["password"]
                if stored_password != encoded_password:
                    return jsonify({"error": "Incorrect password!"})
                else:
                    ide = user["_id"]
                    user_id = turbolancer_data_Security.encrypt(key, ide)

                    if user["d"] == "d" and (
                        user["image"] == "" or user["about_self"] == ""
                    ):
                        return jsonify(
                            {
                                "success": True,
                                "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/none',
                            }
                        )

                    return jsonify(
                        {
                            "success": True,
                            "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/_[__xxx__%12*79)(56)[:]-++784kdd]_',
                        }
                    )

            else:
                return jsonify({"error": "Account does not exist!"})
    except Exception as e:
        print(f"An error occurred in signin route: {e}")
        return jsonify({"error": "An error occurred during sign-in."})

    return render_template("singin.html")


@TurboLancer.route("/redi/<user_id>/<encoded_email>/<ide>/<user_d>/<deno>")
def redi(user_id, encoded_email, ide, user_d, deno):
    try:
        expected_deno = "_[__xxx__%12*79)(56)[:]-++784kdd]_"
        if unquote(expected_deno) == deno:
            return render_template(
                "save_cook.html",
                keys=[
                    ["ideo", "emalo", "tp", "deno"],
                    [user_id, encoded_email, user_d, deno],
                ],
                redi=f"/home-c/{ide}/{user_d}",
            )

        return render_template(
            "save_cook.html",
            keys=[["ideo", "emalo", "tp"], [user_id, encoded_email, user_d]],
            redi=f"/home-c/{ide}/{user_d}",
        )
    except Exception as e:
        print(f"An error occurred in redi route: {e}")
        return redirect(url_for("main"))


@TurboLancer.route("/UPLOAD_IMAGE", methods=["POST"])
def upload_image():
    try:
        if "image" in request.files:
            image = request.files["image"]
            encoded_email = request.form.get("email")

            developer = seller_collection.find_one({"email": encoded_email})

            if developer and "image" in developer:
                previous_image_link = developer["image"]
                if previous_image_link != "":
                    previous_image_id = previous_image_link.split("/")[-1]
                    image_collection.delete_one({"_id": ObjectId(previous_image_id)})

            image_data = image.read()
            image_id = image_collection.insert_one(
                {"data": image_data, "reference": developer["_id"]}
            ).inserted_id

            seller_collection.update_one(
                {"email": encoded_email},
                {"$set": {"image": "/get_image/" + str(image_id)}},
            )

            return jsonify({"image_id": str(image_id)})
        else:
            return jsonify({"error": "No image file found"})
    except Exception as e:
        print(f"An error occurred in upload_image route: {e}")
        return jsonify({"error": "An error occurred during image upload."})




@TurboLancer.route("/i/<image_id>", methods=["GET"])
def get_i(image_id):
    # Retrieve the image from the database
    image_data =  slideshow_collection.find_one({"_id": ObjectId(image_id)})

    if image_data and "data" in image_data:
        # Serve the image data with TurboLancerropriate content type
        return send_file(io.BytesIO(image_data["data"]), mimetype="image/jpeg")
    else:
        return jsonify({"error": "Image not found"})

@TurboLancer.route("/get_image/<image_id>", methods=["GET"])
def get_image(image_id):
    # Retrieve the image from the database
    image_data = image_collection.find_one({"_id": ObjectId(image_id)}) 

    if image_data and "data" in image_data:
        # Serve the image data with TurboLancerropriate content type
        return send_file(io.BytesIO(image_data["data"]), mimetype="image/jpeg")
    else:
        return jsonify({"error": "Image not found"})

    ##############################################################################################


@TurboLancer.route("/update_data", methods=["POST"])
def update_data():
    data = request.get_json()
    encoded_email = data.get("email")
    # (encoded_email)

    text_area_value = data.get("textAreaValue")

    if encoded_email and text_area_value:
        developer = seller_collection.find_one({"email": encoded_email})

        if developer:
            seller_collection.update_one(
                {"email": encoded_email}, {"$set": {"about_self": text_area_value}}
            )
            print(f"home-c/{developer['_id']}/d")
            return jsonify(
                {
                    "message": "_{__xxx__%12*79)(56)[:]-++784kdd}_",
                    "ne": "deno",
                    "re": f"/home-c/{developer['_id']}/d",
                }
            )
        else:
            return jsonify({"error": "seller not found."})
    else:
        return jsonify({"error": "Invalid data."})


@TurboLancer.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Sorry! Resource not found"}), 404


@TurboLancer.route("/home-c/<x>/<y>")
def home_c(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))

    elif (
        check(request.cookies, "file")
        and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != x
    ):
        return redirect(url_for("main"))
    user_data = user_collection.find_one(
        {"_id": x, "d": y}
    ) or seller_collection.find_one({"_id": x})

    if user_data:
        image = user_data["image"]
        name = user_data["name"]
        tag = user_data["tag"]
        user_id = x
        account = ["c", "d"]

        if "c" in account:
            return render_template(
                "clint-side-db.html",
                name=name,
                image=image,
                tag=tag,
                d=y,
                aclink=f"/account/{user_id}/{y}",
                c="c",
                allink=f"/dashboard/{user_id}/{y}",
            )

    return redirect(url_for("main"))


@TurboLancer.route("/dashboard/<x>/<y>")
def dashboard(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))

    elif (
        check(request.cookies, "file")
        and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != x
    ):
        return redirect(url_for("main"))
    Seller_data = seller_collection.find_one({"_id": x, "d": y})

    if Seller_data:
        cat = list(catalogue_collection.find({"seller_id": x}))

        seller_dataS = get_seller_data(x)
        if seller_dataS:
            # Dummy data for seller_dataS
            seller_dataS["total_catalog_items"] = len(cat)
            seller_dataS["total_projects"] = 42
            seller_dataS["rating"] = float(seller_dataS["rating"])
            seller_dataS['um'] = collect_messages(Seller_data['unreadMessages'])
        if "d" in y:
            return render_template(
                "dashboard.html",
                **seller_dataS,
                aclink=f"/account/{x}/{y}",
                allink=f"/home-c/{x}/{y}",
                _id=x,
            )

    return redirect(url_for("main"))

@TurboLancer.route('/notification', methods=['POST'])
def notification():
    data = request.json.get('id')

    if not check(request.cookies, "file"):
        return redirect(url_for("main"))
    
    elif (check(request.cookies, "file") and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != data):
        return redirect(url_for("main"))
    
    user = user_collection.find_one({'_id': data}) or seller_collection.find_one({'_id':data})
    if user and user['unreadMessages']:
        return jsonify({'um':collect_messages(user['unreadMessages'])})
    return jsonify({'not_Found':True})


@TurboLancer.route("/complete_catalogue/<x>", methods=["POST"])
def cc(x):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))
    try:
        id = ObjectId(x)
        data: list = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        cat: dict = draft_catalogue_collection.find_one({'_id': id})
        print(cat)
        if not cat:
            return jsonify({'error': 'Draft catalogue not found'}), 404

        del cat['draft']
        cat['questions'] = data
        result = catalogue_collection.insert_one(cat)
        draft_catalogue_collection.delete_one({'_id': id})
        if not result.acknowledged:
            return jsonify({'error': 'Failed to insert catalogue'}), 500

        return jsonify({'success': True, 'inserted_id': str(result.inserted_id)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@TurboLancer.route("/catalogue/<x>/<y>", methods=["GET", "POST"])
def catalogue(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))
    
    decrypted_key = turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"])
    if check(request.cookies, "file") and decrypted_key != x:
        return redirect(url_for("main"))
    
    Seller_data = seller_collection.find_one({"_id": x, "d": y})
    if not Seller_data:
        return jsonify({"success": False}), 404
    
    if request.method == "GET":
        new = []
        cat = list(catalogue_collection.find({"seller_id": x}))
        draft = list(draft_catalogue_collection.find({"seller_id": x})) or []
        for i in draft: cat.append(i)
        
        if cat:
            res = None
            for item in cat:
                res = new_or_not(item['date'])
                id = item["_id"]
                item['res'] = res
                new.append(id)
            return render_template("catalogue.html", **Seller_data, cat=cat, c_id=new,)
        return render_template("catalogue.html", **Seller_data)
    
    if request.method == "POST":
        data = request.form.to_dict()
        uploaded_files = request.files.getlist('images')
        images = []
        
        for file in uploaded_files:
            binary_data = file.read()
            img_id = slideshow_collection.insert_one({'data': binary_data, 'reference': x}).inserted_id
            images.append("/i/" + str(img_id))
        
        print(images)
        
        catalogue_data = {
            'title': data.get('title'),
            'seller_id': x,
            'category': data.get('category'),
            'description': data.get('description'),
            'tags': json.loads(data.get('tags', '[]')),
            'images': images,
            'inputLabels': json.loads(data.get('inputLabels', '[]')),
            'inputValues': json.loads(data.get('inputValues', '[]')),
            'date': dt.date.today().strftime("%d/%m/%y"),
            'seller_image': Seller_data.get('image'),
            'seller_name': Seller_data.get('name'),
            'likes': 0,
            'orders': 0,
            'clicks': 0,
            'draft': True
        }
        
        cataid = draft_catalogue_collection.insert_one(catalogue_data).inserted_id
        return jsonify({"success": True,'catid': str(cataid)})
    
    return jsonify({"success": False})

@TurboLancer.route("/dell_catalogue", methods=["POST"])
def dell_catalogue():
    if not check(request.cookies, "file"):
        return jsonify({'success': False})
    else:
        decrypted_key = turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"])
        data = request.form.to_dict()
        taken = data.get('id')

        if taken:
            catalogue = catalogue_collection.find_one({'_id': ObjectId(taken)}) or draft_catalogue_collection.find_one({'_id': ObjectId(taken)})
            if catalogue and (catalogue.get('seller_id') == decrypted_key):
                for img in catalogue['images']:
                    delete_image(img)
                
                catalogue_collection.delete_one({'_id': ObjectId(taken)}) if not catalogue.get('draft',None) else draft_catalogue_collection.delete_one({'_id': ObjectId(taken)})
                return jsonify({"success": True})
            else:
                return jsonify({'success': False})
        else:
            return jsonify({'success': False})

@TurboLancer.route('/full_catalogue/<id>')
def full_catalogue(id):
    data = catalogue_collection.find_one({'_id':ObjectId(id)}) or draft_catalogue_collection.find_one({'_id':ObjectId(id)})
    seller = seller_collection.find_one({'_id':data['seller_id']})
    listA:list = data['inputLabels']
    listB:list = data['inputValues']
    pakeages = {'Basic': [], 'Standard': [], 'Premium': []}


    for i, label in enumerate(listA):
        package = 'Basic' if i % 3 == 0 else 'Standard' if i % 3 == 1 else 'Premium'
        if i < len(listB):
            pakeages[package].append((label, listB[i]))
    cookies = getkey(request.cookies)
    ideo = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
    print(pakeages)
    if data and seller:
        

        owner :dict = {
        'Stag':seller['tag'],
        'country':turbolancer_data_Security.decrypt(key, seller['country']),
        'name': seller['name'],
        'S_id': seller['_id'],
        'data': pakeages
    }
        return render_template('full_catalogue.html', **data, **owner, x = 6 if ideo == seller['_id'] else 0)
    else:
        return redirect("/NotFound")




@TurboLancer.route("/order_specifications/<x>/<y>")
def order_specifications(x, y):
    print("Entering order_specifications with x={}, y={}".format(x, y))
    if not check(request.cookies, "file"):
        print("User is not logged in, redirecting to main")
        return redirect(url_for("main"))
    elif check(request.cookies, "file") and not 'Y3VzdG9taXplZA==' in x:
        data = catalogue_collection.find_one({'_id': ObjectId(x)})
        if data:
            ideo = turbolancer_data_Security.decrypt(key, getkey(request.cookies).get("ideo"))
            ideo = user_collection.find_one({'_id': ideo}) or seller_collection.find_one({'_id': ideo})
            image = ideo['image']
            name = ideo['name']
            return render_template('order_specifications.html', data=data['questions'], name=name, image=image, price=y)
        else:
            print("Catalog item not found, redirecting to NotFound")
            return redirect('/NotFound')
    elif check(request.cookies, "file") and 'Y3VzdG9taXplZA==' in x:
        seller = x.replace('Y3VzdG9taXplZA==', '')
        seller = b64decode(seller)
        seller = turbolancer_data_Security.decrypt(key, seller.decode('utf-8'))
        seller = seller_collection.find_one({'_id': seller})
        ideo = turbolancer_data_Security.decrypt(key, getkey(request.cookies).get("ideo"))
        ideo = user_collection.find_one({'_id': ideo}) or seller_collection.find_one({'_id': ideo})
        if seller and ideo and (seller['phone_number'] != ideo['phone_number']):
            image = ideo['image']
            name = ideo['name']
            return render_template('order_specifications.html', name=name, image=image, price=y)
    print("Redirecting to NotFound")
    return redirect('/NotFound')



@TurboLancer.route("/update_profile", methods=["POST"])
def update_profile():
    cookies = getkey(request.cookies)
    image_data = ""
    encoded_email = cookies.get("emalo")
    ideo = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
    check_result = check(request.cookies, "file")
    if not check_result:
        return redirect(url_for("main"))

    elif check_result and request.method == "POST":
        data = dict(request.form)
        print(data)
        file = request.files.get("image")
        if file:
            image_data = file.read()
            upload_image_local(image_data, encoded_email, ideo)

        data = handle_data_encryption(data)
        print(data)
        collection = get_collection(ideo, encoded_email)
        update_database(collection, ideo, encoded_email, data)

        print(data)
        return jsonify({"success": True})

    return jsonify({"success": False})




@TurboLancer.route("/delItem", methods=["POST"])
def delItem():
    cookies = getkey(request.cookies)
    encoded_email = cookies.get("emalo")
    ideo = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
    check_result = check(request.cookies, "file")
    if not check_result:
        return redirect(url_for("main"))

    elif check_result and request.method == "POST":
        data = request.form
        print(data["sk"])
        ud = seller_collection.find_one({"_id": ideo, "email": encoded_email})
        if ud and ud["sk"]:
            base: list = ud["sk"]
            for x in range(len(ud["sk"])):
                if base[x][0] == data["sk"]:
                    base.pop(x)
                    seller_collection.update_one(
                        {"_id": ideo, "email": encoded_email}, {"$set": {"sk": base}}
                    )
                    return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})

@TurboLancer.route("/account/<x>/<y>")
def account(x, y):
    res = check(request.cookies, "file")
    print(res)
    if not res:
        return redirect(url_for("main"))

    decrypted_x = turbolancer_data_Security.decrypt(
        key, getkey(request.cookies)["ideo"]
    )

    if res and (decrypted_x != x):
        if y in ["c", "d"]:
            if y == "c":
                return redirect("/NotFound")
            elif y == "d":
                seller_data = get_seller_data(x)
                if seller_data:
                    new = []
                    cat = list(catalogue_collection.find({"seller_id": x}))
                    if cat:
                        for item in cat:
                            item['sell'] = 'Yes' if seller_data.get('dd') and (item['seller_id'] == seller_data['dd']) else None
                            item['res'] = new_or_not(item['date'])
                            new.append(item["_id"])
                    
                    # Combine seller_data with additional data
                    seller_data["total_catalog_items"] = len(cat)
                    seller_data["total_projects"] = 42  # Replace with actual data
                    seller_data["rating"] = float(seller_data["rating"])
                    
                    return render_template(
                        "profile_page.html", **seller_data, d="avail", cat=cat, c_id=new
                    )
                return redirect(url_for("main"))
        return redirect(url_for("main"))

    if res and (decrypted_x == x) and (y in ["c", "d"]):
        if y == "c":
            user_data = get_user_dataA(x)
            if user_data:
                # Dummy data for user_data
                user_data["total_earnings"] = "$12,345"
                user_data["total_catalog_items"] = 125
                user_data["total_projects"] = 42
                user_data["user_rating"] = 4.8
                return render_template(
                    "profile_page.html", **user_data, x="yes", c="yes"
                )
        elif y == "d":
            seller_data = get_seller_data(x)
            if seller_data:
                new = []
                cat = list(catalogue_collection.find({"seller_id": x}))
                if cat:
                    for item in cat:
                        item['sell'] = 'Yes' if seller_data.get('dd') and (item['seller_id'] == seller_data['dd']) else None
                        item['res'] = new_or_not(item['date'])
                        new.append(item["_id"])
                
                # Combine seller_data with additional data
                seller_data["total_catalog_items"] = len(cat)
                seller_data["total_projects"] = 42  # Replace with actual data
                seller_data["rating"] = float(seller_data["rating"])
                
                return render_template(
                    "profile_page.html", **seller_data, d="avail", x="yes", cat=cat, c_id=new
                )
            return redirect(url_for("main"))

    return redirect(url_for("main"))

@TurboLancer.route('/<tag>')
def tag_pf(tag):
    res = check(request.cookies, "file")
    print(res)
    if not res:
        return redirect(url_for("main"))

    decrypted_x = turbolancer_data_Security.decrypt(
        key, getkey(request.cookies)["ideo"]
    )
    user = seller_collection.find_one({'tag':tag}) or user_collection.find_one({'tag':tag})
    x = user['_id'] if user else None
    y = user['d'] if user else None
    if res and (decrypted_x != x):
        if y in ["c", "d"]:
            if y == "c":
                return redirect("/NotFound")
            elif y == "d":
                seller_data = get_seller_data(x)
                if seller_data:
                    new = []
                    cat = list(catalogue_collection.find({"seller_id": x}))
                    if cat:
                        for item in cat:
                            item['sell'] = 'Yes' if seller_data.get('dd') and (item['seller_id'] == seller_data['dd']) else None
                            item['res'] = new_or_not(item['date'])
                            new.append(item["_id"])
                    
                    # Combine seller_data with additional data
                    seller_data["total_catalog_items"] = len(cat)
                    seller_data["total_projects"] = 42  # Replace with actual data
                    seller_data["rating"] = float(seller_data["rating"])
                    
                    return render_template(
                        "profile_page.html", **seller_data, d="avail", cat=cat, c_id=new
                    )
                return redirect(url_for("main"))
        return redirect(url_for("main"))

    if res and (decrypted_x == x) and (y in ["c", "d"]):
        if y == "c":
            user_data = get_user_dataA(x)
            if user_data:
                # Dummy data for user_data
                user_data["total_earnings"] = "$12,345"
                user_data["total_catalog_items"] = 125
                user_data["total_projects"] = 42
                user_data["user_rating"] = 4.8
                return render_template(
                    "profile_page.html", **user_data, x="yes", c="yes"
                )
        elif y == "d":
            seller_data = get_seller_data(x)
            if seller_data:
                new = []
                cat = list(catalogue_collection.find({"seller_id": x}))
                if cat:
                    for item in cat:
                        item['sell'] = 'Yes' if seller_data.get('dd') and (item['seller_id'] == seller_data['dd']) else None
                        item['res'] = new_or_not(item['date'])
                        new.append(item["_id"])
                
                # Combine seller_data with additional data
                seller_data["total_catalog_items"] = len(cat)
                seller_data["total_projects"] = 42  # Replace with actual data
                seller_data["rating"] = float(seller_data["rating"])
                
                return render_template(
                    "profile_page.html", **seller_data, d="avail", x="yes", cat=cat, c_id=new
                )
            return redirect(url_for("main"))

    return redirect(url_for("main"))


@TurboLancer.errorhandler(404)
def page_not_found(error):
    return "404"


@TurboLancer.route("/upjobpage")
def page():
    return render_template("upload_job.html")


@TurboLancer.route("/getserved")
def get_searved():
 
    Seller:dict = seller_collection.find_one({"_id": turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]), "d": 'd'}) or {'_id':'000'}
    print(Seller)
    new = []
    Seller_data: dict = {}
    cat = list(catalogue_collection.find())
    if cat:
        res = None
        for item in cat:
            Seller_data = seller_collection.find_one({"_id": item['seller_id'], "d": 'd'})
            res = new_or_not(item['date'])
            id = item["_id"]
            item['sell'] = 'Yes' if Seller.get('_id') and (item['seller_id']  == Seller['_id']) else None
            item['res'] = res
            new.append(id)
        return render_template("get_served.html", **Seller_data, cat=cat, c_id=new)
    return render_template("get_served.html", **Seller_data)


@TurboLancer.route("/proj")
def proj():
    return render_template("project.html")





@TurboLancer.route("/rephrase_text", methods=["POST"])
def rephrase():
    data = request.get_json()
    input_text = data.get("text")
    main = data.get("main")
    print(main)
    print(input_text)
    response = TurboLancer_RePhrase_text.do(input_text, main)

    response = response.replace("\n", "")
    response = response.replace("]]", "")
    response = response.replace("[[", "")
    response = response.replace("[[[", "")
    response = response.replace("]]]", "")
    response = response.replace("IIPlease", "")
    response = response.replace("IPlease", "")
    response = response.replace("IIIPlease", "")
    response = response.replace("IIIIPlease", "")
    response = response.replace("TheI", "I")
    response = response.replace("I I", "I")
    response = response.replace("II", "I")
    response = response.replace("BasedBased on", "Based")
    response = response.replace("BasedBased", "")
    response = response.replace("Based the", "Based on the")
    response = response.replace("the client form", "this project")
    response = response.replace("is is", "is")
    response = response.replace("ForFor", "For")
    response = response.replace("BasedI", "I")
    response = response.replace("[IBased", "Based")
    response = remove_word_without_space(response, "Based")
    response = remove_word_without_space(response, "The")
    response = remove_word_without_space(response, "For")
    # response = remove_first_uppercase(response)

    print(response)
    return jsonify(text=response)

######################################################################################################################
#############################################CHAT TurboLancer#################################################################
######################################################################################################################

@TurboLancer.route('/chat/<room>')
def index(room):
    res = check(request.cookies, "file")
    print(res)
    if not res:
        return redirect("/NotFound")
    
    id = getkey(request.cookies).get('ideo')
    ch = chatroom_collection.find_one({
        'name': room,
        'users': {'$elemMatch': {'username': id}}
    })
    
    if ch:
        user_data = user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key,id)}) or seller_collection.find_one({'_id': turbolancer_data_Security.decrypt(key,id)})
        
        for room_data in user_data['rooms']:
            if room_data['room'] == room:
                user_has_buy = room_data.get('buy', False)
                break
        else:
            user_has_buy = False
        
        return render_template('chat.html', un=id, x=room, user_has_buy= user_has_buy)
    else:
        return redirect("/NotFound")
 
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    chatroom = chatroom_collection.find_one({'name': room})
    if chatroom is None:
        chatroom = {'name': room, 'users': [], 'messages': []}

    # Fetch current users in the chatroom
    current_users = chatroom.get('users', [])
    user_exists = False
    users_info = []

    for user in current_users:
        decrypted_username = turbolancer_data_Security.decrypt(key, user['username'])
        user_data = user_collection.find_one({'_id': decrypted_username}) or seller_collection.find_one({'_id': decrypted_username})

        if user_data:
            online_status = bool(user.get('sid'))
            user_info = {
                'id': turbolancer_data_Security.encrypt(key, user_data['_id']),
                'name': user_data['name'],
                'image': user_data['image'],
                'tag': user_data.get('tag', ''),
                'online': online_status
            }
            users_info.append(user_info)

            if user['username'] == username:
                user['sid'] = request.sid
                user_exists = True

                # Remove all unread messages for this room from the user's document
                user_collection_to_check = user_collection if user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}) else seller_collection
                for item in user_collection_to_check.find_one({'_id': turbolancer_data_Security.decrypt(key, username)})['unreadMessages'] if user_collection_to_check.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}).get('unreadMessages') else []:
                    if item['room'] == room:
                        user_collection_to_check.update_one(
                            {'_id': turbolancer_data_Security.decrypt(key, username)},
                            {'$pull': {'unreadMessages': {'room': room}}}
                        )
            else:
                # Emit other user's status to the joining user
                emit('status', user_info, room=request.sid)

    if not user_exists:
        current_users.append({'username': username, 'sid': request.sid, 'online': True, 'last_active': time.time()})
    else:
        for user in current_users:
            if user['username'] == username:
                user['sid'] = request.sid
                user['online'] = True
                user['last_active'] = time.time()

    chatroom_collection.update_one(
        {'name': room},
        {'$set': {'users': current_users}},
        upsert=True
    )

    for user_info in users_info:
        emit('status', user_info, room=room)

    if 'messages' in chatroom:
        for message in chatroom['messages']:
                        emit('response', {
                    'message': message['message'],
                    'sender': message['sender'],
                    'timestamp': message['timestamp'],
                    'type': message['type'],
                    'caption': message.get('caption', ''),
                    'replyTo': message.get('replyTo', None),
                    'filename': message.get('filename', '')
                }, room=request.sid)
    # Broadcast the current user's status to others
    current_user_data = user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}) or seller_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)})
    if current_user_data:
        current_user_info = {
            'id': turbolancer_data_Security.encrypt(key, current_user_data['_id']),
            'name': current_user_data['name'],
            'image': current_user_data['image'],
            'online': True
        }
        emit('status', current_user_info, room=room)

 
@socketio.on('Rejoin')
def on_re_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    chatroom = chatroom_collection.find_one({'name': room})
    if chatroom is None:
        chatroom = {'name': room, 'users': [], 'messages': []}

    # Fetch current users in the chatroom
    current_users = chatroom.get('users', [])
    user_exists = False
    users_info = []

    for user in current_users:
        decrypted_username = turbolancer_data_Security.decrypt(key, user['username'])
        user_data = user_collection.find_one({'_id': decrypted_username}) or seller_collection.find_one({'_id': decrypted_username})

        if user_data:
            online_status = bool(user.get('sid'))
            user_info = {
                'id': turbolancer_data_Security.encrypt(key, user_data['_id']),
                'name': user_data['name'],
                'image': user_data['image'],
                'tag': user_data.get('tag', ''),
                'online': online_status
            }
            users_info.append(user_info)

            if user['username'] == username:
                user['sid'] = request.sid
                user_exists = True

                # Remove all unread messages for this room from the user's document
                user_collection_to_check = user_collection if user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}) else seller_collection
                for item in user_collection_to_check.find_one({'_id': turbolancer_data_Security.decrypt(key, username)})['unreadMessages'] if user_collection_to_check.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}).get('unreadMessages') else []:
                    if item['room'] == room:
                        user_collection_to_check.update_one(
                            {'_id': turbolancer_data_Security.decrypt(key, username)},
                            {'$pull': {'unreadMessages': {'room': room}}}
                        )
            else:
                # Emit other user's status to the joining user
                emit('status', user_info, room=request.sid)

    if not user_exists:
        current_users.append({'username': username, 'sid': request.sid})
    else:
        for user in current_users:
            if user['username'] == username:
                user['sid'] = request.sid

    chatroom_collection.update_one(
        {'name': room},
        {'$set': {'users': current_users}},
        upsert=True
    )

    for user_info in users_info:
        emit('status', user_info, room=room)

    
    # Broadcast the current user's status to others
    current_user_data = user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}) or seller_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)})
    if current_user_data:
        current_user_info = {
            'id': turbolancer_data_Security.encrypt(key, current_user_data['_id']),
            'name': current_user_data['name'],
            'image': current_user_data['image'],
            'online': True
        }
        emit('status', current_user_info, room=room)




@TurboLancer.route('/messenger')
def  messenger():
    if not check(request.cookies, "file"):
        return redirect("/NotFound")
    encrypted_id = getkey(request.cookies).get('ideo')
    user_id = turbolancer_data_Security.decrypt(key, encrypted_id)
    user = user_collection.find_one({'_id': user_id}) or seller_collection.find_one({'_id': user_id})
    data_arr : list[dict] = []
    if user:
        for item in user.get('rooms', []):
            temp = user_collection.find_one({'_id': item['username']}) or seller_collection.find_one({'_id': item['username']})
            patner : dict = temp if temp else {}
            data : dict = {
                'name' : patner.get('name'),
                'image': patner.get('image'),
                'room':'/chat/'+item.get('room')
            }
            data_arr.append(data)
        sorted_data = sorted(data_arr, key=lambda x: x['name'])
        return render_template('messenger.html',data = sorted_data, _id = user_id)
    
    return redirect("/NotFound")






@TurboLancer.route('/create_chat/<other_username>')
def create_chat(other_username):
    if not check(request.cookies, "file"):
        return redirect("/NotFound")

    encrypted_id = getkey(request.cookies).get('ideo')
    current_user_id = turbolancer_data_Security.decrypt(key, encrypted_id)

    current_user = (
        user_collection.find_one({'_id': current_user_id}) or 
        seller_collection.find_one({'_id': current_user_id})
    )
    if not current_user:
        return redirect("/NotFound")

    for room in current_user.get('rooms', []):
        if room['username'] == other_username:
            return redirect(f'/chat/{room['room']}')

    room_id = str(uuid.uuid4())

    current_user_collection = seller_collection if current_user['d'] == 'd' else user_collection
    current_user_collection.update_one(
        {'_id': current_user_id},
        {'$push': {'rooms': {'username': other_username, 'room': room_id,'buy':True}}}
    )

    other_user = (
        user_collection.find_one({'_id': other_username}) or 
        seller_collection.find_one({'_id': other_username})
    )
    if not other_user:
        return redirect("/NotFound")

    other_user_collection = seller_collection if other_user.get('d') == 'd' else user_collection
    other_user_collection.update_one(
        {'_id': other_username},
        {'$push': {'rooms': {'username': current_user_id, 'room': room_id}}}
    )

    chatroom_collection.insert_one({
        'name': room_id,
        'users': [
            {'username': turbolancer_data_Security.encrypt(key, other_username)},
            {'username': encrypted_id}
        ]
    })

    return redirect(f'/chat/{room_id}')
    

@TurboLancer.route('/chatImg/<x>', methods=['GET'])
def get_chat_img(x):
    try:
        img = chatImages_collection.find_one({'_id': ObjectId(x)})
        if not img:
            return jsonify({"error": "Image not found"}), 404

        encrypted_id = getkey(request.cookies).get('ideo')
        if not encrypted_id:
            return jsonify({"error": "Invalid encryption key"}), 403

        t = any(item.get('username') == encrypted_id for item in img.get('users', []))

        if "data" in img and t:
            return send_file(io.BytesIO(img["data"]), mimetype="image/jpeg")
        else:
            return jsonify({"error": "image data not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def upload_image_chat(image_data, chatroom_id, users):
    image_id = chatImages_collection.insert_one({"data": image_data, "reference": chatroom_id,'users':users}).inserted_id
    return image_id

@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    message = data.get('message')
    username = data.get('username')
    reply_to = data.get('replyTo')

    if room and username:
        timestamp = datetime.now(pytz.utc).isoformat()

      # Check if the reply_to message is an 'offer' and update it
        if reply_to:
            chatroom_doc = chatroom_collection.find_one(
                {'name': room, 'messages.timestamp': reply_to},
                {'messages.$': 1}
            )
            if chatroom_doc and 'messages' in chatroom_doc:
                # Extract the message from the document
                reply_to_message = chatroom_doc['messages'][0]
                if reply_to_message['type'] == 'offer':
                    chatroom_collection.update_one(
                        {'name': room, 'messages.timestamp': reply_to},
                        {'$set': {
                            'messages.$.type': 'deleted',
                            'messages.$.message': 'Submitted an offer'
                        }}
                    )
        

        try:
            message_data = {
                'sender': username,
                'message': message,
                'timestamp': timestamp,
                'type': 'text',
                'replyTo': reply_to if reply_to else None
            }

            if data.get('type') == 'offer':
                message_data['type'] = 'offer'
            elif data.get('file'):
                file_data = b64decode(data['file'])
                file_id = upload_file_chat(file_data, room, data['filename'])
                file_url = f'/chatFile/{file_id}'
                message_data['message'] = file_url
                message_data['type'] = 'file'
                message_data['filename'] = data['filename']
            elif data.get('image'):
                image_data = b64decode(data['image'].split(",")[1])
                caption = data.get('caption', '')
                chatroom = chatroom_collection.find_one({'name': room}, {'users': 1})
                if chatroom and 'users' in chatroom:
                    image_id = upload_image_chat(image_data, room, chatroom['users'])
                    image_url = f'/chatImg/{image_id}'
                    message_data['message'] = image_url
                    message_data['type'] = 'image'
                    message_data['caption'] = caption

            # Store the message in the chatroom collection
            chatroom_collection.update_one(
                {'name': room},
                {'$push': {'messages': message_data}},
                upsert=True
            )

            emit('response', {
                'message': message_data['message'],
                'sender': message_data['sender'],
                'timestamp': message_data['timestamp'],
                'type': message_data['type'],
                'caption': message_data.get('caption', ''),
                'replyTo': message_data.get('replyTo', None),
                'filename': message_data.get('filename', '')
            }, room=room)

            # Handle unread messages for offline recipients
            chatroom = chatroom_collection.find_one({'name': room}, {'users': 1})
            if chatroom and 'users' in chatroom and chatroom['users']:
                recipient_user = next((user for user in chatroom['users'] if user['username'] != data['username']), None)
                if recipient_user and not recipient_user.get('sid'):
                    recipient_username = turbolancer_data_Security.decrypt(key, recipient_user['username'])
                    recipient_collection = user_collection if user_collection.find_one({'_id': recipient_username}) else seller_collection

                    recipient_collection.update_one(
                        {'_id': recipient_username},
                        {'$push': {'unreadMessages': {'$each': [{'room': room, 'username': username, 'messages': [message_data]}], '$position': 0}}},
                        upsert=True
                    )
        except Exception as e:
            print(f"Error updating database: {e}")
            emit('error', {'msg': 'Failed to send message.'}, room=request.sid)
    else:
        emit('error', {'msg': 'Invalid message data.'}, room=request.sid)
        
def upload_file_chat(file_data, chatroom_id, filename):
    file_id = chatFiles_collection.insert_one({
        "data": file_data, 
        "reference": chatroom_id, 
        "filename": filename
    }).inserted_id
    return file_id

@TurboLancer.route('/chatFile/<x>', methods=['GET'])
def get_chat_file(x):
    file_doc = chatFiles_collection.find_one({'_id': ObjectId(x)})
    if file_doc and "data" in file_doc:
        return send_file(io.BytesIO(file_doc["data"]), 
                        download_name=file_doc["filename"], 
                        as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


@TurboLancer.route('/offer')
def bid():
    if not check(request.cookies, "file"):
        return redirect("/NotFound")
    return render_template('offer.html')


@socketio.on('disconnect')
def on_disconnect():
    chatroom = chatroom_collection.find_one({'users.sid': request.sid})
    if chatroom:
        username = None
        room = chatroom['name']
        current_users = chatroom['users']
        for user in current_users:
            if user['sid'] == request.sid:
                username = user['username']
                user['sid'] = None
                user['online'] = False  # Set user to offline
                user['last_active'] = time.time()  # Update last active time
                break

        if username:
            chatroom_collection.update_one(
                {'name': room},
                {'$set': {'users': current_users}},
                upsert=True
            )
            leave_room(room)
            user_details = user_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)}) or seller_collection.find_one({'_id': turbolancer_data_Security.decrypt(key, username)})
            if user_details:
                status_data = {
                    'id': username,
                    'name': user_details['name'],
                    'image': user_details['image'],
                    'online': False
                }
                emit('status', status_data, room=room)
            else:
                emit('status', {'msg': f'{username} has disconnected.', 'online': False, 'id': username}, room=room)


@socketio.on('deleteMessage')
def handle_delete_message(data):
    message_id = data.get('messageId')
    room = data.get('room')
    username = data.get('username')
    if message_id and room and username:
        try:
            chatroom = chatroom_collection.find_one({'name': room})
            if chatroom and 'messages' in chatroom:
                for message in chatroom['messages']:
                    if (message.get('timestamp') == message_id) and (message.get('sender') == username):
                        if message['type'] == 'image':
                            chatImages_collection.delete_one({'_id':ObjectId(message['message'].split('/')[2])})
                            message['message'] = "This message was deleted"
                            message['type'] = 'deleted'
                            if 'replyTo' in message: del message['replyTo']
                            if 'caption' in message: del message['caption']
                            break
                        elif message['type'] == 'file':
                            chatFiles_collection.delete_one({'_id':ObjectId(message['message'].split('/')[2])})
                            message['message'] = "This message was deleted"
                            message['type'] = 'deleted'
                            if 'replyTo' in message: del message['replyTo']
                            if 'caption' in message: del message['caption']
                            break
                        else:
                            message['message'] = "This message was deleted"
                            message['type'] = 'deleted'
                            if 'replyTo' in message: del message['replyTo']
                            if 'filename' in message: del message['filename']
                            break
                chatroom_collection.update_one({'name': room}, {'$set': {'messages': chatroom['messages']}})
                emit('delDone', ["This message was deleted", message['sender'], message_id, "deleted"], room=room)
        except Exception as e:
            print(f"Error deleting message: {e}")
            emit('error', {'msg': 'Failed to delete message.'}, room=request.sid)
    else:
        emit('error', {'msg': 'Invalid delete request.'}, room=request.sid)

@socketio.on('heartbeat')
def handle_heartbeat(data):
    username = data['username']
    room = data['room']
    chatroom_collection.update_one(
        {'name': room, 'users.username': username},
        {'$set': {'users.$.last_active': time.time()}}
    )

@socketio.on('user_inactive')
def handle_user_inactive(data):
    username = data['username']
    room = data['room']
    update_user_status(username, room, False)

@socketio.on('user_active')
def handle_user_active(data):
    username = data['username']
    room = data['room']
    update_user_status(username, room, True)

def update_user_status(username, room, is_active):
    chatroom = chatroom_collection.find_one({'name': room})
    if chatroom:
        for user in chatroom['users']:
            if user['username'] == username:
                user['online'] = is_active
                user['last_active'] = time.time()
        chatroom_collection.update_one({'name': room}, {'$set': {'users': chatroom['users']}})
        emit('status', {'username': username, 'online': is_active}, room=room)
        
        
        

if __name__ == "__main__":
    socketio.run(TurboLancer, debug=True)
