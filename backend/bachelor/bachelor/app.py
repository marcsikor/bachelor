from flask import Flask, request, jsonify
from firebase_admin import credentials, auth, firestore, storage, initialize_app
from flask_cors import CORS
from .email_logic.send_email import send_email #import send_email
from .storage_cred import STORAGE_ADDRESS # storage address link
from google.cloud.firestore_v1.base_query import FieldFilter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://tu.bedzia.moja.struna.com"]}})

cred = credentials.Certificate("./firebase-auth/firebase-token.json") # firebase app credentials

initialize_app(cred, {'storageBucket': STORAGE_ADDRESS})
db = firestore.client()

@app.route('/')
def hello():
    return "I'm alive!"

@app.route('/register-user', methods = ['POST'])
def register_user():
    data = request.json
    user_allowed = False
    existing_users = (
        db.collection("users")
        .where(filter=FieldFilter("email", "==", data.get('email')))
        .stream()
    )
    for doc in existing_users: # only one doc should be present in the database
        user_allowed = True
        user_data = doc.to_dict()
        break
    if user_allowed:
        if len(data.get('email')) > 0 and len(data.get('password')) > 0:
            user = auth.create_user(
                email = data.get('email'),
                password = data.get('password')
            )
            # print(user.uid)
            auth.set_custom_user_claims(user.uid, {'function': user_data['position']})
            # print(auth.get_user(user.uid).custom_claims.get('function'))
            return f'Successfully registered user: {user.email}' 
        else:
            return 'Error: Wrong data'

@app.route('/add-report', methods = ['POST']) # make amount with 2 decimal places
def add_report():
    data = request.form.to_dict()
    try:
        if 'file' in request.files:
            file = request.files['file']
            blob = storage.bucket().blob(file.filename)
            blob.upload_from_file(file, content_type=file.content_type)
            data['file'] = blob.public_url
    except Exception as e:
        print(str(e))
        return 'Issue occured while adding new report: ' + e
    data['createdDate'] = firestore.SERVER_TIMESTAMP
    data['confirmed'] = False
    data['approved'] = False
    data['payout'] = False
    update_time, data_ref = db.collection("user_reports").document(data['userUid']).collection("reports").add(data)
    return f"Added document with id {data_ref.id}"

@app.route('/get-list', methods = ['POST'])
def get_list():
    data = request.json
    data = db.collection("user_reports").document(data['userUid']).collection("reports").where(filter=FieldFilter("confirmed", "==", False)).stream()
    response = []
    for doc in data:
        response.append(dict(id = doc.id, paymentName = doc.to_dict()['paymentName'], amount = doc.to_dict()['amount'], currentPaymentType = doc.to_dict()['currentPaymentType'], file = doc.to_dict()['file'], invoiceNumber = doc.to_dict()['invoiceNumber']))
    return jsonify(response)

@app.route('/get-confirmed-list', methods = ['POST'])
def get_confirmed_list():
    data = request.json
    data = db.collection("user_reports").document(data['userUid']).collection("reports").where(filter=FieldFilter("confirmed", "==", True )).where(filter=FieldFilter("approved", "==", False )).stream()
    response = []
    for doc in data:
        response.append(dict(id = doc.id, paymentName = doc.to_dict()['paymentName'], amount = doc.to_dict()['amount'], currentPaymentType = doc.to_dict()['currentPaymentType'], file = doc.to_dict()['file'], invoiceNumber = doc.to_dict()['invoiceNumber']))
    return jsonify(response)

@app.route('/get-approved-list', methods = ['POST'])
def get_approved_list():
    data = request.json
    data = db.collection("user_reports").document(data['userUid']).collection("reports").where(filter=FieldFilter("approved", "==", True)).where(filter=FieldFilter("payout", "==", False)).stream()
    response = []
    for doc in data:
        response.append(dict(id = doc.id, paymentName = doc.to_dict()['paymentName'], amount = doc.to_dict()['amount'], currentPaymentType = doc.to_dict()['currentPaymentType'], file = doc.to_dict()['file'], invoiceNumber = doc.to_dict()['invoiceNumber']))
    return jsonify(response)

@app.route('/get-history', methods = ['POST'])
def get_history():
    data = request.json
    data = db.collection("user_reports").document(data['userUid']).collection("reports").where(filter=FieldFilter("payout", "==", True)).stream()
    response = []
    for doc in data:
        response.append(dict(id = doc.id, paymentName = doc.to_dict()['paymentName'], amount = doc.to_dict()['amount'], currentPaymentType = doc.to_dict()['currentPaymentType'], file = doc.to_dict()['file'], invoiceNumber = doc.to_dict()['invoiceNumber']))
    return jsonify(response)

@app.route('/get-report',  methods = ['POST'])
def get_report():
    data = request.json
    # print(data)
    firebase_data = db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).get()
    # print(firebase_data.to_dict())
    return firebase_data.to_dict()

@app.route('/add-user', methods = ['POST'])
def add_user():
    data = request.json
    no_email = True
    existing_users = (
        db.collection("users")
        .where(filter=FieldFilter("email", "==", data.get('email')))
        .stream()
    )
    for doc in existing_users: # only one doc should be present in the database
        no_email = False
    if no_email:
        data['superadmin'] = False
        update_time, data_ref = db.collection("users").add(data)
        send_email(data.get('email'), 'new-user') 
        return f"Added user with id {data_ref.id}"
    else: 
        # print('user not added')
        return "User already in database"

