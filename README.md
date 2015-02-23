# jira_import_export
Export and import process from one JIRA to another JIRA

1. Go to JIRA Administration and go to Manage Add-ons and find the Xporter plugin by Xpand IT.

NOTE: This process was developed exporting from JIRA v5.2.11#854-sha1:ef00d61 using Xporter plugin version 2.9.8, and importing into JIRA v6.3.15#6346-sha1:dbc023d

2. Load '<path_to_repo>/xporter_template.rtf' into your Xporter plugin.

3. Setup the Xporter plugin to have access to all the Projects, Issues, and Users that you wish to export. NOTE: this UI is a bit janky, be sure that you hit "Save" after each change to lock in the permissions. 

4. Exit Administration. Go to the Issue explorer and search for just the project you wish.  You search could look like:

project = TEST

The export UI won't show up to allow for an export unless all the issues in the search output have permissions. Go back to step 3 if the "Xporter" menu doesn't show up on the menu bar.

5. Open the Xporter UI by clicking menu item Xporter > Export Filter Results.

6. Setup the options as such:
Template: xporter_template.rtf
Export type: RTF
Break pages: unchecked

7. Hit export. The more issues you have the longer this will take. An RTF file will be downloaded.

NOTE: The xporter_template is only setup to export MAX 15 comments per issue. If someone wants to make this script grow its Comment MAX to be the maximum number of comments that will be exported in one issue, go nuts :) That would definitely make this more rock solid.

8. Load your RTF file into a text editor. Make the file Plain Text and save it out as a CSV file, i.e. TEST.csv

NOTE: This process was developed using TextEdit working on a MacBook Air running OS X 10.8.5. 

9. Run 'python <path_to_repo>/export_scrub.py <csv_filename>', which should write out 2 files. 

For example, 'python ~/export_scrub.py ~/Downloads/TEST.csv' will output:
~/Downloads/TEST_scrubbed.csv
~/Downloads/TEST_excel.csv

<csv_filename>_scrubbed.csv will be the file with any double quotes within comments turned into single quotes. This is done so JIRA can read and import the file and preserve line breaks. 

<csv_filename>_excel.csv will remove all commas from the file and turn the pipes into commas so that Microsoft Excel can read it. This is for testing to see where bad issues are (See Step 16)

10. Go to JIRA you are importing into and goto Administration > System > External System Import, and click Import from CSV.

11. Load the *_scrubbed.csv file in as the CSV source file. 

12. Check the "Use an existing configuration file" checkbox and load the '<path_to_repo>/csv_import_configuration.txt' file in as the configuration file. 

13. Change the CSV delimiter to '|', and hit Next.

14. Make sure the Import to Project radio box has "Defined in CSV" selected. 

15. Set your user email domain name (configuration defaults that to @lindenlab.com), and make sure the date format is dd-MM-yyyy hh:mm:ss, then click Next.

16. No changes should be needed here. Click next to move forward. IF you cannot proceed past this point that means your columns are not hitting properly. The errors should give you a clue and the *_excel.csv helps visualize that.

(16B.) IF the importing JIRA does not have all the Status field options mapped, there will be a section where you need to map the unknown imported values to the new system. This is self explanatory, though be sure that all the values you use are in your workflow or the import will have errors. Click next to move forward when you are done.

After these steps the importing should begin. IF any tweaks were made a link to a new CSV configuration is provided when the import is done. IF any warnings or errors are displayed that don't make sense a link to a full log is provided. The logs are very comprehensive and should give you a clue as to what is wrong in your data.

PLEASE NOTE: This process is not perfect and has some flaws. Some of our issues had '|' characters in the issues and so I had to skip them in the search. This is what our search looked like:

project = TEST AND key != TEST-153 AND key != TEST-227 AND key != TEST-152

Also I left in Attachment data, which doesn't import/export well. You will see lots of warnings about attachments it can't find. Also there are several fields I left in that we don't use so that might also cause problems. 
