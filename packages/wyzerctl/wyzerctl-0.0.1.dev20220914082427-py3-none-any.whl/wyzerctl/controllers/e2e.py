from cement import Controller, ex


class E2e(Controller):
    class Meta:
        label = 'e2e'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='list all e2e tests',
        arguments=[]
    )
    def list(self):
        pass

    @ex(
        help='run e2e tests',

        arguments=[
            (['-a', '--all'],
                {'help': 'Run all tests',
                 'dest': 'all'}),
        ]
    )
    def run(self):
        pass
