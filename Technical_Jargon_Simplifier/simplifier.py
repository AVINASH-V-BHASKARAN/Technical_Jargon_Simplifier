"""A small, deterministic jargon simplifier. No trained model or third-party API."""
import re
import unicodedata

# plain is a short phrase for the rewritten sentence; definition is shown in full.
GLOSSARY = [{'term': 'machine learning',
  'category': 'AI',
  'aliases': ['machine learning'],
  'plain': 'learning patterns from examples',
  'definition': 'A way for computers to learn patterns from examples.'},
 {'term': 'algorithm',
  'category': 'Computer science',
  'aliases': ['algorithm', 'algorithms'],
  'plain': 'step-by-step method',
  'definition': 'A set of steps used to solve a problem.',
  'plural': 'step-by-step methods',
  'plural_aliases': ['algorithms']},
 {'term': 'training dataset',
  'category': 'AI',
  'aliases': ['training dataset', 'training datasets', 'training data'],
  'plain': 'examples used for learning',
  'definition': 'Examples used to teach a computer system.'},
 {'term': 'predictive model',
  'category': 'AI',
  'aliases': ['predictive model', 'predictive models'],
  'plain': 'system that makes predictions',
  'definition': 'A system that uses learned patterns to predict an outcome.',
  'plural': 'systems that make predictions',
  'plural_aliases': ['predictive models']},
 {'term': 'neural network',
  'category': 'AI',
  'aliases': ['neural network', 'neural networks'],
  'plain': 'system of connected computing units',
  'definition': 'A computer system with connected units that learns patterns from data.',
  'plural': 'systems of connected computing units',
  'plural_aliases': ['neural networks']},
 {'term': 'deep learning',
  'category': 'AI',
  'aliases': ['deep learning'],
  'plain': 'learning with many layers of connected units',
  'definition': 'A type of machine learning that uses neural networks with many layers.'},
 {'term': 'natural language processing',
  'category': 'AI',
  'aliases': ['natural language processing', 'NLP'],
  'plain': 'computer processing of human language',
  'definition': 'Methods that help computers work with human language.'},
 {'term': 'classification',
  'category': 'AI',
  'aliases': ['classification'],
  'plain': 'sorting items into groups',
  'definition': 'Assigning an item to a predefined group.'},
 {'term': 'regression',
  'category': 'AI',
  'aliases': ['regression'],
  'plain': 'predicting a number',
  'definition': 'Estimating a numerical value from other information.'},
 {'term': 'overfitting',
  'category': 'AI',
  'aliases': ['overfitting'],
  'plain': 'learning the examples too closely',
  'definition': 'Learning training examples so closely that performance on new examples suffers.'},
 {'term': 'dataset',
  'category': 'AI',
  'aliases': ['dataset', 'datasets'],
  'plain': 'collection of examples',
  'definition': 'A collection of related examples or records.',
  'plural': 'collections of examples',
  'plural_aliases': ['datasets']},
 {'term': 'inference',
  'category': 'AI',
  'aliases': ['inference'],
  'plain': 'using a learned system to make a prediction',
  'definition': 'Using an already learned system to produce an answer for new input.'},
 {'term': 'tokenization',
  'category': 'AI',
  'aliases': ['tokenization', 'tokenisation'],
  'plain': 'splitting text into small pieces',
  'definition': 'Splitting text into pieces such as words and punctuation.'},
 {'term': 'API',
  'category': 'Programming',
  'aliases': ['API', 'APIs', 'application programming interface'],
  'plain': 'way for programs to communicate',
  'definition': 'A set of rules that lets one program communicate with another.',
  'plural': 'ways for programs to communicate',
  'plural_aliases': ['apis']},
 {'term': 'compiler',
  'category': 'Programming',
  'aliases': ['compiler', 'compilers'],
  'plain': 'program that translates code',
  'definition': 'A program that translates source code into another form for execution.',
  'plural': 'programs that translate code',
  'plural_aliases': ['compilers']},
 {'term': 'source code',
  'category': 'Programming',
  'aliases': ['source code'],
  'plain': 'instructions written by a programmer',
  'definition': 'Instructions written in a programming language.'},
 {'term': 'variable',
  'category': 'Programming',
  'aliases': ['variable', 'variables'],
  'plain': 'named place that holds a value',
  'definition': 'A name used to refer to a stored value.',
  'plural': 'named places that hold values',
  'plural_aliases': ['variables']},
 {'term': 'function',
  'category': 'Programming',
  'aliases': ['function', 'functions'],
  'plain': 'reusable block of instructions',
  'definition': 'A reusable block of instructions that performs a task.',
  'plural': 'reusable blocks of instructions',
  'plural_aliases': ['functions']},
 {'term': 'recursion',
  'category': 'Programming',
  'aliases': ['recursion'],
  'plain': 'solving a problem by calling the same method on smaller parts',
  'definition': 'A technique where a function calls itself to solve smaller parts of a problem.'},
 {'term': 'iteration',
  'category': 'Programming',
  'aliases': ['iteration', 'iterations'],
  'plain': 'repeated step',
  'definition': 'Repeating a set of steps.',
  'plural': 'repeated steps',
  'plural_aliases': ['iterations']},
 {'term': 'debugging',
  'category': 'Programming',
  'aliases': ['debugging'],
  'plain': 'finding and fixing errors',
  'definition': 'Finding and fixing mistakes in a program.'},
 {'term': 'exception',
  'category': 'Programming',
  'aliases': ['exception', 'exceptions'],
  'plain': 'event that interrupts normal program flow',
  'definition': 'An event that interrupts normal program execution, often because of an error.',
  'plural': 'events that interrupt normal program flow',
  'plural_aliases': ['exceptions']},
 {'term': 'object-oriented programming',
  'category': 'Programming',
  'aliases': ['object-oriented programming', 'object oriented programming', 'OOP'],
  'plain': 'organizing code around data and related actions',
  'definition': 'Organizing a program into objects that combine data with related actions.'},
 {'term': 'database',
  'category': 'Computer science',
  'aliases': ['database', 'databases'],
  'plain': 'organized store of information',
  'definition': 'An organized collection of information that can be searched and updated.',
  'plural': 'organized stores of information',
  'plural_aliases': ['databases']},
 {'term': 'data structure',
  'category': 'Computer science',
  'aliases': ['data structure', 'data structures'],
  'plain': 'way to organize information',
  'definition': 'A way to organize and store information for use by a program.',
  'plural': 'ways to organize information',
  'plural_aliases': ['data structures']},
 {'term': 'binary search',
  'category': 'Computer science',
  'aliases': ['binary search'],
  'plain': 'searching sorted items by halving the search area',
  'definition': 'Finding an item in sorted data by repeatedly checking half of the remaining items.'},
 {'term': 'operating system',
  'category': 'Computer science',
  'aliases': ['operating system', 'operating systems'],
  'plain': 'software system that manages a computer',
  'definition': 'Software that manages a computer and helps other programs run.',
  'plural': 'software systems that manage computers',
  'plural_aliases': ['operating systems']},
 {'term': 'cache',
  'category': 'Computer science',
  'aliases': ['cache', 'caches'],
  'plain': 'fast store of recently used information',
  'definition': 'A store that keeps recently used information for faster access.',
  'plural': 'fast stores of recently used information',
  'plural_aliases': ['caches']},
 {'term': 'encryption',
  'category': 'Computer science',
  'aliases': ['encryption'],
  'plain': 'scrambling information to protect it',
  'definition': 'Turning information into a protected form that requires a key to read.'},
 {'term': 'authentication',
  'category': 'Computer science',
  'aliases': ['authentication'],
  'plain': 'checking who someone is',
  'definition': 'Checking that a person or system is who it claims to be.'},
 {'term': 'authorization',
  'category': 'Computer science',
  'aliases': ['authorization', 'authorisation'],
  'plain': 'checking what someone may access',
  'definition': 'Deciding what an identified person or system is allowed to access.'},
 {'term': 'cloud computing',
  'category': 'Computer science',
  'aliases': ['cloud computing'],
  'plain': 'using computing resources over the internet',
  'definition': 'Using computing services delivered over a network, often the internet.'},
 {'term': 'bandwidth',
  'category': 'Networking',
  'aliases': ['bandwidth'],
  'plain': 'the amount of data a connection can carry per second',
  'definition': 'The maximum amount of data a connection can carry in a given time.'},
 {'term': 'latency',
  'category': 'Networking',
  'aliases': ['latency'],
  'plain': 'the delay before data arrives',
  'definition': 'The delay between an action and the response or arrival of data.'},
 {'term': 'protocol',
  'category': 'Networking',
  'aliases': ['protocol', 'protocols'],
  'plain': 'set of rules for communication',
  'definition': 'A set of rules used by devices or programs to communicate.',
  'plural': 'sets of rules for communication',
  'plural_aliases': ['protocols']},
 {'term': 'IP address',
  'category': 'Networking',
  'aliases': ['IP address', 'IP addresses'],
  'plain': 'address used to identify a network connection',
  'definition': 'A numerical address used to identify a network connection.',
  'plural': 'addresses used to identify network connections',
  'plural_aliases': ['ip address', 'ip addresses']},
 {'term': 'router',
  'category': 'Networking',
  'aliases': ['router', 'routers'],
  'plain': 'device that forwards data between networks',
  'definition': 'A device that directs data from one network to another.',
  'plural': 'devices that forward data between networks',
  'plural_aliases': ['routers']},
 {'term': 'packet',
  'category': 'Networking',
  'aliases': ['packet', 'packets'],
  'plain': 'small piece of transmitted data',
  'definition': 'A small unit of data sent across a network.',
  'plural': 'small pieces of transmitted data',
  'plural_aliases': ['packets']},
 {'term': 'firewall',
  'category': 'Networking',
  'aliases': ['firewall', 'firewalls'],
  'plain': 'filter that controls network traffic',
  'definition': 'A system that allows or blocks network traffic according to rules.',
  'plural': 'filters that control network traffic',
  'plural_aliases': ['firewalls']},
 {'term': 'DNS',
  'category': 'Networking',
  'aliases': ['DNS', 'domain name system'],
  'plain': 'the service that looks up website addresses',
  'definition': 'A system that translates domain names into network addresses.'},
 {'term': 'TCP',
  'category': 'Networking',
  'aliases': ['TCP', 'transmission control protocol'],
  'plain': 'rules for reliable delivery of network data',
  'definition': 'A network protocol that provides ordered and reliable delivery of data.'},
 {'term': 'HTTP',
  'category': 'Networking',
  'aliases': ['HTTP', 'hypertext transfer protocol'],
  'plain': 'rules used to request and send web content',
  'definition': 'A protocol used by web clients and servers to exchange content.'}]

