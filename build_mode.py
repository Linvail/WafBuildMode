from waflib.Configure import conf
from waflib.Build import BuildContext
from waflib import Options, Utils, Context
import os, sys

@conf
def get_all_modes(ctx):
    return Utils.to_list(getattr(Context.g_module, 'modes', []))

def _mode(ctx):
    modes = ctx.get_all_modes()

    default_mode = modes[0]
    mode = Options.options.mode or default_mode

    if mode == '?':
        Logs.info( 'Valid modes (* = default):' )
        for mode in sorted(modes):
            tag = '*' if mode == default_mode else ' '
            Logs.info( '%s %s' % (tag, mode) )
        sys.exit()

    if mode not in modes:
        ctx.fatal('Invalid mode \'%s\'.  Valid modes are %s' % (mode, ','.join(modes)))

    return mode

def _variant(ctx):
    if 'conf_check_' in ctx.top_dir:
        # Configuration time build contexts use a special directory named
        # conf_check_<hash> to build small test programs to figure out if
        # header files or other features are included.  We do not have and
        # cannot require a product and mode to be set for these so check for
        # a build in this directory and return an empty variant in this case.
        # We do not have a better way to know that the build context is being
        # created at configure time.
        return ''

    return os.path.join(Context.g_module.APPNAME, ctx.mode)

def _env_name(ctx):
    return Context.g_module.APPNAME + '-' + ctx.mode

def options(opt):
    group = opt.add_option_group('My Group')
    group.add_option('--mode', help='Build mode (type ? for list)')
    BuildContext.mode = property(_mode)
    BuildContext.variant = property(_variant)
    BuildContext._env_name = property(_env_name)

