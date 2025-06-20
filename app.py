from flask import Flask, render_template, request, jsonify, send_file
from chatbot_logic import get_bot_response
import analytics
import report_generator
import traceback
import os 

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response, success = get_bot_response(user_input)
    analytics.log_search(user_input, response, success)
    return jsonify({'response': response})

@app.route('/analytics')
def analytics_route():
    try:
        data = analytics.get_analytics()
        return jsonify(data)
    except Exception as e:
        print("Analytics Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/download_report')
def download():
    pdf_path = report_generator.create_report()
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
