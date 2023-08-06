"""
Module to convert RDF serialized metadata (first data model) into JSON metadata (new data model).
"""

import re
import os
from pathlib import Path
from typing import Any, Dict, List
from rdflib import Graph
from rdflib.namespace import Namespace, RDF, SDO, PROV, SKOS
import json
import jsonschema
from rdflib.term import BNode, Literal
import requests
import time
from datetime import datetime
from textblob import TextBlob
import guess_language
import langid
from langdetect import detect
from bs4 import BeautifulSoup


schema_url = "https://raw.githubusercontent.com/dasch-swiss/dsp-meta-svc/main/docs/services/metadata/schema-metadata.json"
dsp = Namespace("http://ns.dasch.swiss/repository#")


def convert_and_save(files: List[str], target: str) -> int:
    """Convert a list of metadata files and save output to files.

    Takes a list of `.ttl` files, converts each of them, and stores it to the specified target directory.

    Args:
        files (List[str]): paths to `.ttl` files that should be transformed.
        target (str): path to the target directory where the output files should be saved.

    Returns:
        int: The number of files that were converted.
    """
    res = 0
    for f in files:
        s = convert_file(f)
        print(f'File length: {len(s)}')
        fpath = Path(f)
        out = f"{target}/{fpath.stem}.json"
        print(out)
        with open(out, mode='w+', encoding='utf-8') as fw:
            fw.write(s)
        res += 1
    return res


def convert_files(files: List[str]) -> List[str]:
    """Convert multiple metadata files from a list of files.

    Convert metadata from local .ttl files.

    Args:
        files (List[str]): paths to .ttl files (can be relative or absolute)

    Returns:
        List[str]: list of json serialized metadata
    """
    return [convert_file(f) for f in files]


def convert_file(file: str) -> str:
    """Convert metadata from a file.

    Convert metadata from a local .ttl file.

    Args:
        file (str): path to a .ttl file (can be relative or absolute)

    Returns:
        str: json serialized metadata
    """
    with open(file, 'r+', encoding='utf-8') as f:
        s = f.read()
    return convert_string(s)


def convert_strings(data_list: List[str]) -> List[str]:
    """Convert multiple metadata sets from a list of strings.

    Args:
        data_list (List[str]): list of turtle serializations of metadata

    Returns:
        List[str]: list of json serialized metadata
    """
    return [convert_string(data) for data in data_list]


def convert_string(data: str) -> str:
    """Convert metadata from a string.

    Args:
        data (str): string of a turtle setrialization of metadata

    Returns:
        str: json serialized metadata
    """
    data = data.replace('@prefix schema: <https://schema.org/> .', '@prefix schema: <http://schema.org/> .')
    g = Graph()
    g.parse(data=data, format='ttl')
    res = {"$schema": schema_url}
    res['project'] = _get_project(g)
    res['datasets'] = _get_datasets(g)
    for ds in res.get('datasets'):  # type: ignore
        res['project']['datasets'].append(ds.get('__id'))  # type: ignore
    persons = _get_persons(g)
    if persons:
        res['persons'] = persons
    orgs = _get_organizations(g)
    if orgs:
        res['organizations'] = orgs
    grants = _get_grants(g)
    if grants:
        res['grants'] = grants

    validate(res)
    return json.dumps(res, indent=4, ensure_ascii=False)


# DMP
# ---


def _get_dmp(g: Graph):
    """Get data management plan from graph"""
    try:
        dmp = next(g.subjects(RDF.type, dsp.DataManagementPlan))
    except StopIteration:
        return {}

    res: Dict[str, Any] = {"__type": "DataManagementPlan"}

    for _, p, o in g.triples((dmp, None, None)):
        obj = str(o)
        if p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        elif p == dsp.isAvailable:
            res['available'] = obj == "true"
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Grant:", p, obj)

    return res


# Grant
# -----

def _get_grants(g: Graph):
    """Get grants from graph"""
    grants = g.subjects(RDF.type, dsp.Grant)
    return [_get_grant(g, grant) for grant in grants]


def _get_grant(g: Graph, grant_iri) -> Dict[str, Any]:
    """Get grant from graph"""
    res = {"__id": grant_iri,
           "__type": "Grant",
           "__createdAt": str(time.time_ns()),
           "__createdBy": "dsp-metadata-gui", }

    for _, p, o in g.triples((grant_iri, None, None)):
        obj = str(o).strip()
        if p == dsp.hasFunder:
            res.setdefault('funders', [])
            res['funders'].append(obj)
        elif p == dsp.hasNumber:
            res['number'] = obj
        elif p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Grant:", p, obj)

    return res


