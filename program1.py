from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import mysql.connector
app = Flask(__name__)

# Initialize the recognizer outside the route
recognizer = sr.Recognizer()

@app.route('/')
def hello_world():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/page3')
def page3():
    return render_template('page3.html')


@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/page5')
def page5():
    return render_template('page5.html')

@app.route('/page6')
def page6():
    return render_template('page6.html')



@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("\nPlease say something...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Listen for the audio input
            audio = recognizer.listen(source)

        print("Recognizing...")
        # Recognize the speech
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return jsonify({'result': text})
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
    return jsonify({'error': 'Speech recognition failed'})

recognizer = sr.Recognizer()
# Add a global variable to control speech recording
isRecording = False

@app.route('/process_audio1', methods=['POST'])
def process_audio1():
    global isRecording
    try:
        directory = request.json['directory']
        filename = request.json['filename']
        
        # Check if recording is already in progress
        if isRecording:
            return jsonify({'success': False, 'error': 'Recording already in progress'})

        # Start recording
        isRecording = True
        audio_data = []

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("\nPlease say something...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            
            # Listen for the audio input
            audio = recognizer.listen(source)
            
            # Recognize the speech
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            audio_data.append(text)

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Write the recognized text to a file
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as file:
            for line in audio_data:
                file.write(line + '\n')  # Write each line of recognized text to the file
        print("Note saved successfully to:", filepath)
        
        # Reset recording status
        isRecording = False
        
        return jsonify({'success': True, 'message': 'Note saved successfully'})
    
    except Exception as e:
        # Reset recording status on error
        isRecording = False
        return jsonify({'success': False, 'error': str(e)})

# Function to open the browser
def open_browser(url):
    # Open the default web browser with the specified URL
    webbrowser.open(url)
    print("Web browser opened successfully.")


@app.route('/process_audio2', methods=['POST'])
def process_audio2():
    try:
        response_data = {'success': True, 'message': 'Speech recognized successfully'}
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("\nPlease say something...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Listen for the audio input
            audio = recognizer.listen(source)

        print("Recognizing...")
        # Recognize the speech
        text = recognizer.recognize_google(audio)
        print("You said:", text)       

        # Check if the command to open a browser is present
        if "open browser" in text:
            print("What URL would you like to open?")
           
            # Use the default microphone as the audio source
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source)
                # Listen for the URL input
                audio_url = recognizer.listen(source)
                # Recognize the URL speech
                url = recognizer.recognize_google(audio_url)
                print("Opening", url)
                # Open the browser with the specified URL
                open_browser(url)
        return jsonify({'success': True, 'message': 'Speech recognized successfully'})
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return jsonify({'success': False, 'error': 'Speech recognition failed'})
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return jsonify({'success': False, 'error': str(e)})





# Route for text to speech conversion
@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data['text']

        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Set properties before adding anything to speak
        engine.setProperty('rate', 120)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

        # Pass the text to the engine
        engine.say(text)

        # Wait for the speech to finish
        engine.runAndWait()

        return jsonify({'success': True, 'message': 'Speech conversion successful'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



# MySQL database connection setup
db_config = {
    'user': 'root',
    'password': '',  # Use the password you set up for MySQL
    'host': 'localhost',
    'port': 3308, 
    'database': 'mca'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    comments = request.form['comments']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (name, email, rating, comments)
            VALUES (%s, %s, %s, %s)
        ''', (name, email, rating, comments))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Feedback received from {name} ({email}): Rating - {rating}, Comments - {comments}")
        return render_template('page7.html', name=name)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'success': False, 'error': str(err)})



if __name__ == '__main__':
    app.run(debug=True)
