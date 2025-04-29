import requests
from bs4 import BeautifulSoup
import json

def get_results(roll, year, exam_type):
    try:
        # BTEB results endpoint
        url = "https://btebresultszone.com/results"
        
        # Headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        # Form data
        data = {
            'roll': str(roll),
            'year': str(year),
            'exam_type': exam_type
        }
        
        # Make POST request
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        
        # Parse HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract results (modify selectors based on actual website structure)
        result_data = {
            'gpa': soup.find('div', {'class': 'result-gpa'}).text.strip() if soup.find('div', {'class': 'result-gpa'}) else 'N/A',
            'status': soup.find('div', {'class': 'result-status'}).text.strip() if soup.find('div', {'class': 'result-status'}) else 'N/A',
            'success': True
        }
        
        return result_data
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error processing results: {str(e)}"
        }

# Test function
if __name__ == "__main__":
    test_result = get_results(roll="123456", year="2023", exam_type="diploma")
    print(json.dumps(test_result, indent=2))