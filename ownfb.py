import firebase_admin
from firebase_admin import credentials, firestore, storage
class MyOwnFirebase:
    def __init__(self):
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate("firebase_sdk.json")
            firebase_admin.initialize_app(cred,{'storageBucket': 'streamlit-app-66a95.appspot.com'})
        self.db = firestore.client()
        self.collection = "PredictStock"
        self.bucketname = "streamlit-app-66a95.appspot.com"

    def getDocumentData(self, docName):
        doc_ref = self.db.collection(self.collection).document(docName)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return dict()
    def syncFile(self):
        for i in range(1,8):
            blob = storage.bucket(self.bucketname).blob(f"model_{i}.hdf5")
            blob.download_to_filename(f'model_{i}.hdf5')

