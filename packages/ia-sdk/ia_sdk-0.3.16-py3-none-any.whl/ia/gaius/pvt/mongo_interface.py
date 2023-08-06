import random
import pymongo
import json
from bson.objectid import ObjectId
from copy import deepcopy
import datetime
import io

class MongoDataRecords:
    def __init__(self, dataset_document_list, DR: float, DF: float, shuffle: bool):
        """
        Args:
            dataset_document_list (str or list, required): List of mongo ObjectIds to use as data records
            DR (float, required): fraction of total data to use for testing and training. 0 < DR < 100
            DF (float, required): fraction of the DR to use for training.  The rest of the DR is used for testing. 0 < DF < 100
            shuffle (bool, required): whether to shuffle the data when creating sets

            After creating the class, utilize the member variables `train_sequences` and `test_sequences` for the data sets

        :ivar train_sequences: the mongo documents to use for training
        :ivar test_sequences: the mongo documents to use for testing
        """
        DR = DR / 100
        DF = DF / 100
        
        if DR > 1 or DF > 1:
            raise Exception(f'Invalid value provided for DR or DF: {DR=}, {DF=}')
        
        try:
            if DR == 1 and DF == 1:
                self.train_sequences = dataset_document_list
                self.test_sequences = []
            else:
                if shuffle:
                    random.shuffle(dataset_document_list)

                num_files = len(dataset_document_list)
                num_use_files = int(num_files * DR)  ## use a fraction of the whole set

                num_train_sequences = int(num_use_files * DF)  ## train 2/3rds, test 1/3rd
                num_test_sequences = num_use_files - num_train_sequences

                self.train_sequences = dataset_document_list[:num_train_sequences]
                self.test_sequences = dataset_document_list[num_train_sequences:(num_train_sequences + num_test_sequences)]
        except Exception as exception:
            print(f'MongoDataRecords BROKE by {exception.args}')
            raise


