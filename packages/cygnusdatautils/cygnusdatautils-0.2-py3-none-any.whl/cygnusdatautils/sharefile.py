import json
import http.client as httplib
import os
import mimetypes
import time
import urllib.parse as urlparse


class Cysharefile():

    def __init__(self, hostname, client_id, client_secret, username, password):
        '''
        This class is used to connect to sharefile
        :param hostname: URL of the sharefile
        :param client_id: client_id of the sharefile API
        :param client_secret: client secret of the shahrefile API
        :param username: username of sharefile login
        :param password: password of sharefile API
        '''

        self.hostname = hostname
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    @staticmethod
    def get_authorization_header(token):
        return {'Authorization': 'Bearer %s' % (token['access_token'])}

    @staticmethod
    def get_hostname(token):
        return '%s.sf-api.com' % (token['subdomain'])

    def authenticate(self):
        '''
        Authenticate the credentials and get a token from sharefile API
        :return: (string) token
        '''
        hostname = self.hostname
        client_id = self.client_id
        client_secret = self.client_secret
        username = self.username
        password = self.password
        uri_path = '/oauth/token'
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        params = {'grant_type':'password'
                        , 'client_id':client_id
                        , 'client_secret':client_secret
                        , 'username':username
                        , 'password':password}
        http = httplib.HTTPSConnection(hostname)
        http.request('POST'
                        , uri_path, urlparse.urlencode(params)
                        , headers=headers)
        response = http.getresponse()
        token = None
    #     print(response.read())
        if response.status == 200:
            token = json.loads(response.read())
            self.token = token
            self.valid_token = True
            self.TOKEN_CREATION_TIME = time.time()
        else:
            self.token = None
            self.valid_token = False

        http.close()
        return token

    @staticmethod
    def get_dir_list(token, get_children=True, fid="allshared"):
        """ Get the root level Item for the provided user. To retrieve Children the $expand=Children
        parameter can be added.

        Args:
        dict json token acquired from authenticate function
        boolean get_children - retrieve Children Items if True, default is False"""

        uri_path = '/sf/v3/Items({})'.format(fid)
        if get_children:
            uri_path = '%s?$expand=Children' % (uri_path)
        #     print ('GET %s%s'%(get_hostname(token), uri_path))
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('GET', uri_path, headers=Cysharefile.get_authorization_header(token))
        response = http.getresponse()

        #     print (response.status, response.reason)
        items = json.loads(response.read())
        #     print (items['Id'], items['CreationDate'], items['Name'])
        context = {"id": items['Id']}
        all_children = []
        if 'Children' in items:
            children = items['Children']
            for child in children:
                #             print(child['Id'], items['CreationDate'], child['Name'])
                all_children.append([child['Id'], items['CreationDate'], child['Name']])
        context["children"] = all_children
        return context

    @staticmethod
    def download_item(token, item_id, local_path):
        """ Downloads a single Item. If downloading a folder the local_path name should end in .zip.

        Args:
        dict json token acquired from authenticate function
        string item_id - the id of the item to download
        string local_path - where to download the item to, like "c:\\path\\to\\the.file" """

        uri_path = '/sf/v3/Items(%s)/Download' % (item_id)
        # print('GET %s%s' % (get_hostname(token), uri_path))
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('GET', uri_path, headers=Cysharefile.get_authorization_header(token))
        response = http.getresponse()
        location = response.getheader('location')
        redirect = None
        if location:
            redirect_uri = urlparse.urlparse(location)
            redirect = httplib.HTTPSConnection(redirect_uri.netloc)
            redirect.request('GET', '%s?%s' % (redirect_uri.path, redirect_uri.query))
            response = redirect.getresponse()

        with open(local_path, 'wb') as target:
            b = response.read(1024 * 8)
            while b:
                target.write(b)
                b = response.read(1024 * 8)

        # print(response.status, response.reason)
        http.close()
        if redirect:
            redirect.close()

    @staticmethod
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    @staticmethod
    def multipart_form_post_upload(url, filepath):
        """ Does a multipart form post upload of a file to a url.

        Args:
        string url - the url to upload file to
        string filepath - the complete file path of the file to upload like, "c:\path\to\the.file

        Returns:
        the http response """

        #     print(url)

        newline = b'\r\n'
        filename = os.path.basename(filepath)
        data = []
        headers = {}
        boundary = '----------%d' % int(time.time())
        headers['content-type'] = 'multipart/form-data; boundary=%s' % boundary
        data.append(('--%s' % boundary).encode('utf-8'))
        data.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % ('File1'
                                                                                   , filename)).encode('utf-8'))
        data.append(('Content-Type: %s' % Cysharefile.get_content_type(filename)).encode('utf-8'))
        data.append(('').encode('utf-8'))
        data.append(open(filepath, 'rb').read())
        data.append(('--%s--' % boundary).encode('utf-8'))
        data.append(('').encode('utf-8'))
        data_str = newline.join(data)
        headers['content-length'] = len(data_str)
        uri = urlparse.urlparse(url)
        http = httplib.HTTPSConnection(uri.netloc)
        http.putrequest('POST', '%s?%s' % (uri.path, uri.query))
        for hdr_name, hdr_value in headers.items():
            http.putheader(hdr_name, hdr_value)
        http.endheaders()
        http.send(data_str)
        return http.getresponse()

    @staticmethod
    def upload_file(token, folder_id, local_path):
        """ Uploads a File using the Standard upload method with a multipart/form mime encoded POST.

        Args:
        dict json token acquired from authenticate function
        string folder_id - where to upload the file
        string local_path - the full path of the file to upload, like "c:\\path\\to\\file.name" """

        uri_path = '/sf/v3/Items(%s)/Upload' % (folder_id)
        #     print ('GET %s%s'%(get_hostname(token), uri_path))
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('GET', uri_path, headers=Cysharefile.get_authorization_header(token))

        response = http.getresponse()
        upload_config = json.loads(response.read())
        # print(upload_config)
        if 'ChunkUri' in upload_config:
            upload_response = Cysharefile.multipart_form_post_upload(upload_config['ChunkUri'], local_path)
            # print("\t\t\t\t", upload_response.status, upload_response.reason)
            # print("\t\t\t\t", upload_response.read())
        else:
            print('No Upload URL received')

    @staticmethod
    def delete_file(token, fid):
        #     https://account.sf-api.com/sf/v3/Items(id)

        uri_path = '/sf/v3/Items(%s)' % (fid)
        #     print ('GET %s%s'%(get_hostname(token), uri_path))
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('DELETE', uri_path, headers=Cysharefile.get_authorization_header(token))
        response = http.getresponse()
        # print(response.read())
        return response

    @staticmethod
    def get_item_by_id(token, item_id):
        """ Get a single Item by Id.
        Args:
        dict json token acquired from authenticate function
        string item_id - an item id """
        uri_path = '/sf/v3/Items(%s)' % (item_id)
        #     print('GET %s%s'%(get_hostname(token), uri_path))
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('GET', uri_path, headers=Cysharefile.get_authorization_header(token))
        response = http.getresponse()
        #     print(response.status, response.reason)
        dd = response.read()
        items = json.loads(dd)
        parent_id = "allshared" if "Parent" not in items else items["Parent"]["Id"]
        to_return = [items['Id'], items['CreationDate'], items['Name'], parent_id]
        #     print(dd)
        return to_return

    @staticmethod
    def create_folder(token, parent_id, name, description):
        """ Create a new folder in the given parent folder.

        Args:
        dict json token acquired from authenticate function
        string parent_id - the parent folder in which to create the new folder
        string name - the folder name
        string description - the folder description """

        uri_path = '/sf/v3/Items(%s)/Folder' % (parent_id)
        #     print 'POST %s%s'%(get_hostname(token), uri_path)
        folder = {'Name': name, 'Description': description}
        headers = Cysharefile.get_authorization_header(token)
        headers['Content-Type'] = 'application/json'
        http = httplib.HTTPSConnection(Cysharefile.get_hostname(token))
        http.request('POST', uri_path, json.dumps(folder), headers=headers)
        response = http.getresponse()

        # print(response.status, response.reason)
        new_folder = json.loads(response.read())
        # print('Created Folder %s' % (new_folder['Id']))
        # print(new_folder)
        http.close()

        return new_folder['Id']

    def get_credentials(self):
        return self.hostname, self.client_id, self.client_secret, self.username, self.password

    def update_token_if_expired(self):
        '''
        Sharefile token expires after some time, call this function if you suspect the token is expired
        :return:
        '''
        current_time = time.time()
        TOKEN_CREATION_TIME = self.TOKEN_CREATION_TIME
        diff = current_time - TOKEN_CREATION_TIME

        if diff / 3600 > 1:
            TOKEN = self.authenticate()
            return TOKEN

    def get_dir_list_wrapper(self, get_children=True, fid="allshared"):
        '''
            Get the root level Item for the provided user. To retrieve Children the $expand=Children
            parameter can be added.
        :param get_children: Boolean. Default: True. get the list of subfolders also
        :param fid: String. Default: allshared. Folder ID of the folder whose list needed to be fetched
        :return: list of children folders
        '''
        TOKEN = self.token
        return self.get_dir_list(TOKEN, get_children, fid)

    def download_item_wrapper(self, item_id, local_path):
        """ Downloads a single Item. If downloading a folder the local_path name should end in .zip.

           Args:
           string item_id - the id of the item to download
           string local_path - where to download the item to, like "c:\\path\\to\\the.file" """

        TOKEN = self.token
        Cysharefile.download_item(TOKEN, item_id, local_path)

    def upload_file_wrapper(self, folder_id, local_path):
        """ Uploads a File using the Standard upload method with a multipart/form mime encoded POST.

        Args:
        string folder_id - where to upload the file
        string local_path - the full path of the file to upload, like "c:\\path\\to\\file.name" """
        TOKEN = self.token
        Cysharefile.upload_file(TOKEN, folder_id, local_path)

    def delete_file_wrapper(self, file_id):
        '''
        Delete a file from Sharefile
        :param file_id: ID of file to be deleted
        :return:
        '''
        TOKEN = self.token
        Cysharefile.delete_file( TOKEN, file_id)

    def get_item_by_id_wrapper(self, file_id):
        """ Get a single Item by Id.
        Args:
        string item_id - an item id """
        TOKEN = self.token
        return Cysharefile.get_item_by_id(TOKEN, file_id)

    def create_folder_wrapper(self, parent_id, name, description):
        """ Create a new folder in the given parent folder.

        Args:
        string parent_id - the parent folder in which to create the new folder
        string name - the folder name
        string description - the folder description """
        TOKEN = self.token
        return Cysharefile.create_folder(TOKEN, parent_id, name, description)
