
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import WyzerctlError
from .controllers.base import Base
from .controllers.e2e import E2e

# configuration defaults
CONFIG = init_defaults('wyzerctl')
CONFIG['wyzerctl']['foo'] = 'bar'


class Wyzerctl(App):
    """Wyzerctl primary application."""

    class Meta:
        label = 'wyzerctl'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            E2e,
            Base,
        ]


class WyzerctlTest(TestApp, Wyzerctl):
    """A sub-class of Wyzerctl that is better suited for testing."""

    class Meta:
        label = 'wyzerctl'


def main():
    with Wyzerctl() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except WyzerctlError as e:
            print('WyzerctlError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
