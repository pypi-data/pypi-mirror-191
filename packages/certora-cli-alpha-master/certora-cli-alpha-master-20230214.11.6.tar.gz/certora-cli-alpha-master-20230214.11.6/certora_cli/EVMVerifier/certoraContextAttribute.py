import argparse
from dataclasses import dataclass, field
from enum import unique, auto
from typing import Optional, Dict, Any

from Shared.certoraUtils import NoValEnum

RULE_SANITY_VALUES = ['none', 'basic', 'advanced']
MULTI_EXAMPLE_VALUES = ['none', 'basic']
APPEND = 'append'
STORE_TRUE = 'store_true'
STORE_FALSE = 'store_false'
VERSION = 'version'
SINGLE_OR_NONE_OCCURRENCES = '?'
MULTIPLE_OCCURRENCES = '*'
ONE_OR_MORE_OCCURRENCES = '+'


class AttrType(NoValEnum):
    STRING = auto()
    BOOLEAN = auto()
    ARRAY_OF_STRINGS = auto()
    DICTIONARY = auto()


class AttrFormat(NoValEnum):
    NONE = auto()
    ADDRESS = auto()  # str1:str2, str1 non-empty, str2 hex number
    ALWAYS_TRUE = auto()
    ASSERT_CONTRACTS = auto()  # string with alphanumeric or underscore characters
    BUILD_DIR = auto()  # path to writable non-existent directory
    CONF_FILE = auto()  # path to a file with '.conf' suffix
    DIR = auto()  # path to readable existing directory
    EXEC_FILE = auto()  # path to executable (file can be on $path)
    INPUT_FILE = auto()  # valid input file e.g. .sol, .vy, .tac, .conf .json suffix
    JAR = auto()  # executable existing file that ends with .jar
    JAVA_ARGS = auto()  # string that starts and ends with " and contains no "
    JSON_FILE = auto()  # valid existing readable json file ends with .json
    LINK_ARG = auto()  # <contractA:slot=contractB> or <contractA:slot=number>
    METHOD = auto()  # valid method declaration with params
    NON_NEGATIVE_INTEGER = auto()  # string that can be parsed as non-negative integer
    OPTIMIZE_MAP = auto()  # <contract_1>=<num_runs_1>,<contract_2>=<num_runs_2>,..
    OPTIONAL_READABLE_FILE = auto()  # path to file that either exists and readable or does not exist
    PACKAGES = auto()  # list of name=path separated by space
    POSITIVE_INTEGER = auto()  # like non-negative 0 is not allowed
    PROTOTYPE_ARG = auto()  # hex=name
    READABLE_FILE = auto()  # path to existing readable file
    RULE_SANITY_FLAG = auto()  # one of 'none', 'basic' or 'advanced'
    MULTI_EXAMPLE_FLAG = auto()
    SETTINGS_ARG = auto()  # valid flag for the jar
    SOLC_ARGS = auto()  # "[...]"
    SOLC_MAP = auto()  # map solc files to solc executables <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>,..
    STRUCT_LINK = auto()  # list of <contractA:number=contractB> or <contractA:fieldName=contractB">
    TOOL_OUTPUT_PATH = auto()  # path to writable file, may exist
    VERIFY_ARG = auto()  # string of the form contract:file.[spec|cvl]


class ArgGroups(NoValEnum):
    # The order of the groups is the order we want to show the groups in argParse's help
    MODE = "Mode of operation. Please choose one, unless using a .conf or .tac file"
    USEFUL = "Most frequently used options"
    RUN = "Options affecting the type of verification run"
    SOLIDITY = "Options that control the Solidity compiler"
    LOOP = "Options regarding source code loops"
    RUN_TIME = "Options that help reduce running time"
    LINKAGE = "Options to set addresses and link contracts"
    CREATION = "Options to model contract creation"
    INFO = "Debugging options"
    JAVA = "Arguments passed to the .jar file"
    PARTIAL = "These arguments run only specific parts of the tool, or skip parts"
    CLOUD = "Fine cloud control arguments"
    MISC_HIDDEN = "Miscellaneous hidden arguments"
    ENV = ""


@dataclass
class CertoraArgument:
    flag: Optional[str] = None  # override the 'default': option name
    group: Optional[ArgGroups] = None  # name of the arg parse (see ArgGroups above)
    help_msg: str = argparse.SUPPRESS

    # args for argparse's add_attribute passed as is
    argparse_args: Dict[str, Any] = field(default_factory=dict)
    format: AttrFormat = AttrFormat.NONE
    type: AttrType = AttrType.STRING