# Stopwords are removed ONLY in the inspection view, never from sentences to rewrite.
STOPWORDS = {'a','an','the','is','are','was','were','to','of','and','in','on','for','with','by','it','this','that'}

def normalize_text(text):
    text = unicodedata.normalize('NFKC', text)
    text = text.translate(str.maketrans({'\u2018':"'",'\u2019':"'",'\u2013':'-','\u2014':'-'}))
    return re.sub(r'\s+', ' ', text).strip()

def preprocess(text):
    normalized = normalize_text(text)
    tokens = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?|[^\w\s]", normalized.lower())
    words = [t for t in tokens if any(c.isalpha() for c in t)]
    return {'normalized':normalized, 'tokens':tokens,
            'content_tokens':[t for t in words if t not in STOPWORDS]}

def alias_pattern(alias):
    return r'[\s-]+'.join(re.escape(word) for word in re.split(r'[\s-]+', alias))

# One combined pattern tries longer phrases first. Replacements are never re-scanned.
ALIASES = [(alias, entry) for entry in GLOSSARY for alias in entry['aliases']]
ALIASES.sort(key=lambda pair:len(pair[0]), reverse=True)
TERM_PATTERN = re.compile(r'(?<!\w)(?:'+'|'.join(alias_pattern(a) for a,e in ALIASES)+r')(?!\w)', re.I)
ALIAS_MAP = {re.sub(r'[\s-]+',' ',a.lower()):e for a,e in ALIASES}

