import datetime

from flask import jsonify, make_response
from run import app
from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    with app.app_context():
        all_actors = Actor.query.all()
        actors = []
        for actor in all_actors:
            act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            actors.append(act)
        response_body = jsonify(actors)
        response = make_response(response_body, 200)
    return response, actors


def get_actor_by_id():
    """
    Get record by id
    """
    with app.app_context():
        # data = get_request_data()
        data = {'name': 'Megan Fox', 'gender': 'female', 'id': 15,
                'date_of_birth': datetime.datetime(1986, 5, 16, 0, 0)}
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)

            obj = Actor.query.filter_by(id=row_id).first()
            try:
                actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            return make_response(jsonify(actor), 200)

        else:
            err = 'No id specified'
            return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    # data = get_request_data()
    ### YOUR CODE HERE ###
    with (app.app_context()):
        data = {'name': 'Harry Potter', 'gender': 'male', 'id': 19, 'date_of_birth': '02.05.1990'}
        try:
            if 'name' not in data or 'gender' not in data or 'id' not in data or 'date_of_birth' not in data:
                err = 'Can not add record because of missed field'
                print(err)
                return make_response(jsonify(error=err), 400)
            # if isinstance(data['date_of_birth'], str):
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except:
                err = 'Wrong format of date'
                print(err)
                return make_response(jsonify(error=err), 400)
            try:
                new_record = Actor.create(**data)
                print(new_record)
                new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
                print(new_actor)
                return make_response(jsonify(new_actor), 200)
            except:
                err = 'User with this id is alredy exists'
                print(err)
                return make_response(jsonify(error=err), 400)
        except:
            err = 'Last except'
            print(err)
            return make_response(jsonify(error=err), 400)


def update_actor():
    """
    Update actor record by id
    """
    # data = get_request_data()
    ### YOUR CODE HERE ###
    with (app.app_context()):
        data = {'name': 'Sugar Pig', 'gender': 'male', 'id': '116', 'date_of_birth': '04.11.1991'}
        if all(i in ACTOR_FIELDS for i in data):
            try:
                row_id = int(data['id'])
            except:
                err = 'ID must be an integer'
                return make_response(jsonify(error=err), 400)
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except:
                err = 'Wrong date format'
                print('wrong date format')
                return make_response(jsonify(error=err), 400)
            try:
                #exist = Actor.query.filter_by(id=row_id).first()
                upd_record = Actor.update(row_id, **data)
                upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
                return make_response(jsonify(upd_actor), 200)
            except:
                err = 'Actor with this id does not exist'
                print(err)
                return make_response(jsonify(error=err), 400)
        else:
            err = 'Wrong fields'
            print(err)
            return make_response(jsonify(error=err), 400)

def delete_actor():
    """
    Delete actor by id
    """
    #data = get_request_data()
    with (app.app_context()):
        data = {'name': 'Sugar Pig', 'gender': 'male', 'id': '24', 'date_of_birth': '04.11.1991'}
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'ID must be an integer'
                return make_response(jsonify(error=err), 400)
            obj = Actor.query.filter_by(id=row_id).first()
            if obj:
                Actor.delete(row_id)
                msg = 'Record successfully deleted'
                return make_response(jsonify(message=msg), 200)
            else:
                err = 'User with id does not exist'
                print(err)
                return make_response(jsonify(error=err), 400)
        else:
            err = 'Wrong fields'
            print(err)
            return make_response(jsonify(error=err), 400)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    #data = get_request_data()
    ### YOUR CODE HERE ###
    with (app.app_context()):
        data = {'actor_id': '2', 'movie_id': '1'}
        if 'actor_id' in data.keys() and 'movie_id' in data.keys():
            try:
                row_id = int(data['actor_id'])
                relation_id = int(data['movie_id'])
            except:
                err = 'ID must be an integer'
                #print(err)
                return make_response(jsonify(error=err), 400)
            movie = Movie.query.filter_by(id=relation_id).first()
            #print(movie)
            if not movie:
                err = 'Movie with such ids does not exist'
                #print(err)
                return make_response(jsonify(error=err), 400)
            actor_exist = Actor.query.filter_by(id=row_id).first()
            #print(movie)
            if not actor_exist:
                err = 'Actor with such ids does not exist'
                #print(err)
                return make_response(jsonify(error=err), 400)
            try:
                actor = Actor.add_relation(row_id, movie)
                #print(actor)
                rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
                rel_actor['filmography'] = str(actor.filmography)
                return make_response(jsonify(rel_actor), 200)
            except:
                err = 'This relation is already exist'
                #print(err)
                return make_response(jsonify(error=err), 400)
        else:
            err = 'Such actors or movies ids does not exist'
            #print(err)
            return make_response(jsonify(error=err), 400)

if __name__ == '__main__':
    # print(get_all_actors())
    # print(get_actor_by_id())
    # print(add_actor())
    # print(update_actor())
    #print(delete_actor())
    print(actor_add_relation())
    #print(add_actor())

# def add_actor():
#     """
#     Add new actor
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     new_record =
#     new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
#     return make_response(jsonify(new_actor), 200)
#     ### END CODE HERE ###
#
#
# def update_actor():
#     """
#     Update actor record by id
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     upd_record =
#     upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
#     return make_response(jsonify(upd_actor), 200)
#     ### END CODE HERE ###
#
#
# def delete_actor():
#     """
#     Delete actor by id
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     msg = 'Record successfully deleted'
#     return make_response(jsonify(message=msg), 200)
#     ### END CODE HERE ###
#
#
# def actor_add_relation():
#     """
#     Add a movie to actor's filmography
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     actor =  # add relation here
#     rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
#     rel_actor['filmography'] = str(actor.filmography)
#     return make_response(jsonify(rel_actor), 200)
#     ### END CODE HERE ###
#
#
# def actor_clear_relations():
#     """
#     Clear all relations by id
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     actor =  # clear relations here
#     rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
#     rel_actor['filmography'] = str(actor.filmography)
#     return make_response(jsonify(rel_actor), 200)
#     ### END CODE HERE ###
