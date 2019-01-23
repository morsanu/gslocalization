import argparse

from models.ios_xliff_file import export_xliff_files, load_xliff_files
from cloud_managers.google_sheets_manager import GoogleSheetsManager

ap = argparse.ArgumentParser()
ap.add_argument('-x', '--xcodeproj_path', required=True, help='path to the Xcode project', metavar='\b')
ap.add_argument('-a', '--auth_file_path', required=True, help='path to the Google Sheets authorization JSON file', metavar='\b')
ap.add_argument('-e', '--email', required=True, help='email used for sharing newly created worksheets', metavar='\b')
ap.add_argument('-l', '--languages', required=True, help='list of language codes used for importing/exporting '
                                                         'localizations (comma separated)', metavar='\b')
ap.add_argument('-o', '--output_dir', required=True, help='output dir for saving the xliff files generated from Xcode', metavar='\b')

args = vars(ap.parse_args())

xcodeproj_path = args['xcodeproj_path']
loc_output_path = args['output_dir']
service_account_file = args['auth_file_path']
user_email = args['email']
localization_languages = args['languages'].split(',')

google_sheets_manager = GoogleSheetsManager(service_account_file, user_email)

# xliff_files = export_xliff_files(xcodeproj_path, localization_languages, loc_output_path)
xliff_files = load_xliff_files(localization_languages, loc_output_path)

for l_file in xliff_files:
    l_file.sync_with_google_sheets(gsheets_manager=google_sheets_manager)
    l_file.update_from_google_sheets(gsheets_manager=google_sheets_manager)
    if l_file.has_updates:
        l_file.import_in_xcode(xcodeproj_path=xcodeproj_path)