def entry_for(match):
    return ALIAS_MAP[re.sub(r'[\s-]+',' ',match.group().lower())]

def plain_for(match):
    entry = entry_for(match)
    alias = re.sub(r'[\s-]+',' ',match.group().lower())
    if alias in entry.get('plural_aliases', []):
        return entry['plural']
    return entry['plain']

def detect_terms(text):
    found = {}
    for match in TERM_PATTERN.finditer(text):
        e = entry_for(match)
        if e['term'] not in found:
            found[e['term']] = {'term':e['term'], 'definition':e['definition'],
                                'category':e['category'], 'count':0}
        found[e['term']]['count'] += 1
    return list(found.values())

# Small, visible sentence rules. They are not a language model or a general paraphraser.
SIMPLE_WORDS = {'utilize':'use','utilizes':'uses','utilized':'used','optimize':'improve',
                'facilitate':'help','facilitates':'helps','commence':'start','subsequently':'then'}

def simplify_sentence(sentence):
    # A limited learning-pattern rewrite gives a natural explanation when applicable.
    pattern = r'(.+?)\s+(?:utilize|use)\s+training\s+datasets?\s+to\s+(?:optimize|improve)\s+predictive\s+models?([.!?]?)'
    learning = re.fullmatch(pattern, sentence, re.I)
    if learning:
        subject = re.sub(r'\balgorithms\b','methods',learning.group(1),flags=re.I)
        return subject+' learn from examples to make better predictions'+learning.group(2)
    # A compact noun phrase follows each original term, preserving sentence structure.
    result = TERM_PATTERN.sub(plain_for, sentence)
    for difficult, simple in SIMPLE_WORDS.items():
        result = re.sub(r'\b'+difficult+r'\b',simple,result,flags=re.I)
    result = re.sub(r'\b(a|an|the)\s+(?:a|an|the)\s+', r'\1 ', result, flags=re.I)
    result = re.sub(r'\ban\s+(?=[bcdfghjklmnpqrstvwxyz])', 'a ', result, flags=re.I)
    result = re.sub(r'\ba\s+(?=[aeiou])', 'an ', result, flags=re.I)
    if result:
        result = result[0].upper()+result[1:]
    return result

