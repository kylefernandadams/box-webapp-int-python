# Box Webapp Integration Example
This project contains a [Box Webapp Integration](https://developer.box.com/guides/applications/web-app-integrations/) example the leverages the [Box Python SDK](https://github.com/box/box-python-sdk) to move files in one folder to another. This style of use case may be needed when an external collaborator uploads all necessary files and want to submit or acknowledge that all of the pertinent files have been uploaded

## Pre-Requisites
1. Signup for a [Box Developer](https://account.box.com/signup/n/developer) account.
2. Clone this github repo.

## Sever-side Deployment Instructions
1. Create a [Box JWT application](https://developer.box.com/guides/authentication/jwt/jwt-setup/), rename the JWT config file to box_config.json, and place it in the root directory of this project.
> Note: You may swap out the JWT implementation for three-legged OAuth 2.0. There is no hard requirement to use JWT.  

2. Updated the [target_folder_name](https://github.com/kylefernandadams/box-webapp-int-python/blob/master/main.py#L3) variable with the name of a folder on the same level as the one that the Webapp Integration will be invoked.
3. Deploy the python script to your IaaS of choice. Below is an example of deploying to Google Cloud Functions, however this can be deployed to any IaaS platform that supports python.
4. A REST endpoint will be provided once deployed. Save this for use in the following section.
5. Continue to the Webapp Integration Configuration instructions.

## Box Webapp Integration Configuration
1. Create a new [Webapp Integration](https://developer.box.com/guides/applications/web-app-integrations/configure/).
2. Provide a name that will show up as the right-click or context mention action.
3. Change the Integration scope to `The parent folder of the file/folder from which this integration is invoked`
4. Change the Integration Type to `Folders`
5. In the Callback Configuration section, set the Client Callback URL with URL provided in the previous section
6. Add a prompt message that will be presented to the user.
4. Select User experience option to `The integration will run server-side only`. You may change this if you like. If using a new window, you can leverage callback parameters such as `redirect_to_box_url`
5. In the Callback Parameters section, Add the following GET parameters:
* Method = Post, Parameter Name = user_id, Parameter Value = #user_id#
* Method = Post, Parameter Name = folder_id, Parameter Value = #file_id#
6. Save your changes
7. Navigate to your test folder, open the context menu, and click on your newly created Webapp Integration.


## Disclaimer
This project is a collection of open source examples and should not be treated as an officially supported product. Use at your own risk. If you encounter any problems, please log an [issue](https://github.com/kylefernandadams/box-webapp-int-python/issues).

## License

The MIT License (MIT)

Copyright (c) 2021 Kyle Adams

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
