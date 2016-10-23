import os
from flask_restful import Api
from . import api_blueprint
from ..api_1_0.resources.users import UserAPI
from ..api_1_0.resources.authentication import TokenAPI
from ..api_1_0.resources.machines import MachineAPI, MachineListAPI
from ..api_1_0.resources.revisions import RevisionAPI, RevisionListAPI, MachineRevisionListAPI
from ..api_1_0.resources.cinebenchr15results import \
                CinebenchR15ResultAPI, CinebenchR15ResultListAPI, RevisionCinebenchR15ResultListAPI
from ..api_1_0.resources.futuremark3dmark06results import \
                Futuremark3DMark06ResultAPI, Futuremark3DMark06ResultListAPI, RevisionFuturemark3DMark06ResultListAPI
from ..api_1_0.resources.futuremark3dmarkresults import \
                Futuremark3DMarkResultAPI, Futuremark3DMarkResultListAPI, RevisionFuturemark3DMarkResultListAPI


api = Api(api_blueprint)

api.add_resource(UserAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
api.add_resource(TokenAPI, '/token', endpoint='token')
api.add_resource(MachineListAPI, '/machines', endpoint='machines')
api.add_resource(MachineAPI, '/machines/<int:id>', endpoint='machine')
api.add_resource(RevisionListAPI, '/revisions', endpoint='revisions')
api.add_resource(RevisionAPI, '/revisions/<int:id>', endpoint='revision')
api.add_resource(MachineRevisionListAPI, '/machines/<int:id>/revisions', endpoint='machine_revisions')
api.add_resource(CinebenchR15ResultListAPI, '/cinebenchr15results', endpoint='cinebenchr15results')
api.add_resource(CinebenchR15ResultAPI, '/cinebenchr15results/<int:id>', endpoint='cinebenchr15result')
api.add_resource(RevisionCinebenchR15ResultListAPI, '/revisions/<int:id>/cinebenchr15results',
                 endpoint='revision_cinebenchr15results')
api.add_resource(Futuremark3DMark06ResultListAPI, '/futuremark3dmark06resultsresults',
                 endpoint='futuremark3dmark06results')
api.add_resource(Futuremark3DMark06ResultAPI, '/futuremark3dmark06results/<int:id>',
                 endpoint='futuremark3dmark06result')
api.add_resource(RevisionFuturemark3DMark06ResultListAPI, '/revisions/<int:id>/futuremark3dmark06results',
                 endpoint='revision_futuremark3dmark06results')
api.add_resource(Futuremark3DMarkResultListAPI, '/futuremark3dmarkresultsresults',
                 endpoint='futuremark3dmarkresults')
api.add_resource(Futuremark3DMarkResultAPI, '/futuremark3dmarkresults/<int:id>',
                 endpoint='futuremark3dmarkresult')
api.add_resource(RevisionFuturemark3DMarkResultListAPI, '/revisions/<int:id>/futuremark3dmarkresults',
                 endpoint='revision_futuremark3dmarkresults')
