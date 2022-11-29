import boto3
import imghdr
import six
import base64
import uuid
import io
import csv
import os

from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from app import db
from app.models import User, Collection, Item, Image
from app.main import bp
from werkzeug.utils import secure_filename


# get file extension
def get_file_extension(file_name, decoded_file):
    # get file extension
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension

# decode base64 file
def decode_base64_file(data):
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.

        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        # complete the file name
        complete_file_name = "%s.%s" % (file_name, file_extension,)

        # return the decoded file and complete file name
        return io.BytesIO(decoded_file), complete_file_name


# uplaod base64 method
def upload_base64_file(base64_file):
    # AWS bucket name
    bucket_name = current_app.config['AWS_BUCKET_NAME']

    # file and file name
    file, file_name = decode_base64_file(base64_file)

    # set the boto3 client with IAM profile
    client = boto3.client('s3', aws_access_key_id=current_app.config['AWS_API_KEY'],
                          aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])

    # upload the object to S3
    client.upload_fileobj(
        file,
        bucket_name,
        file_name,
        ExtraArgs={'ACL': 'public-read'}
    )

    # return the file URL
    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"

# render index
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # return index template
    return render_template('index.html', title='Index')

# render dashboard
@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # get all collections for current user
    collections = current_user.get_collections().all()

    # get all items for current user
    items = current_user.get_items().all()
    
    # return dashboard template
    return render_template('dashboard.html', collections=collections, items=items, title='Dashboard')

# render create collection
@bp.route('/create_collection', methods=['GET', 'POST'])
@login_required
def create_collection():
    if request.method=='GET':
        # return create collection template
        return render_template('create_collection.html', title='create collection')
    else:
        # get form fields
        collection_visibility = request.form.get('collection_visibility')
        collection_title = request.form.get('collection_title')
        collection_desc = request.form.get('collection_desc')

        # create a collection object, add to session and commit
        collection = Collection(name=collection_title, description=collection_desc, visibility=collection_visibility, item_count =0, author=current_user)
        db.session.add(collection)
        db.session.commit()
        
        # redirect to dashboard
        return redirect(url_for('main.dashboard'))

# render create item
@bp.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if request.method=='GET':
        # get collections
        collections = current_user.get_collections().all()

        # return create item template
        return render_template('create_item.html', collections=collections, title='create item')
    else:
        # get form fields collection and item category
        collection_name = request.form.get('collection')
        item_category = request.form.get('category')

        # set defaults on collection and item category fields
        if collection_name == "Select Collection":
            collection_name = "Default Collection"

        if item_category == "Select Category":
            item_category = "Trading Cards"

        # get the rest of the form fields
        item_title = request.form.get('item_title')
        item_desc = request.form.get('item_desc')
        custom = request.form.get('hc')

        # create a collection object by collection by name
        collection = Collection.query.filter_by(name=collection_name).filter_by(user_id=current_user.id).first()
    
        # increase the collection object count
        collection.item_count += 1    
        
        # create an item object, add to the session and commit
        item = Item(name=item_title, description=item_desc, collection_name=collection_name, custom=custom, category=item_category, author=current_user, collection=collection)
        db.session.add(item)
        db.session.commit()
        
        # add collection to session and commit
        db.session.add(collection)
        db.session.commit()

        # iterate through the hidden keys to get the auto-generated images
        for key in request.form.keys():
            if key.startswith('img'):
                # create an image object, add to the session and commit
                image = Image(name=upload_base64_file(request.form.get(key)), author=current_user, collection=collection, item=item)
                db.session.add(image)
                db.session.commit()

        # re-direct to the dashboard
        return redirect(url_for('main.dashboard'))