class MongoData:
    """
        Analogous object to the Data class, but utilizes a MongoDB cursor instead of a directory to reference data records
        Start with a MongoDB document containing the name of all dataset files (located separately)
    
        Only retrieve actual data files when calling retrieveDataRecord. Overloaded iterator functions to allow treating of object
        as a list.
        
        Example: 
        
            .. code-block:: python

                >>> mongo = pymongo.MongoClient('mongodb://mongodb:27017/')
                >>> dataset_details = {"user_id": "ABCD1",
                                    "dataset_id": "iris_0_0_13"}
                >>> md = MongoData(mongo_dataset_details=dataset_details, 
                                mongo_db=mongo_db, 
                                data_files_collection_name='dataset_files')
                >>> md.prep(percent_of_dataset_chosen=50, 
                            percent_reserved_for_training=50, 
                            shuffle=True)
                >>> md.setIterMode('testing')
                >>> for record in md:
                ...
        
    """
    def __init__(self, mongo_dataset_details: dict, data_files_collection_name: str, mongo_db:pymongo.MongoClient):
        """Initialized dataset object from MongoDB

        Args:
            mongo_dataset_details (dict): _description_
            data_files_collection_name (str): _description_
            mongo_db (pymongo.MongoClient): _description_

        Raises:
            Exception: user_id field missing from mongo_dataset_details
            Exception: dataset_id field missing from mongo_dataset_details
            Exception: multiple datasets found pertaining to same user_id and dataset_id field
        """
        if not 'user_id' in mongo_dataset_details:
            raise Exception(f'user_id field missing from mongo_dataset_details ({mongo_dataset_details=})')
        if not 'dataset_id' in mongo_dataset_details:
            raise Exception(f'dataset_id field missing from mongo_dataset_details ({mongo_dataset_details=})')
            
        self._mongo_dataset_details = deepcopy(mongo_dataset_details)
        self._data_files_collection_name = deepcopy(data_files_collection_name)
        self.mongo_db = mongo_db
        
        # initialize iteration variables
        self._iter_mode = None
        self.__curr = None
        self.__term = None
        
        if not 'files' in self._mongo_dataset_details:
            dataset_obj = {'user_id':self._mongo_dataset_details['user_id'],
                       'dataset_id':self._mongo_dataset_details['dataset_id']}
            
            if mongo_db['datasets'].count_documents(dataset_obj) != 1:
                raise Exception(f'{mongo_db["datasets"].count_documents(dataset_obj)} dataset records found for {dataset_obj=}')
        
            dataset = mongo_db['datasets'].find_one(dataset_obj)
            
        self._mongo_dataset_details['files'] = [item for item in dataset['dataset']['files']]
        
        
        self.train_sequences = []
        self.test_sequences = []

    def prep(self, percent_of_dataset_chosen:float, percent_reserved_for_training:float, shuffle:bool=False):
        """Prepare the dataset

        Args:
            percent_of_dataset_chosen (float): The percent of the dataset to utilize
            percent_reserved_for_training (float): The training/testing split for the dataset (e.g. set to 80 for 80/20 trianing/testing split)
            shuffle (bool, optional): Whether to shuffle the data. Defaults to False.
        """
        data = [MongoDataRecords(deepcopy(self._mongo_dataset_details['files']), percent_of_dataset_chosen, percent_reserved_for_training, shuffle)]

        self.train_sequences = []
        self.test_sequences = []
        for d in data:
            self.train_sequences += d.train_sequences
            self.test_sequences += d.test_sequences
            
    
    def retrieveDataRecord(self, document_id: ObjectId):
        """Retrieve a data record from MongoDB, pertaining to the ObjectId specifed

        Args:
            document_id (ObjectId, required): data record to retrieve from mongo, located in the collection specified when calling :func:`__init__`
        

        Raises:
            Exception: Raised when MongoDB document is not found. Shows query performed that failed

        Returns:
            str: binary string depicting data sequence stored in MongoDB Document
        """
        query_dict = {'user_id': self._mongo_dataset_details['user_id'],
                      'dataset_id': self._mongo_dataset_details['dataset_id'],
                      '_id': document_id}
        
        record = self.mongo_db[self._data_files_collection_name].find_one(query_dict)
        if record is None:
            raise Exception(f'DataRecord {str(document_id)} not found using {query_dict=}')

        return record['file']

    def convertBinaryStringtoSequence(self, record):
        """Convert Binary string of multiple GDFs (delimited by newline) into a sequence of JSON objects

        Args:
            record (str, required): binary string of GDFs to convert

        Returns:
            list: list of GDFs in json format
        """
        try:
            lines = io.StringIO(record.decode('utf-8'))
            sequence = (tuple([json.loads(line.strip()) for line in lines]))
            return sequence
        except Exception as e:
            print(f'failed to retrieve record as StringIO: {e}')
        
    def getSequence(self, record):
        """Wrapper function to retrieve a record from MongoDB and convert it into a sequence

        Args:
            record (ObjectId): The MongoDB ObjectId of the data record to retrieve

        Returns:
            list: GDF sequence retrieved from MongoDB
        """
        return self.convertBinaryStringtoSequence(self.retrieveDataRecord(record))
    
    def setIterMode(self, mode:str):
        """Set mode to be used for iterating across dataset

        Args:
            mode (str): set to "training" or "testing" depending on what set of sequences is to be iterated across

        Raises:
            Exception: When no data is in train_sequences or test_sequences, and :func:`prep` should be called first
            Exception: When invalid mode specified in mode argument
        """
        if len(self.train_sequences) == 0 and len(self.test_sequences) == 0:
            raise Exception('no data in train_sequences or test_sequences, use prep first')
            
        if mode == 'training':
            
            self.__curr = 0
            self.__term = len(self.train_sequences)
            
        elif mode == 'testing':
            self.__curr = 0
            self.__term = len(self.test_sequences)
        else:
            raise Exception('setIterMode only supports "training" and "testing"')
        
        self._iter_mode = mode
        return
    
    def __iter__(self):
        return self

    def __next__(self):
        """Iterate across range, calling :func:`retrieveDataRecord` for each item
        """        
        if self.__curr >= self.__term:
            self.__curr = 0
            raise StopIteration()
            
        
        if self._iter_mode == 'training':
            (cur, self.__curr) = (self.train_sequences[self.__curr], self.__curr + 1)
        
        elif self._iter_mode == 'testing':
            (cur, self.__curr) = (self.test_sequences[self.__curr], self.__curr + 1)
        
        else: 
            raise Exception('invalid iter mode: {self._iter_mode}, set using setIterMode(mode)')

        return self.retrieveDataRecord(cur)


