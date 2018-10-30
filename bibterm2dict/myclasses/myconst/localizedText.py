# -*- coding: utf-8 -*-
"""   """
INTERFACE_LANGS = {'langs':{'0':'en-US', '1':'fr-FR', '2':'pt-PT'},}

LOCALIZED_TEXT = { \
        'en-US':{ \
            '...':'...', \
            '{} already exist choose another name.':"{} already exist choose another name.", \
            'About...':'About...', \
            'Accept all new single renderings':'Accept all new single renderings', \
            'Accept selected renderings':'Accept selected renderings', \
            'Accept':'Accept', \
            'Accept_ttp':'Accept_ttp', \
            'AcceptRegionalDigits':\
                "Accept all regional renderings of digits", \
            'Add row':'Add row', \
            'AddCLDRfields':"Add the CLDR fields", \
            'All_ttp':"Show all terms with their possible and or suggested rendering along with the regional alternative rendering", \
            'Approved':"Approved", \
            'Approved_ttp':"Show all 'Approved' term/rendering pairs " + \
                "hiding all others.", \
            'Approved source/target language term pairs':\
                'Approved source/target language term pairs', \
            'Biblical terms list':'Biblical terms list', \
            'Biblical Terms':'Biblical Terms', \
            'BibTerms2Dict project':"BibTerms2Dict project", \
            'btnAll':"Collapse All", \
            'btnApproved':"Expand Approved", \
            'btnCLDR':"Expand CLDR", \
            'btnConflicts':"Expand Conflicts", \
            'btnSuggestions':"Expand Suggestions", \
            'btnUnknown':"Expand Unknown", \
            'Can not find the':'Can not find the', \
            'Cldr':"CLDR", \
            'CLDR':"CLDR", \
            'CLDR_ttp':"'CLDR' button will show the terms required for " + \
                "submission to prepare an application to include the " + \
                "language in the Common Language Data Repository.", \
            'Conflicts':"Conflicts", \
            'Conflicts_ttp':"Show all terms whose new rendering conflicts " + \
                "with that found in the old source/target map creator " + \
                "dictionary.", \
            'Current Project>':'Current Project:', \
            'Delete project settings':'Delete project settings', \
            'Delete Project':'Delete Project', \
            'Delete Project_ttp':'Delete an existing project file.', \
            'Delete row':'Delete row', \
            'DictIn_ttp':"Browse to the source/fallback dictionary " + \
                "exported from Map Creator.", \
            'empty string':'', \
            'Exit':'Exit', \
            'Expand/Collapse':"Expand/Collapse", \
            'f0_ttp':"Setup tab tooltip", \
            'F05Next_ttp':'F05Next_ttp', \
            'F0Next_ttp':'F0Next_ttp', \
            'fallback':'fallback', \
            'File':'File', \
            'Help':'Help', \
            'Interface language>':'Interface language:', \
            'is empty':"is empty", \
            'labelf2':'labelf2', \
            'labelf5':'labelf5', \
            'lblLoadTemplate':"Load template from...", \
            'lblPreferred':"A mapping for transliterating loan words from " + \
                "the national or regional fallback language into the " + \
                "orthography of the target language. " + \
                "A comma separated list of fallback character / target " + \
                "character pairs (e.g. ŋ/ng, Ŋ/Ng). " + \
                "Any unspecified characters will be passed through " + \
                "directly. You can also overide the mapping of " + \
                "punctuation characters (with the exception of '\\' " + \
                "and '/'), to specify a space or a comma use the 0xNNNN " + \
                "notation giving their Unicode value. This list can be " + \
                "changed at any time, but the changes will available " + \
                "until the 'Set template' button has been pressed.", \
            'Load project settings':'Load project settings', \
            'Load Regional':"Load Regional", \
            'Load Regional_ttp':"Load the regional rendering as the preferred entry.", \
            'Load Suggestion':"Load Suggestion", \
            'Load Suggestion_ttp':"Load suggested rendering as the preferred entry.", \
            'Load Transliterated Regional':"Load Transliterated Regional", \
            'Load Transliterated Regional_ttp':"Load the transliterated regional rendering as the preferred entry.", \
            'Map Creator Dictionary':"Map Creator Dictionary", \
            'New Project':"New Project", \
            'New Project_ttp':"Create a new project file and add it to the list.", \
            'Next':'Next', \
            "No '{}' will be loaded":"No '{}' will be loaded", \
            'Old Source/Target dictionary':'Old Source/Target dictionary', \
            "Output Dictionary":"Output Dictionary", \
            'OldDict_ttp':"Browse to the existing source/target dict file " + \
            "exported from Paratext Bilical Terms tool, if any.", \
            'Output':"Output", \
            'Paratext Biblical Terms':"Paratext Biblical Terms", \
            'Please enter a name for your project.':"Please enter the " + \
                "name of your target language. Or it's three letter " + \
                "Enthnologue code.", \
            'Please enter a valid path to your':\
                "Please enter a valid path to your", \
            'Project name':'Project name',\
            'Read Me':'Read Me', \
            'Reject':"Reject", \
            'Reject_ttp':"Reject the selected rendering. On an approved " + \
                "term this will move it to the 'Unknown' category unless " + \
                "suggestions can be made in which case it will be place " + \
                "in the 'Suggestions' category. On term with suggestions " + \
                "this will remove the selected suggestion, if only one " + \
                "rendering is left the term will be moved to the " + \
                "'Approved' category.", \
            'Reject all new renderings':'Reject all new renderings', \
            'Reject all selected renderings':\
                'Reject all selected renderings', \
            'Rendering':'Rendering', \
            'Save':'Save', \
            'Save_ttp':'Save_ttp', \
            'SavePref':"Save current template", \
            'Set template':"Set template", \
            'Setup':"Setup", \
            'Show':"Show", \
            'source':'source', \
            'Source language terms without target language renderings.':\
                "Source language terms without target language renderings.", \
            'Source/Fallback dictionary':'Source/Fallback dictionary', \
            'Source/Target dictionary':'Source/Target dictionary', \
            'Suggestions':"Suggestions", \
            'Suggestions_ttp':\
                "Show all unapproved terms, which have multiple possibel " + \
                "renderings. " + \
                "(N.B. Additional renderings may be suggested for terms " + \
                "without any renderings, based on the occurance " + \
                "of words in the source term within other approved terms.", \
            'target':'target', \
            'Term':'Term', \
            'Terms':'Terms', \
            'TermsIn_ttp':"Browse to the html file exported from Paratext " + \
                "Bilical Terms too.l", \
            'Transliteration (from fallback to target language)>':\
                "Transliteration (from fallback to target language):", \
            'Transliteration':'Transliteration', \
            'Transliterate':"Transliterate regional & load", \
            'Transliterate_ttp':"Load the transliterated regional rendering as the preferred entry.", \
            'Unknown':"Unknown", \
            'Unknown_ttp':"'Unknown' shows all terms with no suggested " + \
                "rendering. These will normally have the fallback " + \
                "(national/regional) language term shown. " + \
                "Defaulting to expanded.", \
            }, \
        'fr-FR':{ \
            'Current Project>':'Projet en cours:', \
            }, \
        'pt-PT':{ \
            'Current Project>':'Projeto atual:', \
            }
        }

TRIM_TAG = {'en-US':{ \
            'Nothing':'Nothing', \
            'Leading digits':'Leading digits', \
            'Leading alphanumerics':'Leading alphanumerics', \
            'Trailing digits':'Trailing digits' \
            }, \
        'fr-FR':{ \
            'Nothing':'Rien', \
            'Leading digits':'Chiffres initiauxs', \
            'Leading alphanumerics':'Alphanumériques précédents', \
            'Trailing digits':'Derniers chiffres' \
            }, \
        'pt-PT':{ \
            'Nothing':'Nada', \
            'Leading digits':'Dígitos iniciais', \
            'Leading alphanumerics':'Alfanuméricos iniciais', \
            'Trailing digits':'Dígitos finais' \
            } \
        }

CLDR = dict()