class UniqueStore(argparse.Action):
    """
    This class makes the argparser throw an error for a given flag if it was inserted more than once
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,  # type: ignore
                 option_string: str) -> None:
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(f"{option_string} appears several times.")
        setattr(namespace, self.dest, values)


class SplitArgsByCommas(argparse.Action):
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,
                 option_string: Optional[str] = None) -> None:
        new_values = values
        if isinstance(values, str):
            new_values = values.split(',')
        setattr(namespace, self.dest, new_values)


@unique
class ContextAttribute(NoValEnum):
    """
    This enum class must be unique. If 2 args have the same value we add the 'flag' attribute to make sure the hash
    value is not going to be the same

    The order of the attributes is the order we want to show the attributes in argParse's help

    """
    FILES = CertoraArgument(
        format=AttrFormat.INPUT_FILE,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac",
        flag='files',
        argparse_args={
            'nargs': MULTIPLE_OCCURRENCES
        }
    )

    VERIFY = CertoraArgument(
        group=ArgGroups.MODE,
        format=AttrFormat.VERIFY_ARG,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="Matches specification files to contracts. For example: -verify [contractName:specName.spec ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    ASSERT_CONTRACTS = CertoraArgument(
        group=ArgGroups.MODE,
        format=AttrFormat.ASSERT_CONTRACTS,
        type=AttrType.ARRAY_OF_STRINGS,
        flag='--assert',
        help_msg="The list of contracts to assert. Usage: --assert [contractName ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'dest': 'assert_contracts',
            'action': APPEND
        }
    )

    BYTECODE = CertoraArgument(
        group=ArgGroups.MODE,
        format=AttrFormat.JSON_FILE,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="List of EVM bytecode json descriptors. Usage: --bytecode [bytecode1.json ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'dest': 'bytecode_jsons',
            'action': APPEND
        }
    )

    BYTECODE_SPEC = CertoraArgument(
        group=ArgGroups.MODE,
        format=AttrFormat.READABLE_FILE,
        help_msg="Spec to use for the provided bytecodes. Usage: --bytecode_spec myspec.spec",
        argparse_args={
            'action': UniqueStore
        }
    )

    MSG = CertoraArgument(
        group=ArgGroups.USEFUL,
        help_msg="Add a message description (alphanumeric string) to your run.",
        argparse_args={
            'action': UniqueStore
        }
    )

    #  RULE option is for both --rule and --rules
    RULE = CertoraArgument(
        group=ArgGroups.USEFUL,
        help_msg="List of specific properties (rules or invariants) you want to verify. "
                 "Usage: --rule [rule1 rule2 ...] or --rules [rule1 rule2 ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    MULTI_ASSERT_CHECK = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="Check each assertion separately by decomposing every rule "
                 "into multiple sub-rules, each of which checks one assertion while it assumes all "
                 "preceding assertions",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    INCLUDE_EMPTY_FALLBACK = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="check the fallback method, even if it always reverts",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    RULE_SANITY = CertoraArgument(
        group=ArgGroups.RUN,
        format=AttrFormat.RULE_SANITY_FLAG,
        help_msg="Sanity checks for all the rules",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --rule_sanity given, may take from --settings
            'const': "basic"  # 'default': when --rule_sanity is given, but no argument to it
        }
    )

    MULTI_EXAMPLE = CertoraArgument(
        group=ArgGroups.RUN,
        format=AttrFormat.MULTI_EXAMPLE_FLAG,
        help_msg="produce multi-examples",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --multi_example given, may take from --settings
            'const': "basic"  # 'default': when --multi_example is given, but no argument to it
        }
    )

    SHORT_OUTPUT = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="Reduces verbosity. It is recommended to use this option in continuous integration",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_CALLTRACE_STORAGE_INFORMATION = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="Avoid adding storage information to CallTrace report.",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    TYPECHECK_ONLY = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="Stop after typechecking",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SEND_ONLY = CertoraArgument(
        group=ArgGroups.RUN,
        type=AttrType.BOOLEAN,
        help_msg="Do not wait for verifications results",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SOLC = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.EXEC_FILE,
        help_msg="Path to the Solidity compiler executable file",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_ARGS = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.SOLC_ARGS,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="List of string arguments to pass for the Solidity compiler, for example: "
                 "\"['--evm-version', 'istanbul', '--experimental-via-ir']\"",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.SOLC_MAP,
        type=AttrType.DICTIONARY,
        help_msg="Matches each Solidity file with a Solidity compiler executable. "
                 "Usage: <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>[,...] ",
        argparse_args={
            'action': UniqueStore
        }
    )

    PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.DIR,
        help_msg="Use the given path as the root of the source tree instead of the root of the "
                 "filesystem. Default: $PWD/contracts if exists, else $PWD",
        argparse_args={
            'action': UniqueStore
        }
    )

    OPTIMIZE = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        help_msg="Tells the Solidity compiler to optimize the gas costs of the contract for a given "
                 "number of runs",
        argparse_args={
            'action': UniqueStore
        }
    )

    OPTIMIZE_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.OPTIMIZE_MAP,
        type=AttrType.DICTIONARY,
        help_msg="Matches each Solidity source file with a number of runs to optimize for. "
                 "Usage: <sol_file_1>=<num_runs_1>,<sol_file_2>=<num_runs_2>[,...]",
        argparse_args={
            'action': UniqueStore
        }
    )

    PACKAGES_PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.DIR,
        help_msg="Path to a directory including the Solidity packages ('default':: $NODE_PATH)",
        argparse_args={
            'action': UniqueStore
        }
    )

    PACKAGES = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        format=AttrFormat.PACKAGES,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="A mapping [package_name=path, ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': UniqueStore
        }
    )

    OPTIMISTIC_LOOP = CertoraArgument(
        group=ArgGroups.LOOP,
        type=AttrType.BOOLEAN,
        help_msg="After unrolling loops, assume the loop halt conditions hold",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    LOOP_ITER = CertoraArgument(
        group=ArgGroups.LOOP,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        help_msg="The maximal number of loop iterations we verify for. Default: 1",
        argparse_args={
            'action': UniqueStore
        }
    )

    METHOD = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        format=AttrFormat.METHOD,
        help_msg="Parametric rules will only verify given method. "
                 "Usage: --method 'fun(uint256,bool)'",
        argparse_args={
            'action': UniqueStore
        }
    )

    CACHE = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        help_msg='name of the cache to use',
        argparse_args={

            'action': UniqueStore
        }
    )

    SMT_TIMEOUT = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        format=AttrFormat.POSITIVE_INTEGER,
        help_msg="Set max timeout for all SMT solvers in seconds, 'default': is 600",
        argparse_args={
            'action': UniqueStore
        }
    )

    LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        format=AttrFormat.LINK_ARG,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    ADDRESS = CertoraArgument(
        group=ArgGroups.LINKAGE,
        format=AttrFormat.ADDRESS,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="Set a contract's address to be the given address Format: <contractName>:<number>",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': UniqueStore
        }
    )

    STRUCT_LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        format=AttrFormat.STRUCT_LINK,
        type=AttrType.ARRAY_OF_STRINGS,
        flag='--structLink',
        help_msg="Linking to a struct field, <contractName>:<number>=<contractName>",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': UniqueStore,
            'dest': 'struct_link'
        }
    )

    PROTOTYPE = CertoraArgument(
        group=ArgGroups.CREATION,
        format=AttrFormat.PROTOTYPE_ARG,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="Execution of constructor bytecode with the given prefix should yield a unique instance of the "
                 "given contract",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    DYNAMIC_BOUND = CertoraArgument(
        group=ArgGroups.CREATION,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        help_msg="Maximum number of instances of a contract that can be created "
                 "with the CREATE opcode; if 0, CREATE havocs ('default':: 0)",
        argparse_args={
            'action': UniqueStore
        }
    )

    DYNAMIC_DISPATCH = CertoraArgument(
        group=ArgGroups.CREATION,
        type=AttrType.BOOLEAN,
        help_msg="If set, on a best effort basis automatically use dispatcher summaries for external"
                 " calls on contract instances generated by CREATE",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DEBUG = CertoraArgument(
        group=ArgGroups.INFO,
        format=AttrFormat.ALWAYS_TRUE,
        type=AttrType.ARRAY_OF_STRINGS,
        help_msg="Use this flag to see debug statements. A comma separated list filters logger topics",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'default': None,
            'const': [],
            'action': SplitArgsByCommas
        }
    )

    DEBUG_TOPICS = CertoraArgument(
        group=ArgGroups.INFO,
        format=AttrFormat.ALWAYS_TRUE,
        type=AttrType.BOOLEAN,
        help_msg="Include topic names in debug messages",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    VERSION = CertoraArgument(
        group=ArgGroups.INFO,
        format=AttrFormat.ALWAYS_TRUE,
        help_msg="Show the tool version",
        argparse_args={
            'action': VERSION,
            'version': 'This message should never be reached'
        }
    )

    JAR = CertoraArgument(
        group=ArgGroups.JAVA,
        format=AttrFormat.JAR,
        argparse_args={
            'action': UniqueStore
        }
    )

    JAVA_ARGS = CertoraArgument(
        group=ArgGroups.JAVA,
        format=AttrFormat.JAVA_ARGS,
        type=AttrType.ARRAY_OF_STRINGS,
        flag="--javaArgs",
        argparse_args={
            'action': APPEND,
            'dest': 'java_args'
        }
    )

    CHECK_ARGS = CertoraArgument(
        group=ArgGroups.PARTIAL,
        type=AttrType.BOOLEAN,
        flag='--check_args',  # added to prevent dup with DISABLE_LOCAL_TYPECHECKING
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_ONLY = CertoraArgument(
        group=ArgGroups.PARTIAL,
        flag='--build_only',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_DIR = CertoraArgument(
        group=ArgGroups.PARTIAL,
        format=AttrFormat.BUILD_DIR,
        help_msg="Path to the build directory",
        argparse_args={
            'action': UniqueStore
        }
    )

    DISABLE_LOCAL_TYPECHECKING = CertoraArgument(
        group=ArgGroups.PARTIAL,
        type=AttrType.BOOLEAN,
        flag='--disableLocalTypeChecking',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_COMPARE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        type=AttrType.BOOLEAN,
        flag='--no_compare',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    EXPECTED_FILE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        format=AttrFormat.OPTIONAL_READABLE_FILE,
        help_msg="JSON file to use as expected results for comparing the output",
        argparse_args={
            'action': UniqueStore
        }
    )

    QUEUE_WAIT_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        flag='--queue_wait_minutes',  # added to prevent dup with MAX_POLL_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_POLL_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        flag='--max_poll_minutes',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    LOG_QUERY_FREQUENCY_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        flag='--log_query_frequency_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_ATTEMPTS_TO_FETCH_OUTPUT = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        flag='--max_attempts_to_fetch_output',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    DELAY_FETCH_OUTPUT_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        flag='--delay_fetch_output_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    PROCESS = CertoraArgument(
        group=ArgGroups.CLOUD,
        format=AttrFormat.ALWAYS_TRUE,
        argparse_args={
            'action': UniqueStore,
            'default': 'emv'
        }
    )

    SETTINGS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.NONE,  # checking in a dedicated validate_settings()
        argparse_args={
            'action': APPEND
        }
    )

    LOG_BRANCH = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.ALWAYS_TRUE,
        argparse_args={
            'action': UniqueStore
        }
    )

    COMMIT_SHA1 = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        type=AttrType.STRING,
        argparse_args={
            'action': UniqueStore
        }
    )

    DISABLE_AUTO_CACHE_KEY_GEN = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        type=AttrType.BOOLEAN,
        argparse_args={
            'action': STORE_FALSE
        }
    )

    MAX_GRAPH_DEPTH = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.NON_NEGATIVE_INTEGER,
        argparse_args={
            'action': UniqueStore
        }
    )

    TOOL_OUTPUT = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.TOOL_OUTPUT_PATH,
        flag='--toolOutput',
        argparse_args={
            'action': UniqueStore,
            'dest': 'tool_output'
        }
    )

    INTERNAL_FUNCS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.JSON_FILE,
        argparse_args={
            'action': UniqueStore
        }
    )

    COINBASE_MODE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        type=AttrType.BOOLEAN,
        flag='--coinbaseMode',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    GET_CONF = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.CONF_FILE,
        argparse_args={
            'action': UniqueStore
        }
    )

    SKIP_PAYABLE_ENVFREE_CHECK = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        format=AttrFormat.ALWAYS_TRUE,
        type=AttrType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    STAGING = CertoraArgument(
        group=ArgGroups.ENV,
        format=AttrFormat.ALWAYS_TRUE,
        flag='--staging',  # added to prevent dup with CLOUD
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'default': None,
            'const': "",
            'action': UniqueStore
        }
    )

    CLOUD = CertoraArgument(
        group=ArgGroups.ENV,
        flag='--cloud',  # added to prevent dup with STAGING
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'default': None,
            'const': "",
            'action': UniqueStore
        }
    )