# Organizations
# -------------

def _get_organizations(g: Graph):
    """Get organizations from graph"""
    orgs = g.subjects(RDF.type, dsp.Organization)
    return [_get_organization(g, org) for org in orgs]


def _get_organization(g: Graph, org_iri):
    """Get organization from graph"""
    res = {"__id": org_iri,
           "__type": "Organization",
           "__createdAt": str(time.time_ns()),
           "__createdBy": "dsp-metadata-gui", }

    for _, p, o in g.triples((org_iri, None, None)):
        obj = str(o).strip()
        if p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasURL:
            res['url'] = _get_url(g, o)
        elif p == dsp.hasEmail:
            res['email'] = obj
        elif p == dsp.hasAddress:
            res['address'] = _get_address(g, o)
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Organization:", p, obj)

    return res


# Person
# ------

def _get_persons(g: Graph):
    """Get persons from graph"""
    persons = g.subjects(RDF.type, dsp.Person)
    return [_get_person(g, person) for person in persons]


def _get_person(g: Graph, person_iri):
    """Get person from graph"""
    res = {"__id": person_iri,
           "__type": "Person",
           "__createdAt": str(time.time_ns()),
           "__createdBy": "dsp-metadata-gui", }

    for _, p, o in g.triples((person_iri, None, None)):
        obj = str(o).strip()
        if p == dsp.hasJobTitle:
            res.setdefault('jobTitles', [])
            res['jobTitles'].append(obj)
        elif p == dsp.hasGivenName:
            res['givenNames'] = obj.split(';')
        elif p == dsp.hasFamilyName:
            res['familyNames'] = obj.split(';')
        elif p == dsp.isMemberOf:
            res.setdefault('affiliation', [])
            res['affiliation'].append(obj)
        elif p == dsp.hasAddress:
            res['address'] = _get_address(g, o)
        elif p == dsp.hasEmail:
            if res.get('email'):
                res['secondaryEmail'] = obj
            else:
                res['email'] = obj
        elif p == dsp.sameAs:
            res.setdefault('authorityRefs', [])
            res['authorityRefs'].append(_get_url(g, o))
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Person:", p, obj)

    return res


# Dataset
# -------

def _get_datasets(g: Graph):
    """Get datasets from graph"""
    datasets = g.subjects(RDF.type, dsp.Dataset)
    return [_get_dataset(g, dataset) for dataset in datasets]


def _get_dataset(g: Graph, dataset_iri):
    """Get dataset from graph"""
    res = {"__id": dataset_iri,
           "__type": "Dataset",
           "__createdAt": str(time.time_ns()),
           "__createdBy": "dsp-metadata-gui", }

    for _, p, o in g.triples((dataset_iri, None, None)):
        obj = str(o).strip()
        if p == dsp.hasTitle:
            res['title'] = obj
        elif p == dsp.hasConditionsOfAccess:
            obj = obj.lower()
            if obj not in ['open', 'restricted', 'closed']:
                obj = f"XX - Access Conditions should be one of 'open', 'restricted' or 'closed', but found: {obj}"
            res['accessConditions'] = obj
        elif p == dsp.hasHowToCite:
            res['howToCite'] = obj
        elif p == dsp.hasStatus:
            res['status'] = obj
        elif p == dsp.hasAbstract:
            res.setdefault("abstracts", [])
            if isinstance(o, BNode):
                res['abstracts'].append(_get_url(g, o))
            else:
                res['abstracts'].append(_guess_language_of_text(obj))
        elif p == dsp.hasTypeOfData:
            res.setdefault("typeOfData", [])
            if obj == "Movie":
                obj = "Video"
            res['typeOfData'].append(obj)
        elif p == dsp.hasLicense:
            res.setdefault("licenses", [])
            res['licenses'].append({"__type": "License",
                                    "date": str(datetime.date(datetime.now())),
                                    "license": _get_url(g, o)})
        elif p == dsp.hasLanguage:
            res.setdefault("languages", [])
            res['languages'].append(_get_language(obj))
        elif p == dsp.hasQualifiedAttribution:
            res.setdefault("attributions", [])
            res['attributions'] = (_add_attribution(g, o, res['attributions']))
        elif p == dsp.hasAlternativeTitle:
            res.setdefault("alternativeTitles", [])
            res['alternativeTitles'].append(_guess_language_of_text(obj))
        elif p == dsp.hasDateCreated:
            res['dateCreated'] = obj
        elif p == dsp.hasDatePublished:
            res['datePublished'] = obj
        elif p == dsp.hasDateModified:
            res['dateModified'] = obj
        elif p == dsp.hasDistribution:
            res['distribution'] = _get_url(g, o)
        elif p == dsp.sameAs:
            res.setdefault('urls', [])
            res['urls'].append(_get_url(g, o))
        elif p == dsp.hasDocumentation:
            res.setdefault("additional", [])
            if isinstance(o, BNode):
                res['additional'].append(_get_url(g, o))
            else:
                res['additional'].append(_guess_language_of_text(obj))
        elif p == dsp.isPartOf:
            pass
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Dataset:", p, obj)

    return res


