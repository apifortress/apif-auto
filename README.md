Welcome to the API Fortress Command Line Tool!

The tool, or rather, pair of tools, are designed to reduce the amount of legwork that goes into executing or uploading API Fortress tests. The following readme will explain each part of the process.

From the command line interface:

# APIF-RUN

Run allows us to execute tests on the platform and do things with that data. We can run tests via API either in an authenticated or unauthenticated state. By passing credentials, we receive a more verbose test result. We can output this result to a file. We also have access to all of the standard options that API Fortress provides in its API (silent run, dry run, etc.)

## RUN EXECUTION FLAGS

* **run-all** - RUN ALL - This will execute all of the tests in a chosen project.
* **run-by-tag** - RUN BY TAG - This will execute all tests with a selected tag (requires the -t flag to set tag) 
* **run-by-id** - RUN BY ID - This will execute a test with a specific ID (requires the -i flag to set id)
* **hook** - HOOK - This is the webhook of the project you are working with. This can be either an API Fortress URL, or the key from a configuration file (set the path to the config file with the **\-c** tag)

ex: to run all of the tests in a specific project, we would use the following command string:

**python apif-run.py run-all http://mastiff.apifortress.com/yourWebHook**

## RUN OPTION FLAGS

*  **\-f** - FORMAT - This will determine the format of the test result output (JSON, JUnit, Bool)
*  **\-S** - SYNC - This will provide a response body with the result of the test.
*  **\-d** - DRY - This will cause the test run to be a dry run.
*  **\-s** - SILENT - This will cause the test to run in silent mode. 
*  **\-o** - OUTPUT - This will write the result of the test to a local file. You must provide the path to the file to be created. Remember your filetype! (.json/.xml)
*  **\-c** - CONFIG - This provides the path to a configuration file which can provide webhooks and user credentials. If no path is specified, the program will look for a config.yml in the same directory as it is (./config.yml)
*  **\-C** - CREDENTIALS - This allows you to manually pass user credentials (username:password) **(SUPERSEDES CONFIG FILE)**
*  **\-t** - TAG - This is how you pass a tag for RUN BY TAG mode.
*  **\-i** - ID - This is how you pass an ID for RUN BY ID mode.

# APIF-PUSH

Push allows us to push tests into API Fortress. When tests are downloaded from the platform, they come as 2 XML files (unit.xml & input.xml). We can use this tool to push those files back to an API Fortress project, either individually or in bulk. 

## PUSH EXECUTION FLAGS

* **hook** - HOOK - This is the webhook of the project you are working with. This can be either an API Fortress URL, or the key from a configuration file (set the path to the config file with the **\-c** tag)

## PUSH OPTION FLAGS

* **\-p** - PATH - This provides the path to the test file you wish to upload. **You can pass multiple paths.**
* **\-r** - RECURSIVE - This flag will make the call recursive; It will dive through the directory passed with **-p** and grab every test in all of its subdirectories.
* **\-b** - BRANCH - This allows you to specify a Git branch that these test files are attached to. **Default is master.** 
*  **\-c** - CONFIG - This provides the path to a configuration file which can provide webhooks and user credentials. If no path is specified, the program will look for a config.yml in the same directory as it is (./config.yml)
*  **\-C** - CREDENTIALS - This allows you to manually pass user credentials (username:password) **(SUPERSEDES CONFIG FILE)**

# CONFIGURATION FILE

A configuration file is a YAML file that is formatted as follows:

```yaml
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
  - key: unauth_proj
    url: https://mastiff.apifortress.com/app/api/rest/v3/JUST_A_WEBHOOK_WITHOUT_CREDENTIALS
```

Once you create a configuration file, you can pass the path with **\-c** and the key to the data in place of the normal hook URL. If you also pass credentials, they'll override the credentials in the configuration file. If you don't include credentials in the config file, you can pass them manually or leave them out entirely. 

# EXAMPLES

Execute all of the tests in a project and output the results to a JUnit/XML file via an authenticated route:

**python apif-run.py run-all http://mastiff.apifortress.com/yourWebHook -S -C my@username.com:password1 -f junit -o some/route/results.xml**

Push all of the tests from a directory and all of its subdirectories to a project:

**python apif-push.py http://mastiff.apifortress.com/yourWebHook -C my@username.com:password1 -r -p some/directory/with/tests**

Execute one test in a project by ID, using a config file for credentials and webhook:

**python apif-run.py run-by-id config_key -c path/to/config/file -i testidhash8924jsdfiwef891**

# NOTES

* The order of the optional arguments passed does not matter.
* Remember, in a bash environment, anything that has a space in it needs to be wrapped in quotes. This goes for paths, filenames, etc. 