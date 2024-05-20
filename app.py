from flask import Flask, request, render_template, redirect, url_for,jsonify
import mysql.connector
from datetime import datetime
import google.generativeai as genai

app = Flask(__name__)

# Function to establish connection to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )

@app.route('/')
def index():
     return render_template('Guest.html')

@app.route('/feedback')
def feedback():
     return render_template('feedback.html')   
                        
@app.route('/submit_review', methods=['POST'])
def submit_review():
    # Retrieve review data from the form
    review_text = request.form['review_text']
    review_type = request.form['review_type']
    timestamp = datetime.now()
    
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()
    print(f"Review text: {review_text}")
    # Execute an SQL query to insert the review into the database
    query = "INSERT INTO feedback (review_text, review_type,timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (review_text, review_type,timestamp))

    # Commit the transaction
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Redirect the user to the homepage or another appropriate page
    return redirect(url_for('feedback'))






# Configure generative model
genai.configure(api_key="AIzaSyDbXSEfwrEw47cF1evZjGzQbht6-QgAG9U")

# Set up the model
generation_config = {
    "temperature": 0.95,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["your are a fatima jinnah women university chatbot you have to answer any question related to university website the URL of website is https://www.fjwu.edu.pk/"]
  },
  {
    "role": "model",
    "parts": ["**Chatbot for Fatima Jinnah Women University**\n\n**Welcome to Fatima Jinnah Women University!**\n\nI am your virtual assistant, and I'm here to help you navigate our university website and provide any information you may need.\n\n**To ask me a question, simply type it in the chat box below. I'll do my best to provide a helpful response.**\n\n**Here are some examples of questions you can ask me:**\n\n* What is the university's admission process?\n* What academic programs are offered?\n* What are the tuition fees?\n* What is the university's location?\n* What are the university's contact details?\n\n**Please note that I am still under development, so I may not be able to answer all questions perfectly. However, I will continue to learn and improve over time.**\n\n**I look forward to assisting you with your university inquiries.**\n\n**To visit the university website, please click on the following link:**\n\nhttps://www.fjwu.edu.pk/"]
  },
])





@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    convo.send_message(message)  # Send the user's message to the model
    response = convo.last.text   # Retrieve the bot's response
    print(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
