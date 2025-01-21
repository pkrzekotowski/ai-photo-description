import os
from flask import Flask, request, render_template, send_file, url_for, flash
from werkzeug.utils import secure_filename
import openai
import pandas as pd
from io import StringIO, BytesIO
import base64
from werkzeug.utils import secure_filename
import uuid
from config import Config

# Validate configuration
Config.validate()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size
app.config['SECRET_KEY'] = os.urandom(24)

# In-memory storage for images
IMAGE_STORE = {}

def get_image_description(image_data):
    try:
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

        # Convert image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Generate a concise alt text for this image that would be suitable for screen readers. Focus on the key elements and actions in the image, maintaining accessibility best practices. Keep it under 100 characters when possible."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=150,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as api_error:
            print(f"API Error details: {str(api_error)}")
            raise

    except openai.AuthenticationError as auth_error:
        print(f"Authentication error details: {str(auth_error)}")
        raise ValueError(f"Invalid OpenAI API key: {str(auth_error)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise Exception(f"Error calling OpenAI API: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return {'error': 'No files uploaded'}, 400

    files = request.files.getlist('files[]')
    descriptions = []
    errors = []

    for file in files:
        if file:
            try:
                # Read file into memory
                file_data = file.read()
                filename = secure_filename(file.filename)

                description = get_image_description(file_data)
                descriptions.append({
                    'filename': filename,
                    'description': description
                })
            except ValueError as ve:
                return {'error': str(ve)}, 401
            except Exception as e:
                errors.append(f"Error processing {filename}: {str(e)}")

    if errors and not descriptions:
        return {'error': errors[0]}, 500

    # Create CSV in memory
    df = pd.DataFrame(descriptions)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Generate unique filename
    unique_filename = f'photo_descriptions_{uuid.uuid4().hex[:8]}.csv'

    # Convert to BytesIO
    byte_buffer = BytesIO()
    byte_buffer.write(csv_buffer.getvalue().encode('utf-8'))
    byte_buffer.seek(0)

    return send_file(
        byte_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=unique_filename
    )

if __name__ == '__main__':
    app.run(debug=True)
