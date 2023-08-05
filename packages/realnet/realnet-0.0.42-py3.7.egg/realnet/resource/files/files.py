import mimetypes

from flask import jsonify
from realnet.resource.items.items import Items

class Files(Items):
    
    def get_endpoint_name(self):
        return 'files'

    def get(self, module, args, path=None, content_type='text/html'):
        if path == 'upload-url':
            attributes = dict()
            attributes['filename'] = args.get('filename', 'file.tmp')
            attributes['filesize'] = args.get('size', 0)
            content_type = mimetypes.guess_type(attributes['filename'].lower())[0]
            if not content_type:
                if attributes['filename'].lower().endswith('heic'):
                    content_type = 'image/heic'
                else:
                    content_type = 'application/octet-stream'
            
            arguments = dict()
            typename = 'File'
            if content_type.startswith('image/'):
                typename = 'Image'
            elif content_type.startswith('application/pdf') or content_type.startswith('text/plain') or attributes['filename'].endswith('.md'):
                typename = 'Document'
                if attributes['filename'].endswith('.md'):
                    content_type = 'text/markdown'
            elif content_type.startswith('text/html'):
                typename = 'Page'
            elif content_type.startswith('video/'):
                typename = 'Video'
            elif content_type.startswith('application/zip') or content_type.startswith('application/x-zip-compressed'):
                typename = 'File'
            elif content_type.startswith('text/csv'):
                typename = 'File'
            elif attributes['filename'].endswith('.glb'):
                typename = 'Scene'
            
            attributes['content_type'] = content_type
            arguments['type'] = args.get('type', typename)
            parent_id = args.get('parent_id', None)
            if parent_id:
                parent_item = module.get_item(parent_id)
                if parent_item and module.can_account_write_item(module.get_account(), parent_item):
                    arguments['parent_id'] = parent_id
            
            arguments['ip_address'] = args.get('ip_address', None)
            for key, value in args.items():
                if not key in {'filename', 'file_size', 'parent_id', 'type', 'size', 'ip_address'}:
                    attributes[key] = value
            
            arguments['name'] = attributes['filename']
            arguments['attributes'] = attributes
            item = module.create_item(**arguments)
            if item:
                return module.get_data_upload_url(item.id)

        return self.render_item(module, args, path, content_type)

    def post(self, module, args, path=None, content_type='text/html'):
        if path == 'upload-confirm':
            item_id = args.get('item_id', None)
            filename = args.get('filename', None)
            filesize = args.get('size', None)
            content_type = mimetypes.guess_type(filename.lower())[0]

            if not content_type:
                if filename.lower().endswith('heic'):
                    content_type = 'image/heic'
                else:
                    content_type = 'application/octet-stream'
            
            item = module.get_item(item_id)
            if item:
                # todo get from S3
                attributes = dict(item.attributes)
                attributes['filename'] = filename
                attributes['content_type'] = content_type
                attributes['content_length'] = filesize
                attributes['mime_type'] = content_type
                
                for (key,value) in args.items():
                    if not key in {'filename', 'file_size', 'parent_id', 'type', 'size', 'ip_address'}:
                        attributes[key] = value

                module.update_item(item.id, **{"attributes": attributes})

                return jsonify(item.to_dict()), 200        
            # module.create_item(**args)
        if 'add' in args:
            del args['add']
        return self.render_item(module, args, path, content_type)