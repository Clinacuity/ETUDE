
import json

import args_and_configs

#############################################
## Test loading and reading of config files
#############################################

## Namespaces

def test_i2b2_2016_track_1_has_empty_namespace():
    config_file = 'config/i2b2_2016_track-1.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = config_file ,
                                       score_key = 'Short Name' )
    ## Empty dictionary resolves as False
    assert not bool( namespaces )
    

def test_sentences_has_defined_namespaces():
    config_file = 'config/uima_sentences.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = config_file ,
                                       score_key = 'Short Name' )
    ## Non-empty dictionary resolves as True
    expected_namespaces = \
      { 'type': 'http:///com/clinacuity/deid/nlp/uima/type.ecore',
        'type4': 'http:///de/tudarmstadt/ukp/dkpro/core/api/segmentation/type.ecore' 
      }
    assert namespaces == expected_namespaces
    

def test_webanno_custom_namespaces():
    config_file = 'config/webanno_uima_xmi.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = config_file ,
                                       score_key = 'Short Name' )
    ## Non-empty dictionary resolves as True
    expected_namespaces = { 'custom': 'http:///webanno/custom.ecore' }
    with open( '/tmp/stdout.log' , 'w' ) as fp:
        fp.write( '-----------\n{}\n-------------\n'.format( namespaces ) )
    assert namespaces == expected_namespaces
    

## Patterns

def test_set_score_key_Sentences():
    filename = 'config/uima_sentences.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = filename ,
                                       score_key = 'Short Name' )
    for pattern in patterns:
        assert pattern[ 'type' ] == "Sentence"

def test_set_score_key_DateTime_Tutorial():
    filename = 'config/CAS_XMI.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = filename ,
                                       score_key = 'Short Name' )
    for pattern in patterns:
        assert pattern[ 'type' ] == "DateTime"
    namespaces , patterns = \
      args_and_configs.process_config( config_file = filename ,
                                       score_key = 'Parent' )
    for pattern in patterns:
        assert pattern[ 'type' ] == "Time"
    namespaces , patterns = \
      args_and_configs.process_config( config_file = filename ,
                                       score_key = 'Long Name' )
    for pattern in patterns:
        assert pattern[ 'type' ] == "Date and Time Information"


def test_skip_missing_XPath():
    filename = 'config/i2b2_2016_track-1.conf'
    namespaces , patterns = \
      args_and_configs.process_config( config_file = filename ,
                                       score_key = 'Short Name' )
    for pattern in patterns:
        assert pattern[ 'long_name' ] != "Other Person Name"


#############################################
## Helper functions to help in setting up tests
#############################################

def convert_configs_to_json():
    fileroots = [ 'CAS_XMI' ,
                  'i2b2_2016_track-1' ,
                  'uima_sentences' ,
                  'webanno_uima_xmi' ]
    for fileroot in fileroots:
        filename = 'config/' + fileroot + '.conf'
        namespaces , patterns = \
          args_and_configs.process_config( config_file = filename ,
                                           score_key = 'Short Name' )
        with open( 'tests/data/' + fileroot + '.json' , 'w' ) as fp:
            json.dump( patterns , fp ,
                       indent = 4 )
