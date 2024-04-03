import SAST_api
import requests
import os
import sys
import yaml
import time

# Open the YAML file
with open('config_rep.yaml', 'r') as file:
    # Load the YAML contents
    config = yaml.safe_load(file)

SAST_username = config['SAST_username']
SAST_password = config['SAST_password']
SAST_auth_url = config['SAST_auth_url']
SAST_api_url = config['SAST_api_url']

def SAST_get_report(project_name, report_type, SAST_username, SAST_password, SAST_auth_url, SAST_api_url):
    try:
        # Get access token
        access_token = SAST_api.SAST_get_access_token(SAST_username, SAST_password, SAST_auth_url)
        if not access_token:
            raise Exception("Failed to obtain access token")
        
        # Get latest scan id
        scan_id = SAST_api.SAST_get_project_latest_scan_id(access_token, project_name, SAST_api_url)
        
        # Post report request
        report_id = SAST_api.SAST_post_report_request(access_token, scan_id, report_type, SAST_api_url)
        
        # Wait for report to be ready
        status = 0
        while status != 200:
            status = SAST_api.SAST_get_report_status(access_token, report_id, SAST_api_url,)
            time.sleep(1)

        # Construct report URL
        report_url = f"{SAST_api_url}/reports/sastScan/{report_id}"
        
        # Fetch report content
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(report_url, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status codes
        report_content = response.content
        
        # Save report to file
        report_filename = f"{project_name}_SAST_report.{report_type}"
        report_path = os.path.join(os.getcwd(), report_filename)
        with open(report_path, 'wb') as f:
            f.write(report_content)

        print("SAST report saved successfully.")
        return report_path

    except Exception as e:
        print(f"Exception: {e}")
        return ""

#################################################
# main code
######<###########################################
def main():
    if(len(sys.argv) < 3):
        print('usage: Create_sast_report <project_name> <format: PDF | XML | CSV>')
        exit()

    project_name = sys.argv[1]
    report_type = sys.argv[2]

    # optional report types - pdf or csv
    SAST_report_path = SAST_get_report(project_name, report_type, SAST_username, SAST_password, SAST_auth_url, SAST_api_url) 

    print('\n\n' + 'SAST report location:\n' + SAST_report_path)
  
if __name__ == '__main__':
   main()