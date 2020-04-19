import json
from flask import request
from sandman2.service import Service


class DirectusService(Service):
    __json_collection_name__ = 'data'


    def get(self, resource_id=None):
        extra_args = {k: v for (k, v) in request.args.items() if k in ('meta', 'fields', 'offset')}
        request.args = dict(set(request.args.items()) - set(extra_args.items()))

        if 'offset' in extra_args:
           limit = request.args.get('limit', 100)
           request.args['page'] = int(int(extra_args['offset'])/int(limit)) + 1

        response = super().get(resource_id)
        if extra_args:
           out_dict = json.loads(response.get_data())
           out_dict.update(self._process_extra_args(extra_args))
           response.set_data(json.dumps(out_dict))
        return response
               

    def _process_extra_args(self, extra_args):
       out = dict()
       for k, v in extra_args.items():
          if k == "meta":
            out["meta"] = {"count" : 100, "total_count" : 100}
       return out