def simplify(text):
    if not isinstance(text,str):
        raise TypeError('Input must be text.')
    processed = preprocess(text)
    normalized = processed['normalized']
    terms = detect_terms(normalized)
    if not normalized:
        return {'original':text,'normalized':'','simplified':'','terms':[],
                'preprocessing':processed,'explanation':'Enter some text to begin.','status':'empty'}
    if not terms:
        return {'original':text,'normalized':normalized,'simplified':normalized,'terms':[],
                'preprocessing':processed,'explanation':'No glossary terms were recognized. The text is unchanged.','status':'no_terms'}
    sentences = re.split(r'(?<=[.!?])\s+', normalized)
    simplified = ' '.join(simplify_sentence(s) for s in sentences)
    definitions = '\n'.join(f"{t['term']}: {t['definition']}" for t in terms)
    return {'original':text,'normalized':normalized,'simplified':simplified,'terms':terms,
            'preprocessing':processed,'explanation':simplified+'\n\nTerms explained\n'+definitions,'status':'simplified'}

# Expected labels are manually specified; evaluation does not generate its own answers.
SAMPLES = [
    ('Machine learning algorithms utilize training datasets to optimize predictive models.', {'machine learning','algorithm','training dataset','predictive model'}),
    ('A neural network supports deep learning.', {'neural network','deep learning'}),
    ('Classification and regression use a dataset.', {'classification','regression','dataset'}),
    ('Overfitting reduces the value of inference.', {'overfitting','inference'}),
    ('Tokenization is used in natural language processing.', {'tokenization','natural language processing'}),
    ('The compiler checks source code.', {'compiler','source code'}),
    ('Debugging finds an exception in a function.', {'debugging','exception','function'}),
    ('Recursion and iteration can update variables.', {'recursion','iteration','variable'}),
    ('An API reads a database.', {'API','database'}),
    ('Binary search uses a data structure.', {'binary search','data structure'}),
    ('The operating system uses a cache.', {'operating system','cache'}),
    ('Encryption does not replace authentication or authorization.', {'encryption','authentication','authorization'}),
    ('Bandwidth and latency affect a protocol.', {'bandwidth','latency','protocol'}),
    ('A router forwards packets to an IP address.', {'router','packet','IP address'}),
    ('A firewall checks TCP and HTTP traffic; DNS looks up names.', {'firewall','TCP','HTTP','DNS'}),
    ('Object-oriented programming can be used in cloud computing.', {'object-oriented programming','cloud computing'}),
    ('The cat sleeps on the chair.', set()),
    ('   ', set()),
]

def evaluate():
    rows = []
    for text, expected in SAMPLES:
        result = simplify(text)
        detected = {x['term'] for x in result['terms']}
        detection_ok = detected == expected
        explanation_ok = all(x['definition'] in result['explanation'] for x in result['terms'])
        rows.append({'text':text, 'expected':sorted(expected), 'detected':sorted(detected),
                     'detection_pass':detection_ok, 'explanation_pass':explanation_ok,
                     'passed':detection_ok and explanation_ok, 'output':result['simplified']})
    return {'total':len(rows),'passed':sum(x['passed'] for x in rows),'cases':rows,
            'note':'Exact expected-term set and definition inclusion on these handcrafted examples; not readability or real-world accuracy.'}
