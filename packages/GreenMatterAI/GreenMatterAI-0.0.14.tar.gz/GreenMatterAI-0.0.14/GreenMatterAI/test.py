import GreenMatterAI as gm

# WebRenderClient
gmai = gm.GMAI(task='alfalfa',
             access_key_id='AKIARHSIRLVR5DV2PY42',
             secret_access_key='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')

# web_render_client
'''gmai = gm.GMAI(task='render-alfalfa',
             access_key_id='AKIARAOYKX7WG5QEPUPT',
             secret_access_key='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')'''
'''gmai = gm.GMAI(task='get_parameters',
             access_key_id='AKIARAOYKX7WG5QEPUPT',
             secret_access_key='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')'''

# folder_path can be omitted if blender file does not have any external dependencies
#gmai.upload_blend_file(blend_file_path='./alfalfa.blend', folder_path='assets')

gmai._download_results(2, s3_prefix='alfalfa/1acc7431-a86a-4a3c-9ac3-ad11df560166')

'''gmai.get_params()

parameters = {
    "min_distance": 0.15,
    "min_density": 0.4,
    "max_density": 1.0,
    "min_num_branches": 3,
    "max_num_branches": 20
}

labels = ['bounding_boxes_per_plant', 'bounding_boxes_per_branch', 'segmentation_masks']

gmai.render(nr_imgs_to_render=5,
            nr_return_imgs=4,
            parameters=parameters,
            labels=labels)'''