class MongoResults:
    """Class to handle saving and linking result data inside MongoDB. Provides functions to insert single log record during training/testing,
    save final result after test completion, and remediation/deletion function for test aborting, database cleanup
    """
    def __init__(self, mongo_db, result_collection_name: str, log_collection_name: str, test_id:str, user_id:str, dataset_id:str, test_configuration:dict=None):
        """Initialize MongoResults object

        Args:
            mongo_db (pymongo.MongoClient): Database where the results are to be stored
            result_collection_name (str): collection name to save final test results
            log_collection_name (str): collection name to save testing log documents
            test_id (str): unique-id for the test being conducted
            user_id (str): unique-id for the user conducting the test
            dataset_id (str): unique-id for the dataset being used in the test
            test_configuration (dict): object showing all of the options used for configuring pvt
        """
        
        self.mongo_db = mongo_db
        self.result_collection_name = result_collection_name
        self.log_collection_name = log_collection_name
        self.result_collection = mongo_db[result_collection_name]
        self.log_collection = mongo_db[log_collection_name]
        self.test_configuration = test_configuration
        self.result_obj = {'testing_logs': [],
                           'training_logs': [],
                           'test_id': test_id,
                           'user_id': user_id,
                           'dataset_id': dataset_id,
                           'start_time_utc' : str(datetime.datetime.utcnow()),
                           'test_configuration': self.test_configuration}
        
    def reset(self):
        """Reset start time and testing/training logs in result_obj
        """
        self.result_obj.update({'testing_logs': [],
                                'training_logs': [],
                                'start_time_utc' : str(datetime.datetime.utcnow())})
        return
    
    def addLogRecord(self, type:str, record:dict):
        """Called during the testing loop to insert a pvt status record into MongoDB

        Args:
            type (str): Whether the record should be appended to the training or testing logs
            record (dict): the record to insert

        Raises:
            Exception: Thrown if the type provided is not supported
        """
        
        record_id = self.log_collection.insert_one(record).inserted_id
        if type == 'training':
            self.result_obj['training_logs'].append(record_id)
        elif type == 'testing':
            self.result_obj['testing_logs'].append(record_id)
        else:
            raise Exception(f'Unsupported record type {type} for record {record}')
        
        return
    
    def saveResults(self, final_results:dict):
        """Save a document in MongoDB, linking the result doc to the logs documents

        Args:
            final_results (dict): Information pertaining to the results of the test, to be stored in the results object for future use

        Returns:
            str: string of the ObjectId saved in MongoDB
            
            
        Example:
            .. code-block:: python
            
                uid = mongo_results.saveResults(final_state)
        """
        self.result_obj['end_time_utc'] = str(datetime.datetime.utcnow())
        self.result_obj['final_results'] = final_results
        # print(f'{self.result_obj = }')
        result_id = self.result_collection.insert_one(self.result_obj).inserted_id
        print(f'saved test results in {self.result_collection_name} as id: {result_id}')
        return str(result_id)
    
    def deleteResults(self):
        """Function used to remediate database in the event of a failed/aborted test

        Returns:
            dict: dict showing the deleted result record, if any
        """
        try:
            delete_result = self.result_collection.find_one_and_delete({'user_id': self.result_obj['user_id'],
                                                            'dataset_id': self.result_obj['dataset_id'],
                                                            'test_id': self.result_obj['test_id'],
                                                            }, {'_id': False})
            # print(f'deleted_count = {delete_result}')
                # print(f'log_delete_result={log_delete_result}')
            
        except Exception as e:
            print(f'failed to delete results: {e}')
            return None
        
        try:
            for log_id in delete_result['training_logs']:
                log_delete_result = self.log_collection.find_one_and_delete({'_id':log_id},{'_id': False})
            for log_id in delete_result['testing_logs']:
                log_delete_result = self.log_collection.find_one_and_delete({'_id':log_id},{'_id': False})
        except Exception as e:
            print(f'failed to delete log record: {e}')
            return None
        return {'status': 'deleted', 'record': delete_result}