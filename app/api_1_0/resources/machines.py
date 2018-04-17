from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from dateutil import parser
from .authentication import auth
from ... import db
from .users import user_fields
from ...models import Machine


active_revision_fields = {
    'id': fields.Integer,
    'cpu_make': fields.String,
    'cpu_name': fields.String,
    'cpu_socket': fields.String,
    'cpu_mhz': fields.Integer(default=None),
    'cpu_proc_cores': fields.Integer(default=None),
    'chipset': fields.String,
    'system_memory_gb': fields.Integer(default=None),
    'system_memory_mhz': fields.Integer(default=None),
    'gpu_name': fields.String,
    'gpu_make': fields.String,
    'gpu_memory_gb': fields.Integer(default=None),
    'revision_notes': fields.String,
    'revision_notes_html': fields.String,
    'pcpartpicker_url': fields.String,
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'uri': fields.Url('.revision', absolute=True)
}

machine_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'system_notes': fields.String,
    'owner': fields.String,
    'active_revision': fields.Nested(active_revision_fields),
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'uri': fields.Url('.machine', absolute=True),
    'user': fields.Nested(user_fields)
}

# machine_list_fields = {
#     'id': fields.Integer,
#     'system_name': fields.String,
#     'system_notes': fields.String,
#     'owner': fields.String,
#     'active_revision': fields.Nested(active_revision_fields),
#     'timestamp': fields.DateTime(dt_format='iso8601'),
#     'uri': fields.Url('.machine', absolute=True),
#     'user': fields.Nested(user_fields)
# }

# View subclass of Resource (which inherits from MethodView)
class MachineListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('system_name', type=str, required=True,
                                   help='No machine name provided',
                                   location='json')
        self.reqparse.add_argument('system_notes', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('owner', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('timestamp', type=str,
                                   location='json')
        super(MachineListAPI, self).__init__()

    @marshal_with(machine_fields, envelope='machines')
    def get(self):
        return Machine.query.order_by(Machine.timestamp.desc()).all()

    @auth.login_required
    @marshal_with(machine_fields, envelope='machine')
    def post(self):
        args = self.reqparse.parse_args()

        # parse the timestamp provided
        ts = None # set to none if not provided next
        if args['timestamp'] is not None:
            ts = parser.parse(args['timestamp'])

        machine = Machine(system_name=args['system_name'],
                          system_notes=args['system_notes'],
                          owner=args['owner'],
                          timestamp=ts,
                          author_id=g.user.id)

        db.session.add(machine)
        db.session.commit()
        return machine, 201


class MachineAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('system_name', type=str, location='json')
        self.reqparse.add_argument('system_notes', type=str, location='json')
        self.reqparse.add_argument('owner', type=str, location='json')
        self.reqparse.add_argument('timestamp', type=str,
                                   location='json')
        super(MachineAPI, self).__init__()

    @marshal_with(machine_fields)
    def get(self, id):
        return Machine.query.get(id)

    @auth.login_required
    @marshal_with(machine_fields, envelope='machine')
    def put(self, id):
        machine = Machine.query.get_or_404(id)

        # a little clever loop to go through all the args passed and
        # apply them to the newly instantiated Machine object
        # since the SQLAlchemy machine object does not support item
        # assignment, let's use some setattr func
        args = self.reqparse.parse_args()

        for k, v in args.items():
            if v is not None:
                # this is a hack because I couldn't get a built-in datetime parser
                # to work. This is bad and you should feel bad for reading it.
                if k == 'timestamp':
                    setattr(machine, k, parser.parse(v))
                else:
                    setattr(machine, k, v)
        # autocommit? This doesn't appear to be necessary---leaving in for now.
        db.session.commit()
        return machine

    @auth.login_required
    def delete(self, id):
        Machine.query.filter(Machine.id == id).delete()
        db.session.commit()
        return {'result': True}