# render collection details
@bp.route('/collection_details/<cid>')
def collection_details(cid):
    # create a collection object
    collection_record = Collection.query.get(cid)
    
    # check if collection is private
    if collection_record.visibility == 'Private':
        # if the current user is authenticated and the collection record belongs to the current user
        if current_user.is_authenticated and collection_record.user_id == current_user.id:
            # pasadena california
            pass
        else:
            # redirect to the index for private collections
            return redirect(url_for('main.index'))

    # get items by collection record id
    items = Item.query.filter_by(collection_id=collection_record.id).all()
    
    # create a user object
    user = User.query.get(collection_record.user_id)

    # init custom object
    r_items = []
    r_item = {}
    
    # iterate through the items records
    for item in items:
        # build the master object record with only the fields we want to display on an overview
        r_item["name"] = item.name
        r_item["id"] = item.id
        r_item["description"] = item.description

        # get the first item
        if Image.query.filter_by(item_id = item.id).first() is None:
            # set to default no-img
            r_item["images"] = "../static/images/no-img.jpg" 
        else:
            # set first item
            r_item["images"] = Image.query.filter_by(item_id = item.id).first().name 
        
        # append the items to the object and the object to the array
        r_items.append(r_item)
        r_item = {} 

    # render collection details
    return render_template('collection_details.html', collection=collection_record, master_obj=r_items, items=items, user=user, title='Collection Details')
    
# render item details
@bp.route('/item_details/<iid>')
def item_details(iid):
    # get the item record
    item_record = Item.query.get(iid)
    
    # redirect to the dashboard if there's no record
    if not item_record:
        # redirect to dashboard
        return redirect(url_for('main.dashboard'))

    # if item is private    
    if item_record.collection.visibility == "Private":
        # check if user is authenticated and the item record belongs to the current user
        if current_user.is_authenticated and item_record.user_id is current_user.id:
            pass
        else:
            # return to dashboard
            return redirect(url_for('main.dashboard'))
    
    # get the images associated to the item record
    images = Image.query.filter_by(item_id=item_record.id).all()

    # render the item details template
    return render_template('item_details.html', item=item_record, images=images, title='Item Details')

# render edit itme
@bp.route('/edit_item/<iid>', methods=['GET', 'POST'])
@login_required
def edit_item(iid):
    # get the item record
    item_record = Item.query.get(iid)
    if request.method=='GET':

        # if item is private    
        if item_record.collection.visibility == "Private":
            # check if user is authenticated and the item record belongs to the current user
            if current_user.is_authenticated and item_record.user_id is current_user.id:
                pass
            else:
                # return to dashboard
                return redirect(url_for('main.dashboard'))

        # if there is no item record, return to dashboard
        if not item_record:
            # redirect to dashboard
            return redirect(url_for('main.dashboard'))

        # get the images associated with this item record
        images = Image.query.filter_by(item_id=item_record.id).all()

        img_list = []

        # add the static no-img to the record if there are no images associated with this record
        if len(images) == 0:
            # append images
            img_list.append("../static/images/no-img.jpg")
        else:
            for i in images:
                img_list.append(i.name)

        # get all the current user collections
        collections = current_user.get_collections().all()

        # render the template
        return render_template('edit_item.html', item=item_record, images=img_list, collections=collections, iid=iid, title='Edit Item')

    else:
        new_arr = []
        for key in request.form.keys():
            if key.startswith('img'):
                if key.startswith('img-http'):
                    new_arr.append(request.form.get(key))
                else:
                    new_arr.append(upload_base64_file(request.form.get(key)))

        current_images = Image.query.filter_by(item_id=item_record.id).all()       
        cid = Collection.query.get(item_record.collection.id) 
        
        for ci in current_images:
            if ci.name not in new_arr:
                # delete from s3
                print("delete")
            db.session.query(Image).filter(Image.id==ci.id).delete()
            db.session.commit()
        
        for na in new_arr:
            item = Image(name=na, author=current_user, collection=cid, item=item_record)
            db.session.add(item)
            db.session.commit()

        collection_name = request.form.get('collection')
        if collection_name == "Select Collection":
            collection_name = "Default Collection"
        item_category = request.form.get('category')
        item_title = request.form.get('item_title')
        item_desc = request.form.get('item_desc')
        custom = request.form.get('hc')

        new_cid = Collection.query.filter_by(name=collection_name).filter_by(user_id=current_user.id).first()
        if collection_name is not cid.name:
            cid.item_count -= 1
            db.session.commit()
            new_cid.item_count += 1
            db.session.commit()
        else:
            pass

        item_record.name = item_title
        item_record.description = item_desc
        item_record.collection_name = collection_name
        item_record.custom = custom
        item_record.category = item_category
        item_record.collection=new_cid


        db.session.commit()
        return redirect(url_for('main.dashboard'))