# Project
# -------

def _get_project(g: Graph):
    """Get project from graph"""
    project_iri = next(g.triples((None, RDF.type, dsp.Project)))[0]
    res = {"__id": project_iri,
           "__type": "Project",
           "__createdAt": str(time.time_ns()),
           "__createdBy": "dsp-metadata-gui",
           "howToCite": "XX - new property on project level",
           "teaserText": "XX - new property",
           "datasets": []}

    for _, p, o in g.triples((project_iri, None, None)):
        obj = str(o).strip()
        if p == dsp.hasShortcode:
            res['shortcode'] = obj
        elif p == dsp.hasName:
            res['name'] = obj
        elif p == dsp.hasDescription:
            res['description'] = _guess_language_of_text(obj)
        elif p == dsp.hasStartDate:
            res['startDate'] = obj
        elif p == dsp.hasEndDate:
            res['endDate'] = obj
        elif p == dsp.hasKeywords:
            res.setdefault('keywords', [])
            res['keywords'].append(_guess_language_of_text(obj))
        elif p == dsp.hasDiscipline:
            res.setdefault('disciplines', [])
            if isinstance(o, BNode):
                res['disciplines'].append(_get_url(g, o))
            else:
                res['disciplines'].append(_guess_language_of_text(obj))
        elif p == dsp.hasTemporalCoverage:
            res.setdefault('temporalCoverage', [])
            if isinstance(o, BNode):
                res['temporalCoverage'].append(_get_url(g, o))
            else:
                res['temporalCoverage'].append(_guess_language_of_text(obj))
        elif p == dsp.hasSpatialCoverage:
            res.setdefault('spatialCoverage', [])
            res['spatialCoverage'].append(_get_place(g, o))
        elif p == dsp.hasURL:
            if res.get('url'):
                res['secondaryURL'] = _get_url(g, o)
            else:
                res['url'] = _get_url(g, o)
        elif p == dsp.hasDataManagementPlan:
            res['dataManagementPlan'] = _get_dmp(g)
        elif p == dsp.hasPublication:
            res.setdefault('publications', [])
            res['publications'].append(obj)
        elif p == dsp.hasGrant:
            res.setdefault('grants', [])
            res['grants'].append(obj)
        elif p == dsp.hasAlternateName:
            res.setdefault('alternativeNames', [])
            res['alternativeNames'].append(_guess_language_of_text(obj))
        elif p == dsp.hasFunder:
            res.setdefault('funders', [])
            res['funders'].append(obj)
        elif p == dsp.hasContactPoint:
            res['contactPoint'] = obj
        # default cases
        elif p == RDF.type:
            pass
        else:
            print("Issue: Could not handle in Project:", p, obj)

    return res


# Utils
# -----

def _add_attribution(g: Graph, iri: BNode, attributions: List):
    """From a graph g, add an attribution defined by a blank node (i.e. all tripples that have the iri as subject), to a list."""
    role = str(next(g.objects(iri, dsp.hasRole)))
    agent = str(next(g.objects(iri, PROV.agent)))
    for att in attributions:
        p = att.get('agent')
        r = att.get('roles')
        if r and p and p == agent:
            r.append(role)
            return attributions
    attributions.append({"__type": "Attribution",
                         "agent": agent,
                         "roles": [role]})
    return attributions


def _get_language(language):
    """Get the correct language representation according to a string describing a language (i.e. the language itself or a language shortcode)"""
    language = str(language)
    if re.match('^[a-z]{2}$', language):
        return _get_language_from_shortcode(language)
    else:
        return _guess_language_of_text(language)


def _get_language_from_shortcode(code):
    """Get language representation from a language shortcode"""
    code = str(code)
    langs = {'en': {'en': 'English',
                    'de': 'Englisch',
                    'fr': 'anglais'},
             'de': {'en': 'German',
                    'de': 'Deutsch',
                    'fr': 'allemand'},
             'fr': {'en': 'French',
                    'de': 'Französisch',
                    'fr': 'français'}}
    default = {code: 'XX - ' + code}
    lang = langs.get(code)
    return lang if lang else default


