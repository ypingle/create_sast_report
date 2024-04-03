import requests

import requests

def SAST_get_access_token(SAST_username, SAST_password, SAST_auth_url):
    try:
        payload = {
            'scope': 'access_control_api sast_api',
            'client_id': 'resource_owner_sast_client',
            'grant_type': 'password',
            'client_secret': '014DF517-39D1-4453-B7B3-9930C563627C',
            'username': SAST_username,
            'password': SAST_password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(SAST_auth_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        print(f'get_SAST_access_token - token = {response.text}')
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Exception: get SAST access token failed: {e}")
        return ""

def SAST_get_projects(access_token, SAST_api_url):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        url = f'{SAST_api_url}/projects'

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        print('SAST_get_projects')
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Exception: SAST_get_projects: {e}")
        return ""
    
def SAST_get_project_ID(access_token, project_name, SAST_api_url):
    try:
        projects = SAST_get_projects(access_token, SAST_api_url)
        projId = next((project['id'] for project in projects if project['name'] == project_name), 0)
    except Exception as e:
        print(f"Exception: SAST_get_project_ID: {e}")
        return ""
    return projId

def SAST_get_project_latest_scan_id(access_token, project_name, SAST_api_url):
    try:
        projId = SAST_get_project_ID(access_token, project_name, SAST_api_url)
        if projId == 0:
            return 0
        
        url = f"{SAST_api_url}/sast/scans?projectId={projId}&last=1"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        response_json = response.json()
        lastScanId = response_json[0]['id']
    except Exception as e:
        print(f"Exception: SAST_get_project_latest_scan_id: {e}")
        return ""
    else:
        print(f'SAST_get_project_latest_scan_id scan_id= {lastScanId}')
        return lastScanId

def SAST_get_project_latest_scan_comment(access_token, project_name, SAST_api_url):
    try:
        projId = SAST_get_project_ID(access_token, project_name, SAST_api_url)
        if projId == 0:
            return ""

        url = f"{SAST_api_url}/sast/scans?projectId={projId}&last=1"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        response_json = response.json()
        comment = response_json[0].get('comment', '')
    except Exception as e:
        print(f"Exception: SAST_get_project_latest_scan_comment: {e}")
        return ""
    else:
        print(f"SAST_get_project_latest_scan_comment comment= {comment}")
        return comment

def SAST_post_report_request(access_token, sast_scan, report_type, SAST_api_url):
    url = f"{SAST_api_url}/reports/sastScan"

    try:
        payload = {
            "reportType": report_type,
            "scanId": sast_scan
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        response_json = response.json()
    except Exception as e:
        print(f"Exception: SAST_post_report_request: {e}")
        return ""
    else:
        return response_json.get('reportId', "")

def SAST_get_report_status(access_token, report_id, SAST_api_url):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        url = f"{SAST_api_url}/help/reports/sastScan/{report_id}/status"

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        status = response.status_code
    except Exception as e:
        print(f"Exception: SAST_get_report_status: {e}")
        return ""
    else:
        print('SAST_get_report_status')
        return status
