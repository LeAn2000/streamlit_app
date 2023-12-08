import firebase_admin
from firebase_admin import credentials, firestore
class MyOwnFirebase:
    def __init__(self):
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate("firebase_sdk.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection = "PredictStock"

    def getDocumentData(self, docName):
        doc_ref = self.db.collection(self.collection).document(docName)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return dict()


