from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <div style='text-align:center; padding-top:50px; font-family:Arial;'>
        <h1 style='color:#0078D4;'>🚀 DevOps Pipeline Optimization System Live!</h1>
        <p>Managed by: Vishal, Satyam & Rohit</p>
        <p>Status: <b>Application Successfully Deployed via Azure & Docker</b></p>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)