# render profile
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method=='GET':
        return render_template('profile.html', title='Profile')
    else:
        username = request.form.get('username')
        email = request.form.get('email_address')
        
        emailuser = User.query.filter_by(email=email).first()
        if emailuser:
            if emailuser.email is current_user.email:
                pass
            else:
                flash('Email {} already exists.'.format(email))
                return redirect(url_for('main.profile'))
        current_user.username = username
        current_user.email = email
        
        if(request.form.get('hidden_profile_image') != ""):
            profile_image = upload_base64_file(request.form.get('hidden_profile_image'))
            current_user.profile_image = profile_image
        if(request.form.get('hidden_banner_image') != ""):
            banner_image = upload_base64_file(request.form.get('hidden_banner_image'))
            current_user.background_image = banner_image
        
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.profile'))

# render create options
@bp.route('/create_options')
@login_required
def create_options():
    return render_template('create_options.html', title='Create Item')
    
# render create multiple
@bp.route('/create_multiple', methods=['GET', 'POST'])
@login_required
def create_multiple():
    if request.method=='GET':
        return render_template('create_multiple.html', title='Create Items')
    else:
        uploaded_df = request.files['csv']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(current_app.config['CSV_LOCATION'], data_filename))
 
        # Storing uploaded file path in flask session
        data_file_path = os.path.join(current_app.config['CSV_LOCATION'], data_filename)

        input_file = csv.DictReader(open(data_file_path))
        
        for row in input_file:
            key_mapping = row.keys()
            if not row['Title (required)']:
                pass
            else: 
                # check to see if collection column exists, otherwise set to default
                collection = ''
                if not row['Collection']:
                    collection = 'Default Collection'
                else:
                    if row['Collection'] == 'Default':
                        collection = 'Default Collection'
                    else: 
                        collection = row['Collection']

                # query for the collection
                collection_request = Collection.query.filter_by(name=collection).filter_by(user_id=current_user.id).first()
                
                collection = collection_request

                # create a new collection if collection column doesn't exist
                if collection_request is None:
                    # create a new collection
                    collection = Collection(name=row['Collection'], description=row['Collection'], visibility='Private', item_count =0, author=current_user)
                    db.session.add(collection)
                    db.session.commit()

                # array to build custom object
                custom_arr = []

                # custom inner object
                custom_obj = {}

                # get custom attributes and create the custom object
                for k in key_mapping:
                    if k == 'Title (required)' or k == 'Item Description' or k == 'Collection':
                        continue
                    custom_obj[k] = row[k]
                    custom_arr.append(custom_obj)
                    custom_obj = {}


                # create the item record with pending
                print("title "+ row['Title (required)'])
                print("description "+ row['Item Description'])
                print("collection "+ row['Collection'])

                description = ''
                if row['Item Description'] is None:
                    description = row['Title (required)']
                else:
                    description = row['Item Description']

                # increase the collection object count
                collection.item_count += 1    
                
                # create an item object, add to the session and commit
                item = Item(name= row['Title (required)'], description=description, collection_name=row['Collection'], custom=custom_arr, category='Trading Cards', author=current_user, collection=collection)
                db.session.add(item)
                db.session.commit()
                
                # add collection to session and commit
                db.session.add(collection)
                db.session.commit()

                
        return redirect(url_for('main.dashboard'))
    