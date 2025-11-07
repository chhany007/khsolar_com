"""
Netlify Function to run Streamlit app
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def handler(event, context):
    """
    Netlify function handler for Streamlit app
    
    Note: This is a simplified handler. For full Streamlit functionality,
    consider using Streamlit Cloud, Render.com, or Hugging Face Spaces.
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>KHSolar - Deployment Notice</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 600px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                }
                h1 {
                    color: #667eea;
                    margin-bottom: 20px;
                    font-size: 2.5em;
                }
                .icon {
                    font-size: 4em;
                    margin-bottom: 20px;
                }
                p {
                    color: #555;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }
                .notice {
                    background: #fff3cd;
                    border: 2px solid #ffc107;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                }
                .alternatives {
                    text-align: left;
                    margin: 20px 0;
                }
                .alternatives h3 {
                    color: #667eea;
                    margin-bottom: 10px;
                }
                .alternatives ul {
                    list-style: none;
                    padding: 0;
                }
                .alternatives li {
                    padding: 10px;
                    margin: 5px 0;
                    background: #f8f9fa;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }
                .alternatives strong {
                    color: #667eea;
                }
                .btn {
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 12px 30px;
                    border-radius: 25px;
                    text-decoration: none;
                    margin: 10px 5px;
                    transition: all 0.3s;
                }
                .btn:hover {
                    background: #764ba2;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">☀️</div>
                <h1>KHSolar</h1>
                <p><strong>Solar Planning & Business Software</strong></p>
                
                <div class="notice">
                    <h3>⚠️ Deployment Notice</h3>
                    <p>KHSolar is a Streamlit Python application that requires a Python runtime server.</p>
                    <p>Netlify is optimized for static sites and serverless functions, which has limitations for full Streamlit apps.</p>
                </div>
                
                <div class="alternatives">
                    <h3>🚀 Recommended Hosting Platforms:</h3>
                    <ul>
                        <li><strong>Hugging Face Spaces</strong> - Free unlimited hosting, best for Streamlit</li>
                        <li><strong>Render.com</strong> - Free tier with custom domains</li>
                        <li><strong>Streamlit Cloud</strong> - Native Streamlit hosting (1 free app)</li>
                        <li><strong>Railway.app</strong> - $5/month free credit</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px; color: #888; font-size: 0.9em;">
                    For full deployment instructions, see <code>NETLIFY_DEPLOYMENT.md</code> in the repository.
                </p>
                
                <a href="https://github.com/chhany007/khsolar" class="btn">View on GitHub</a>
            </div>
        </body>
        </html>
        '''
    }
