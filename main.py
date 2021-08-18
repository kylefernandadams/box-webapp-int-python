from boxsdk import JWTAuth, Client

target_folder_name = 'Target_Folder'


def move_files(request):
    content_type = request.headers["Content-Type"]
    print('Found content type header: {0}'.format(content_type))

    # Get the form data from the POST request coming from the Box Webapp
    if content_type == 'application/x-www-form-urlencoded':
        form_data = request.form
        print('Form data: {0}'.format(form_data))

        if form_data and 'user_id' in form_data:
            user_id = form_data['user_id']
            print('Found user_id: {0}'.format(user_id))
        if form_data and 'folder_id' in form_data:
            current_folder_id = form_data['folder_id']
            print('Found folder_id: {0}'.format(current_folder_id))
        if form_data and 'auth_code' in form_data:
            auth_code = form_data['auth_code']
            print('Found auth_code: {0}'.format(auth_code))

        # Get the Box service account client
        auth = JWTAuth.from_settings_file('./box_config.json')
        client = Client(auth)

        service_account = client.user().get()
        print('Found Service Account with name: {0}, id: {1}, and login: {2}'.format(service_account.name,
                                                                                     service_account.id,
                                                                                     service_account.login))
        # Get the current user
        user = client.user(user_id=user_id).get(fields=['id', 'name', 'login'])
        print('Found current user with id: {0}, login: {1}, and name: {2}'.format(user.id, user.login, user.name))

        # Get the current folder
        current_folder = client.folder(folder_id=current_folder_id).get(fields=['id', 'name', 'parent'])
        print('Found current folder with id: {0}, name: {1}, and parent id: '.format(current_folder.id,
                                                                                     current_folder.name))
        # Get the parent folder
        parent_folder = client.folder(folder_id=current_folder.parent.id).get(fields=['id', 'name', 'type'])
        print('Found parent folder with id: {0} and name: {1}'.format(parent_folder.id, parent_folder.name))

        # Get the target folder
        parent_folder_items = client.folder(folder_id=parent_folder.id).get_items(limit=None, offset=0, marker=None,
                                                                                  use_marker=False, sort=None,
                                                                                  direction=None,
                                                                                  fields=['id', 'name', 'type'])
        for item in parent_folder_items:
            print('Found item with type: {0}, id: {1}, and name: {2}'.format(item.type, item.id, item.name))
            if item.type == 'folder' and item.name == target_folder_name:
                print('Found target folder with id: {0} and name: {1}'.format(item.id, item.name))
                target_folder_id = item.id

        # Loop through parent folder items and move each to the target folder
        target_folder = client.folder(folder_id=target_folder_id).get(fields=['id', 'name', 'type', 'owned_by'])
        print('Found target folder with id: {0}, name: {1}, and owner login: {2}'.format(target_folder.id,
                                                                                         target_folder.name,
                                                                                         target_folder.owned_by.login))

        # Get target folder owner. This is needed to move the files since the target folder may not be owned by the user executing the Webapp Integration
        target_folder_owner = client.user(user_id=target_folder.owned_by.id).get(fields=['id', 'name', 'login'])
        print('Found current user with id: {0}, login: {1}, and name: {2}'.format(target_folder_owner.id,
                                                                                  target_folder_owner.login,
                                                                                  target_folder_owner.name))

        # Get all of the items in the current folder
        current_folder_items = client.folder(folder_id=current_folder.id).get_items(limit=None, offset=0, marker=None,
                                                                                    use_marker=False, sort=None,
                                                                                    direction=None,
                                                                                    fields=['id', 'name', 'type'])

        # Loop through all of the items and move them to the target folder
        for item in current_folder_items:
            print('Found item with type: {0}, id: {1}, and name: {2}'.format(item.type, item.id, item.name))
            if item.type == 'file':
                file_to_move = client.file(file_id=item.id)
                file_to_move.move(target_folder)
            elif item.type == 'folder':
                folder_to_move = client.folder(folder_id=item.id)
                folder_to_move.move(target_folder)

    return 'Successfully Submitted Files for Review', 200