def _guess_language_of_text(text):
    """ Guess the language of a string.

    Returns a dict of type multilanguage text, if possible with the correct language attribution to the text.
    """
    probables = ["en", "de", "fr"]
    text = str(text)
    predefined = _get_predefined_multilanguage_string(text)
    if predefined:
        return predefined
    try:
        lang_txtblob = TextBlob(text).detect_language()
        if lang_txtblob in probables:
            return {lang_txtblob: text}
    except Exception:
        lang_txtblob = None
    try:
        guess = guess_language.guess_language(text, probables)
        if guess in probables:
            return {guess: text}
        if not isinstance(guess, str):
            guess = None
    except Exception as e:
        guess = None
    try:
        la_id, _ = langid.classify(text)
        det = detect(text)
        if det and la_id and det == la_id and det in probables:
            return {det: text}
    except Exception as e:
        det = None
    return {"XX": text}


def _get_address(g: Graph, iri: BNode):
    """Get address from graph"""
    locality = str(next(g.objects(iri, SDO.addressLocality)))
    code = str(next(g.objects(iri, SDO.postalCode)))
    street = str(next(g.objects(iri, SDO.streetAddress)))
    country = _get_country(locality)
    return {'__type': 'Address',
            'street': street,
            'postalCode': code,
            'locality': locality,
            'country': country}


def _get_country(locality):
    """Get country of an address

    Checks if the place is in Switzerland.
    """
    q = f"http://api.geonames.org/searchJSON?username=blandolt&name_equals={locality}&country=ch"
    r = requests.get(q)
    js = r.json()
    gn = js.get('geonames')
    return "Switzerland" if len(gn) > 0 else "XX - Switzerland?"


def _get_place(g: Graph, iri: BNode):
    """Get a place from graph"""
    url = next(g.objects(iri, SDO.url))
    return _get_url(g, url)


def _ensure_protocol_in_url(url: str):
    """Tries to ensure that a url starts with a valid protocol."""
    if url.startswith('https://') or url.startswith('http://'):
        return url
    else:
        return f'http://{url}'


def _get_url(g: Graph, iri: BNode):
    """Get URL from graph"""
    url = str(next(g.objects(iri, SDO.url))).strip()
    try:
        propID_bnode = next(g.objects(iri, SDO.propertyID))
        propID = str(next(g.objects(propID_bnode, SDO.propertyID)))
    except StopIteration:
        propID = url
    type_ = _get_url_type(propID)
    txt = _get_url_text(url, type_)
    url = _ensure_protocol_in_url(url)
    res = {"__type": "URL",
           "type": type_,
           "url": url
           }
    if txt:
        res['text'] = txt
    return res


def _get_predefined_multilanguage_string(text: str):
    knowns: Dict[str, Dict] = {'German': {'de': 'Deutsch',
                                          'en': 'German',
                                          'fr': 'allemand'},
                               'English': {'en': 'English',
                                           'de': 'Englisch',
                                           'fr': 'anglais'},
                               'Latin': {'en': 'Latin',
                                         'de': 'Latein',
                                         'fr': 'latin'},
                               'French': {'en': 'French',
                                          'de': 'Französisch',
                                          'fr': 'français'},
                               'Italian': {'en': 'Italian',
                                           'de': 'Italienisch',
                                           'fr': 'italien'}}
    known = knowns.get(text)
    if known:
        return known
    if re.search('^\d{4}( ?- ?\d{4})?$', text):  # date
        return {'de': text,
                'en': text,
                'fr': text}


def _get_url_text(url, t):
    """Get a reasonable display text for a URL of a defined type."""
    if t == 'URL':
        return url
    if t == 'Skos':
        return _get_skos_name(url)
    if t == 'Geonames':
        return _get_geonames_name(url)
    if t == 'Pleiades':
        return f"XX: Pleiades URL: {url}"
    if t == 'ORCID':
        return f"ORCID URL: {url}"
    if t == 'Periodo':
        return _get_periodo_name(url)
    if t == 'GND':
        return f"GND URL: {url}"
    if t == 'VIAF':
        return f"VIAF URL: {url}"
    if t == 'Creative Commons':
        return _get_cc_name(url)
    if t == 'Chronontology':
        return _get_chronontology_name(url)
    f"XX: Unknown Type for URL: {url}"


def _get_periodo_name(url: str):
    """Get display text for a Periodo URL"""
    try:
        r = requests.get(url + '.json')
        data = r.json()
        res = data.get('label')
        return res
    except Exception:
        return f'XX: Periodo URL: {url}'


