import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
import backend as bk

def test_extract_text_from_pdf_returns_string():
    from io import BytesIO
    from reportlab.pdfgen import canvas
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Test judgement text")
    c.save()
    buffer.seek(0)
    
    result = bk.extract_text_from_pdf(buffer)
    assert isinstance(result, str)
    assert len(result) > 0

def test_extract_text_from_url_returns_string():
    with patch('backend.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.text = "<html><body>Test judgement</body></html>"
        mock_get.return_value = mock_response
        
        result = bk.extract_text_from_url("https://example.com")
        assert isinstance(result, str)
        assert len(result) > 0

def test_summarize_judgement_returns_required_keys():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '''
    {
        "case_name": "Test vs Test",
        "court": "Supreme Court of India",
        "date": "2024-01-01",
        "facts": "Test facts",
        "issues": "Test issues",
        "procedural_history": "Test history",
        "reasoning": "Test reasoning",
        "ratio_decidendi": "Test ratio",
        "judgement": "Test judgement"
    }
    '''
    with patch('backend.get_groq_client') as mock_client:
        mock_client.return_value.chat.completions.create.return_value = mock_response
        result = bk.summarize_judgement("test text")
            
    required_keys = ["case_name", "court", "date", "facts", 
                     "issues", "procedural_history", "reasoning", 
                     "ratio_decidendi", "judgement"]
    for key in required_keys:
        assert key in result