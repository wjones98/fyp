from Utils.Database import Database


class Upload:
    def __init__(self, file_id, file_name, user_id, content):
        self.user_id = user_id
        self.file_id = file_id
        self.file_name = file_name
        self.signal_type = content['SignalType']
        self.species = content['Species']
        self.gender = content['Gender']
        self.age = content['Age']
        self.target = content['Target']
        self.action = content['Action']
        self.device = content['Device']
        self.dataset_id = content['DataSetId']
        self.channel_count = content['ChannelCount']
        self.tags = content['Tags']

    def upload_file_metadata(self):
        query = f"""
                [metadata].[InsertFileMetaData] ?,?,?,?,?,?,?,?,?,?,?,?
                """
        params = (self.file_id, self.file_name, self.user_id, self.signal_type, self.species, self.gender,
                  self.age, self.target, self.action, self.device, self.dataset_id, self.channel_count)
        print(params)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
            response = {'Status': results['Status'], 'FileId': self.file_id, "Message": results['Message']}
        else:
            cursor.rollback()
            response = {'Status': results['Status'], 'FileId': self.file_id, "Message": results['Message']}
        conn.close()
        return response

    @staticmethod
    def create_dataset_metadata(dataset_id, dataset_name):

        query = f"""
                [metadata].[GetorInsertDataset] @DatasetName = ?, @DataSetId = ?
                """
        params = (dataset_name, dataset_id)
        conn = Database.connect()
        cursor = conn.cursor()
        response = Database.execute_sproc(query, params, cursor)
        if response['Status'] == 201:
            cursor.commit()
        conn.close()
        return response

    @staticmethod
    def upload_tags(dataset_id, key, value):
        query = f"""
                INSERT INTO
                    [metadata].[Tag]
                    ([DatasetId],[TagKey],[TagValue])
                VALUES
                    ('{dataset_id}','{key}','{value}')
                """
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    @staticmethod
    def init_file_path(file_id, file_path):
        query = f"""
                UPDATE 
                    [metadata].[FileHistory]
                SET
                    [FilePath] = '{file_path}'
                WHERE
                    [FileID] = '{file_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()

    @staticmethod
    def file_history_insert(user_id, file_info):

        query = f"""
                SELECT TOP 1 
                    [FileID]
                    ,[ProjectID]
                    ,[Change]
                FROM 
                    [MetaData].[metadata].[FileHistory]
                WHERE
                    [Filepath] = '{file_info["PreviousFilepath"]}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)

        for row in results:
            insert_query = f"""
                            INSERT INTO 
                                [metadata].[FileHistory]
                                ([FileID]
                                ,[UserID]
                                ,[ProjectID]
                                ,[Change]
                                ,[Filepath]
                                ,[Active]
                                ,[StartDate]
                                ,[EndDate]
                                ,[Previous]
                                ,[PreviousChange])
                            VALUES
                                ('{row[0]}','{user_id}','{row[1]}','{file_info['Change']}',
                                '{file_info['Filepath']}',1,GETDATE(),NULL,
                                '{file_info['PreviousFilepath']}','{row[2]}')
                            """
            Database.execute_non_query(insert_query, cursor)
            cursor.commit()
        conn.close()
        return {'Status': 201, 'Message': 'Change to file has been uploaded'}