def _get_chronontology_name(url: str):
    """Get display text for a ChronOntology URL"""
    try:
        id_ = url.rsplit('/', maxsplit=1)[-1]
        r = requests.get(f'https://chronontology.dainst.org/data/period/{id_}')
        data = r.json()
        names = data.get('resource').get('names').get('en')
        return names[0]
    except Exception:
        return f'XX: Chronontology URL: {url}'


# LATER: this should not be called "SKOS"
def _get_skos_name(url: str):
    """Get display text for a SKOS URL"""
    url = url.removesuffix('/')
    url = url.removesuffix('/html')
    try:
        url += '/n-triples'
        r = requests.get(url)
        data = r.text
        g = Graph()
        g.parse(data=data, format='n3')
        labels = g.objects(predicate=SKOS.prefLabel)
        for label in labels:
            l: Literal = label
            if l.language == 'en':
                return str(l)
    except Exception:
        return f'XX: Skos URL: {url}'


def _get_cc_name(url: str):
    """Get display text for a Creative Commons URL"""
    try:
        r = requests.get(url.strip())
        soup = BeautifulSoup(r.content, 'html.parser')
        ident = soup.select_one('span.cc-license-identifier')
        res: str = ident.get_text()
        res = res.strip().removeprefix('(').removesuffix(')')
        return res
    except Exception:
        return f'XX: CC URL: {url}'


def _get_geonames_name(url: str):
    """Get display text for a geonames URL"""
    if url.endswith('/'):
        url = url.removesuffix('/')
    try:
        if re.search('\/countries\/', url):
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            tables = soup.select('table')
            table = tables[1]
            link = table.select_one('a')
            url = link['href']
        if url.endswith(".html"):
            url = url.rsplit("/", 1)[0]
        gn_id = url.rsplit("/")[-1]
        base = f'http://api.geonames.org/getJSON'
        payload = {'geonameId': gn_id,
                   'username': 'blandolt'}
        r = requests.get(base, params=payload)
        resp = r.json()
        name = resp.get('name')
        if not name:
            raise Exception()
        return name
    except Exception:
        return f'XX: Geonames URL: {url}'


def _get_url_type(propID):
    """Get URL type from schema.propertyID"""
    if propID.startswith("SKOS"):
        return "Skos"
    if propID.startswith("Geonames"):
        return "Geonames"
    if propID.startswith("Pleiades"):
        return "Pleiades"
    if propID.startswith("ORCID"):
        return "ORCID"
    if propID.startswith("Periodo"):
        return "Periodo"
    if propID.startswith("ChronOntology") or propID.startswith("dainst."):
        return "Chronontology"
    if propID.startswith("GND"):
        return "GND"
    if propID.startswith("VIAF"):
        return "VIAF"
    if propID.startswith("Creative Commons"):
        return "Creative Commons"
    else:
        return "URL"


def validate(data, verbose=False):
    """Validates JSON

    Validates json serialized data against the schema of the API specification.  

    [Schema](https://raw.githubusercontent.com/dasch-swiss/dasch-service-platform/main/docs/services/metadata/schema-metadata.json)

    Args:
        data ([type]): [description]
    """
    r = requests.get(schema_url)
    schema = r.json()
    try:
        if verbose:
            print("Validating...")
        validator = jsonschema.Draft7Validator(schema)
        valid = True
        for e in validator.iter_errors(data):
            if verbose:
                print(f'Validation Error: {e.message}')
            valid = False
        if valid and verbose:
            print("JSON is valid.")
        return valid
    except jsonschema.ValidationError as val:
        if verbose:
            print(val.message)
        return False


if __name__ == "__main__":
    files = ['maximal.ttl',
             'rosetta.ttl',
             'limc.ttl',
             'awg.ttl',
             'hdm.ttl',
             'drawings-gods.ttl'
             ]
    results = {}
    os.makedirs('out', exist_ok=True)
    for filename in files:
        print(f'Converting: {filename}...')
        s = convert_file(f'test/test-data/{filename}')
        issues = s.count("XX")
        results[filename] = {
            'isValid': validate(s),
            'numberOfIssues': issues,
            'toResolve': [l.strip().replace('"', "'") for l in s.splitlines() if 'XX' in l]
        }
        print(f'Number of issues encountered: {issues}')
        out = filename.replace('.ttl', '.json')
        with open(f'out/{out}', mode='w+', encoding='utf-8') as f:
            f.write(s)
        print(f'Saved as: {out}\nDone.\n\n----\n')
    print(json.dumps(results, indent=4))
