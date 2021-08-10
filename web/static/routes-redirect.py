routers = dict(
    BASE = dict(
        default_application='solver',
        default_controller='solver_web',
        default_function='_redirect',
        functions=[
            '_redirect',
            'randomizerWebService',
            'randomizerWebService.json'
        ]
    )
)
