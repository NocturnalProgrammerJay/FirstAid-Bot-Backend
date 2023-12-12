from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS module
import pymongo
from bson import ObjectId

app = Flask(__name__)
CORS(app) 

# Set up MongoDB connection
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = client.LikesDB
collection = db.test1

def update_likes(query_string, likes_change):
    # Assuming you have an ObjectId for the document you want to update
    document_id = ObjectId("6566c938860f47b3b47a9c9e")

    # Fetch the document
    current_data = collection.find_one({"_id": document_id})

    # Check if the query string is either "ModMed" or "ChatGPT"
    if query_string in ["ModMed", "ChatGPT"]:
        # Construct the update based on the query string
        update = {
            f"{query_string}.Likes": current_data[query_string]["Likes"] + likes_change,
            "TotalLikes": current_data["TotalLikes"] + likes_change
        }

        # Update the document in the collection
        updated_data = collection.update_one(
            {"_id": document_id},
            {"$set": update}
        )

        # Check if the update was successful
        if updated_data.modified_count > 0:
            # Construct the response object
            response_object = {
                "queryString": query_string,
                "Likes": current_data[query_string]["Likes"] + likes_change,
                "TotalLikes": current_data["TotalLikes"] + likes_change
            }
            print(f"Document updated successfully for {query_string}")
            print("Response Object:", response_object)
            return response_object

    else:
        print("Invalid query string")

    return None

# Example route to handle the request for decrementing likes
@app.route('/decrement_likes/<query_string>', methods=['POST'])
def decrement_likes(query_string):
    return jsonify(update_likes(query_string, -1))

# Example route to handle the request for incrementing likes
@app.route('/increment_likes/<query_string>', methods=['POST'])
def increment_likes(query_string):
    return jsonify(update_likes(query_string, 1))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)


