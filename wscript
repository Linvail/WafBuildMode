from waflib import Configure, Context, Errors, Utils, Logs
from waflib.Configure import conf

APPNAME = 'LambdaPractice'
VERSION = '1.0'

top = '.'
out = 'build'

modes = ['debug', 'release']

def options(opt):
    opt.load('compiler_cxx')
    opt.load('build_mode', tooldir='.')

def configure(ctx):
    ctx.load('compiler_cxx')
    ctx.load('build_mode', tooldir='.')

    ctx.env.append_value('DEFINES', [
        'WIN32',
        '_WINDOWS',
        '_UNICODE',
        'UNICODE',
        '_CRT_SECURE_NO_DEPRECATE',
        '_CRT_NON_CONFORMING_SWPRINTFS',
        '_ENABLE_ATOMIC_ALIGNMENT_FIX'
    ])

    # the original variant should be an empty string
    Logs.info( "Original variant: %s" % ctx.variant )
    ctx.env.append_value('CXXFLAGS', ['/EHsc'])

    '''
    For debug build
    '''
    base_env = ctx.env
    ctx.setenv('%s-debug' % APPNAME, base_env)
    # the ctx.variant will be LambdaPractice-debug
    Logs.info( "Debug variant: %s" % ctx.variant )

    ctx.env.append_value('DEFINES', ['_DEBUG', 'DEBUG'])
    for flag_var in ('CFLAGS', 'CXXFLAGS'):
        ctx.env.append_value(flag_var, ['/MDd', '/Zi', '/Ob0', '/Od', '/RTC1'])
        ctx.env.append_value(flag_var, ['/FS'])

    ctx.env.append_value('LINKFLAGS', ['/DEBUG:FASTLINK'])

    '''
    For release build
    '''
    ctx.setenv('%s-release' % APPNAME, base_env)
    # the ctx.variant will be LambdaPractice-release
    Logs.info( "Release variant: %s" % ctx.variant )

    ctx.env.append_value('DEFINES', ['RELEASE'])
    for flag_var in ('CFLAGS', 'CXXFLAGS'):
        ctx.env.append_value(flag_var, ['/MD', '/O2', '/Ob2', '/DNDEBUG'])

def build(bld):
    bld.APPNAME = APPNAME

    # These will change according to what mode you use (--mode=...)
    Logs.info( "Mode: %s" % bld.mode )
    Logs.info( "Current: %s" % bld.variant )

    '''
    Manually get the proper env because the variant and the env name are not the same.
    The variant looks like 'LambdaPractice/debug'. We need it look like in this way because
    it is used to generate the output folders.
    The env name looks like 'LambdaPractice-debug'. We set it in cconfigure().
    '''
    env_name = bld._env_name
    Logs.info( "env_name: %s" % env_name )

    bld.env = bld.all_envs[env_name].derive()

    bld.program(
    source = 'LambdaExpressionPractice.cpp',
    target = 'LambdaPractice',
    includes='.'
    )