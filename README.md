# Document-Management
Authenticated users can upload, download and share his/her documents.

I used __python 3.10__ version for this project. <br>
__requirements.txt__ file is created under the __document_management__ folder.<br>
Also, __document-Management.postman_collection.json__ file is created under the __document_management__ folder.<br>
1.First create virtual environment using this command: <br>
***py -3.10 -m venv [your virtual_environment_name]***<br>
2. Activate virtual environment<br>
***[virtual_environment_name]/scripts/activate***<br>
3. Go to document_management folder and then run this command (make sure your current folder has __requirements.txt__ file):<br>
***pip install -r requirements.txt***<br>
4. Then run this command (make sure your current folder has __manage.py__ file)<br>
***py manage.py runserver***<br>

You can test all APIs using __Postman__ <br>
All API endpoints are properly documented using __Swagger__.<br>

**USERS**<br>
**__api/users/__** <br>
Anyone can get the list of all users using this API. I have created this API to get users __UID__ only for testing other __APIs__. <br>
**__api/users/register/__**<br>
User can register with this API.<br>
**__api/users/login/__** <br>
User can login with __email__ and __password__ and get __jwt_token__.<br>

**Documents**<br>
**__api/documents/__**<br>
Authenticated user can upload and get all of his/her document list.<br>
**__api/documents/<uuid:document_uid>/__**<br>
Authenticated user can retrieve, update and delete his/her document.<br>
**__api/documents/<uuid:document_uid>/download/__**<br>
Authenticated user can download his/her document list.<br>
**__api/documents/share/__**<br>
Authenticated user can share and get his/her shared document list.<br>
**__api/documents/receive/__**<br>
Authenticated user can get of all the documents shared with him.<br>