@app.route('/update-report', methods = ['POST'])
def update_report():
    data = request.form.to_dict()
    docId = data['docId']
    del data['docId']
    try:
        if 'file' in request.files:
            file = request.files['file']
            blob = storage.bucket().blob(file.filename)
            blob.upload_from_file(file, content_type=file.content_type)
            data['file'] = blob.public_url
    except Exception as e:
        print(str(e))
        return 'Issue occured while updating report: ' + e
    data['createdDate'] = firestore.SERVER_TIMESTAMP
    db.collection("user_reports").document(data['userUid']).collection("reports").document(docId).update(data)
    return f"Updated document with id {docId}"

@app.route('/list-users')
def list_users():
    data = db.collection("users").where(filter=FieldFilter("superadmin", "!=", True)).stream()
    response = []
    for doc in data:
        response.append(dict(id = doc.id, email = doc.to_dict()['email'], position = doc.to_dict()['position'], name = doc.to_dict()['name'], surname = doc.to_dict()['surname']))
    return jsonify(response)

@app.route('/delete-user', methods = ['POST'])
def delete_user():
    data = request.json
    db.collection("users").document(data['docId']).delete()
    try:
        user = auth.get_user_by_email(data['email'])
        # doc = db.collection("user_reports").document(user.uid).get()
        # if doc.exists:
        #     db.collection("user_reports").document(user.uid).delete()
        auth.delete_user(user.uid)
    except auth.UserNotFoundError:
        print('No user set yet')
    return f"Deleted user with uid {user.uid}"

@app.route('/delete-report', methods = ['POST'])
def delete_report():
    data = request.json
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).delete()
    return f"Deleted report with id {data['docId']}"

@app.route('/get-user/<doc_id>')
def get_user(doc_id):
    data = db.collection("users").document(doc_id).get()
    return data.to_dict()

@app.route('/update-user-access', methods = ['POST'])
def update_user_access():
    data = request.json
    try:
        user = auth.get_user_by_email(data['email'])
        auth.set_custom_user_claims(user.uid, {
            'function': data['position']
        })
    except auth.UserNotFoundError:
        print('Password not yet set for the user')
    db.collection("users").document(data['docId']).update({"position": data['position']})
    return f"Updated user with doc id {data['docId']}"

@app.route('/get-prep-list')
def get_prep_list():
    user_list = db.collection("users").stream()
    response = []
    for doc in user_list:
        user = auth.get_user_by_email(doc.to_dict()['email'])
        report_list = (
            db.collection("user_reports").document(user.uid).collection("reports")
            .where(filter=FieldFilter("confirmed", "==", True))
            .where(filter=FieldFilter("payout", "==", False))
            .order_by("approved")
            .order_by("createdDate")
            .stream()
            )
        for report in report_list:
            processed_report = report.to_dict()
            # print(processed_report)
            processed_report['userEmail'] = doc.to_dict()['email']
            processed_report['userUid'] = user.uid
            processed_report['docId'] = report.id
            response.append(processed_report)
    return jsonify(response)

@app.route('/get-prep-history')
def get_prep_history():
    user_list = db.collection("users").stream()
    response = []
    for doc in user_list:
        user = auth.get_user_by_email(doc.to_dict()['email'])
        report_list = (
            db.collection("user_reports").document(user.uid).collection("reports")
            .where(filter=FieldFilter("payout", "==", True))
            .stream()
            )
        for report in report_list:
            processed_report = report.to_dict()
            # print(processed_report)
            processed_report['userEmail'] = doc.to_dict()['email']
            processed_report['userUid'] = user.uid
            processed_report['docId'] = report.id
            response.append(processed_report)
    return jsonify(response)

@app.route('/confirm-report', methods = ['POST'])
def confirm_report():
    data = request.json
    # print(data)
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).update({'confirmed': True})
    return f"Confirmed report with id {data['docId']}"

@app.route('/revert-report', methods = ['POST'])
def revert_report():
    data = request.json
    # print(data)
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).update({'confirmed': False})
    return f"Reverted report with id {data['docId']}"

@app.route('/approve-report', methods = ['POST']) # email
def approve_report():
    data = request.json
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).update({'approved': True})
    user = auth.get_user(data['userUid'])
    send_email(user.email, 'approved', data['paymentName']) 
    return f"Approved report with id {data['docId']}"

@app.route('/reject-report', methods = ['POST']) # email
def reject_report():
    data = request.json
    # print(data)
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).update({'approved': False})
    user = auth.get_user(data['userUid'])
    send_email(user.email, 'rejected', data['paymentName'])
    return f"Rejected report with id {data['docId']}"

@app.route('/payout-report', methods = ['POST']) # email
def payout_report():
    data = request.json
    # print(data)
    db.collection("user_reports").document(data['userUid']).collection("reports").document(data['docId']).update({'payout': True})
    user = auth.get_user(data['userUid'])
    send_email(user.email, 'payout', data['paymentName'])
    return f"Paid out report with id {data['docId']}"