Welcome to the API Fortress Command Line Tool!

The tool, or rather, pair of tools, are designed to reduce the amount of legwork that goes into executing or uploading API Fortress tests. The following readme will explain each part of the process.

From the command line interface:

# PULL

Pull allows us to execute tests on the platform and do things with that data. We can run tests via API either in an authenticated or unauthenticated state. By passing credentials, we receive a more verbose test result. We can output this result to a file. We also have access to all of the standard options that API Fortress provides in its API (silent run, dry run, etc.)

## PULL EXECUTION FLAGS

/- **RA** - RUN ALL - This will execute all of the tests in a chosen project.
/- **RT** - RUN BY TAG - This will execute all tests with a selected tag (requires the -t flag to set tag) 
/- **RI** - RUN BY ID - This will execute a test with a specific ID (requires the -i flag to set id)
/- **H** - HOOK - This is the webhook of the project you are working with.

ex: to run all of the tests in a specific project, we would use the following command string:

**python pull.py -H http://mastiff.apifortress.com/yourWebHook -RA**

## PULL OPTION FLAGS

* - **\\-f** - FORMAT - This will determine the format of the test result output (JSON, JUnit, Bool)
* - **\\-S** - SYNC - This will provide a response body with the result of the test.
* - **d** - DRY - This will cause the test run to be a dry run.
* - **s** - SILENT - This will cause the test to run in silent mode. 
* - **o** - OUTPUT - This will write the result of the test to a local file. You must provide the path to the file to be created. Remember your filetype! (.json/.xml)
* - **c** - CONFIG - This provides the path to a configuration file which can provide webhooks and user credentials.
* - **C** - CREDENTIALS - This allows you to manually pass user credentials (username:password)
* - **t** - TAG - This is how you pass a tag for RUN BY TAG mode.
* - **i** - ID - This is how you pass an ID for RUN BY ID mode.
* - **k** - KEY - This is how you pass a key to reference in a configuration file.

# CONFIGURATION FILE

A configuration file is a YAML file that is formatted as follows:

hooks:
  - key: cool_proj1
    url: https://mastiff.apifortress.com/app/api/rest/v3/A_WEBHOOK
    credentials:
      username: (your username)
      password: (your password)
  - key: uncool_proj
    url: https://mastiff.apifortress.com/app/api/rest/v3/ANOTHER_WEBHOOK
    credentials:
      username: (another username)
      password: (another password)

Once you create a configuration file, you can pass the path with **c** and the key to the data you wish to pass with **k**.
